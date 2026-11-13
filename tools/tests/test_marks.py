"""Drawing candidates, with the paid call faked."""
import io
import pathlib
import sys
from types import SimpleNamespace

import pytest
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import images  # noqa: E402


def draw(tmp_path, monkeypatch, model):
    monkeypatch.setattr(images, "WORK", tmp_path)
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    monkeypatch.setattr(images, "briefs", lambda: {
        "styles": {"workshop": {"brief": "a draft"}},
        "projects": {"thing": {"subject": "s", "alt": {"drive": "d"}}}})

    def fake_call(model, prompt, refs=(), timeout=240):
        buf = io.BytesIO()
        Image.new("RGB", (1280, 720), "white").save(buf, "PNG")
        return [buf.getvalue()], 0.14, ""
    monkeypatch.setattr(images, "call", fake_call)
    images.cmd_marks(SimpleNamespace(slugs=["thing"], styles=["workshop"], all_styles=False,
                                     alt="drive", n=1, budget=1.0, snap=False, force=False,
                                     model=model))
    return sorted(p.name for p in (tmp_path / "thing").glob("*.png") if ".raw" not in p.name)


def test_another_models_drawings_sit_beside_the_default_models(tmp_path, monkeypatch):
    assert draw(tmp_path, monkeypatch, images.DEFAULT_MODEL) == ["workshop-drive-1.png"]
    assert draw(tmp_path, monkeypatch, "google/gemini-3-pro-image") == [
        "workshop-drive-1.png", "workshop-drive-gemini-1.png"]


def test_marks_exits_before_calling_when_the_key_is_not_in_the_environment(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(images, "WORK", tmp_path)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setattr(images, "call", lambda *a, **k: calls.append(a))
    with pytest.raises(SystemExit) as e:
        images.cmd_marks(SimpleNamespace(slugs=["thing"], styles=["workshop"], all_styles=False,
                                         alt="drive", n=1, budget=1.0, snap=False, force=False,
                                         model=images.DEFAULT_MODEL))
    assert str(e.value) == "OPENROUTER_API_KEY is not set in the environment"
    assert calls == []
