"""Tests for config validation and the end-to-end pipeline."""
import pandas as pd
import pytest
import yaml

from factorlab.config import load_config
from factorlab.pipeline import run

from conftest import EXAMPLE_CONFIG, REPO


def _write_config(tmp_path, patch):
    from conftest import RAW
    cfg = yaml.safe_load(EXAMPLE_CONFIG.read_text())
    # point at the real data with absolute paths (tmp config lives elsewhere)
    cfg["data"]["factors"] = str(RAW / "Europe_5_Factors.csv")
    cfg["data"]["portfolios"] = str(RAW / "Europe_25_Portfolios_ME_BE-ME.csv")
    for keys, value in patch.items():
        node = cfg
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
    p = tmp_path / "config.yaml"
    p.write_text(yaml.safe_dump(cfg))
    return p


def test_load_example_config():
    cfg = load_config(EXAMPLE_CONFIG)
    assert cfg["models"].keys() >= {"FF3", "FF5"}
    assert cfg["universe"]["risk_free"] == "RF"


def test_config_missing_data_raises(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("models:\n  FF3: [Mkt-RF]\n")
    with pytest.raises(ValueError, match="data.factors"):
        load_config(p)


def test_pipeline_rejects_unknown_factor(tmp_path):
    cfg_path = _write_config(tmp_path, {("models",): {"FF3": ["Mkt-RF", "NOPE"]}})
    with pytest.raises(ValueError, match="NOPE"):
        run(cfg_path, output_dir=tmp_path / "out")


def test_pipeline_rejects_empty_sample(tmp_path):
    cfg_path = _write_config(tmp_path, {("data", "start"): "2030-01"})
    with pytest.raises(ValueError, match="empty"):
        run(cfg_path, output_dir=tmp_path / "out")


def test_pipeline_end_to_end_headlines(tmp_path):
    out = tmp_path / "out"
    result = run(EXAMPLE_CONFIG, output_dir=out)
    stats = result["factor_stats"]
    assert stats.loc["SMB", "ann_mean_pct"] == pytest.approx(0.15, abs=0.01)
    assert stats.loc["RMW", "t_mean"] == pytest.approx(3.89, abs=0.01)
    grs = result["grs"].set_index("model")
    assert grs.loc["FF3", "GRS_F"] == pytest.approx(3.046066, rel=1e-4)
    assert grs.loc["FF5", "GRS_F"] == pytest.approx(2.705853, rel=1e-4)
    reg5 = result["reg_tables"]["FF5"]
    assert reg5.loc["SMALL LoBM", "alpha_ann_pct"] == pytest.approx(-2.427, abs=5e-3)
    # artifacts written
    assert (out / "tables" / "factor_summary_stats.csv").exists()
    assert (out / "tables" / "grs_test.csv").exists()
    assert (out / "figures" / "factor_cumulative.png").exists()
    assert (out / "tearsheet.md").exists()
    # CSV round-trip matches the in-memory frame
    disk = pd.read_csv(out / "tables" / "regression_ff5.csv", index_col=0)
    assert disk.loc["SMALL LoBM", "alpha_ann_pct"] == pytest.approx(
        reg5.loc["SMALL LoBM", "alpha_ann_pct"], abs=1e-3)
