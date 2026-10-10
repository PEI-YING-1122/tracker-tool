import pytest

try:
    from PySide6.QtCore import QSettings
except ImportError:  # GUI tests are skipped without PySide6.
    QSettings = None


@pytest.fixture
def ini_settings(tmp_path):
    return QSettings(
        str(tmp_path / "preferences.ini"),
        QSettings.Format.IniFormat,
    )


@pytest.fixture(autouse=True)
def isolated_preferences(request, monkeypatch, tmp_path):
    # Never let tests read or write the user's real preferences (the
    # Windows registry with the default QSettings).
    if QSettings is None:
        return

    import tracker_tool_gui.main_window as main_window
    from tracker_tool_gui.preferences import Preferences

    def preferences():
        return Preferences(
            QSettings(
                str(tmp_path / "default-preferences.ini"),
                QSettings.Format.IniFormat,
            )
        )

    monkeypatch.setattr(main_window, "Preferences", preferences)


@pytest.fixture(autouse=True)
def no_real_dialogs_or_shell(monkeypatch):
    # A modal dialog would block a headless test run forever, and opening a
    # folder would launch the file manager. Tests that need these
    # behaviours inject their own callables.
    if QSettings is None:
        return

    import tracker_tool_gui.main_window as main_window
    import tracker_tool_gui.widgets as widgets

    def unexpected_overwrite_dialog(parent, output_path):
        pytest.fail(f"unexpected overwrite dialog for {output_path}")

    def unexpected_open_folder(folder):
        pytest.fail(f"unexpected request to open {folder}")

    monkeypatch.setattr(main_window, "_ask_overwrite", unexpected_overwrite_dialog)
    monkeypatch.setattr(widgets, "_open_folder", unexpected_open_folder)
