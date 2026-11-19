import numpy as np
import pandas as pd
import torch
import torch.nn as nn


class _GRUModel(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 16):
        super().__init__()
        self.gru = nn.GRU(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        out, _ = self.gru(x)
        return self.fc(out[:, -1, :])


def prognozuj_gru(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int, epoki: int = 60) -> pd.Series:
    print("\n--- Trenowanie sieci GRU ---")
    torch.manual_seed(42)

    y_raw = df.iloc[:, 0].to_numpy(dtype=float)
    n = len(y_raw)

    mean_y = y_raw.mean()
    std_y = y_raw.std() if y_raw.std() > 0 else 1.0
    y_norm = (y_raw - mean_y) / std_y

    has_exog = df.shape[1] > 1
    if has_exog:
        exog_raw = df.iloc[:, 1:].to_numpy(dtype=float)
        mean_exog = exog_raw.mean(axis=0)
        std_exog = np.where(exog_raw.std(axis=0) > 0, exog_raw.std(axis=0), 1.0)
        exog_norm = (exog_raw - mean_exog) / std_exog

        exog_fut_raw = df_przyszle.to_numpy(dtype=float)
        exog_fut_norm = (exog_fut_raw - mean_exog) / std_exog
        features = np.column_stack([y_norm, exog_norm])
    else:
        features = y_norm.reshape(-1, 1)

    window = max(1, min(3, n // 3))
    input_dim = features.shape[1]

    X, Y = [], []
    for i in range(n - window):
        X.append(features[i:i + window])
        Y.append(y_norm[i + window])

    X_t = torch.tensor(np.array(X), dtype=torch.float32)
    Y_t = torch.tensor(np.array(Y), dtype=torch.float32).unsqueeze(-1)

    model = _GRUModel(input_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
    loss_fn = nn.MSELoss()

    for _ in range(epoki):
        loss = loss_fn(model(X_t), Y_t)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        in_sample = model(X_t).squeeze(-1).numpy() * std_y + mean_y
    pred_hist = np.concatenate([y_raw[:window], in_sample])

    # Generowanie prognozy na przyszłość
    curr_features = [features[i] for i in range(n)]
    fut_preds = []
    for h in range(horyzont):
        seq = np.array(curr_features[-window:])
        inp = torch.tensor(seq, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            next_y_norm = model(inp).item()
        fut_preds.append(next_y_norm * std_y + mean_y)

        if has_exog:
            next_feat = np.concatenate([[next_y_norm], exog_fut_norm[h]])
        else:
            next_feat = np.array([next_y_norm])
        curr_features.append(next_feat)

    przyszle_daty = pd.date_range(start=df.index[-1], periods=horyzont + 1, freq=df.index.freq)[1:]
    s_hist = pd.Series(pred_hist, index=df.index)
    s_fut = pd.Series(fut_preds, index=przyszle_daty)
    return pd.concat([s_hist, s_fut])
