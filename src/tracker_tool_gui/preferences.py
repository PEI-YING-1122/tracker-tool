from pathlib import Path

from PySide6.QtCore import QByteArray, QSettings


ORGANIZATION = "TrackerTool"
APPLICATION = "TrackerToolGUI"

DIRECTORY_KINDS = ("input", "output")

# Only GUI conveniences are persisted. Shot metadata (resolution, frame
# range) and software choices are never stored: reusing one shot's values
# on another shot would be a silent geometry or frame error.
_DIRECTORY_KEY = "directories/{kind}"
_WINDOW_GEOMETRY_KEY = "window/geometry"

PERSISTED_KEYS = frozenset(
    [_DIRECTORY_KEY.format(kind=kind) for kind in DIRECTORY_KINDS]
    + [_WINDOW_GEOMETRY_KEY]
)


class Preferences:
    def __init__(self, settings=None):
        self._settings = settings or QSettings(ORGANIZATION, APPLICATION)

    @staticmethod
    def _directory_key(kind: str) -> str:
        if kind not in DIRECTORY_KINDS:
            raise ValueError(f"Unknown directory kind: {kind}")

        return _DIRECTORY_KEY.format(kind=kind)

    def directory(self, kind: str) -> str:
        value = self._settings.value(self._directory_key(kind), "")
        return value if isinstance(value, str) else ""

    def remember_file(self, kind: str, file_path: str) -> None:
        if not file_path:
            return

        self._settings.setValue(
            self._directory_key(kind),
            str(Path(file_path).parent),
        )

    def window_geometry(self) -> QByteArray | None:
        value = self._settings.value(_WINDOW_GEOMETRY_KEY)
        return value if isinstance(value, QByteArray) else None

    def save_window_geometry(self, geometry: QByteArray) -> None:
        self._settings.setValue(_WINDOW_GEOMETRY_KEY, geometry)

    def sync(self) -> None:
        self._settings.sync()
