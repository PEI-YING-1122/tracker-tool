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
