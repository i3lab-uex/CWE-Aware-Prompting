from cwe_experiment.progress import ConsoleProgress


def test_console_progress_reports_stages_to_stderr(capsys) -> None:
    progress = ConsoleProgress()

    progress.message("config", "modelo=fake")
    progress.update("generation", 1, 2, "último=ok", force=True)
    progress.update("generation", 2, 2, "último=ok")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "modelo=fake" in captured.err
    assert "1/2 ( 50%)" in captured.err
    assert "2/2 (100%)" in captured.err
