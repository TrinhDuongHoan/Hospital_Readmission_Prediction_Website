from src.orchestration.pipelines.streaming_pipeline import build_streaming_commands
from src.orchestration.pipelines.training_pipeline import run_training_pipeline


def test_build_streaming_commands():
    commands = build_streaming_commands()
    assert len(commands) >= 3
    assert commands[0][0] in {"bash", "python"}


def test_training_pipeline_importable():
    assert run_training_pipeline is not None