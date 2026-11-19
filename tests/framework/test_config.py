"""SK-01: settings load from config, and env/local override works"""

from nv_eval.config import load_settings


def test_settings_load_and_env_override(monkeypatch):
    monkeypatch.setenv("NV_EVAL_ADAPTER", "stub")
    s = load_settings()
    assert s["adapter"]["name"] == "stub"
    assert "answer_relevancy" in s["thresholds"]


def test_both_models_share_one_ollama_address():
    s = load_settings()
    assert s["judge"]["base_url"] == s["adapter"]["rag_demo"]["base_url"]
