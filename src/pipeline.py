
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


def load_config(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def run(config_path: str = "configs/default.yaml") -> None:
    cfg = load_config(config_path)
    rng = np.random.default_rng(cfg.get("seed", 42))
    x = rng.normal(size=(240, 8))
    y = (x[:, 0] + x[:, 1] * 0.5 + rng.normal(0, 0.2, 240) > 0).astype(int)
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=cfg.get("seed", 42), test_size=0.25)
    model = RandomForestClassifier(random_state=cfg.get("seed", 42)).fit(x_train, y_train)
    preds = model.predict(x_test)
    report = Path("reports")
    report.mkdir(exist_ok=True)
    pd.DataFrame([{
        "accuracy": accuracy_score(y_test, preds),
        "macro_f1": f1_score(y_test, preds, average="macro"),
    }]).to_csv(report / "metrics.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    run(parser.parse_args().config)
