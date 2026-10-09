from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal


class _TaskSignals(QObject):
    succeeded = Signal(object)
    failed = Signal(object)


class _Task(QRunnable):
    def __init__(self, function, signals):
        super().__init__()

        self._function = function
        self._signals = signals

    def run(self):
        try:
            result = self._function()
        except Exception as exc:  # noqa: BLE001
            # The exception is handed over unchanged. Classifying it is a
            # Core responsibility, not the worker's.
            self._signals.failed.emit(exc)
        else:
            self._signals.succeeded.emit(result)


class TaskRunner(QObject):
    """Run one task at a time off the GUI thread.

    Signals are delivered on the thread that owns the runner (the GUI
    thread). busy_changed(False) is emitted before succeeded / failed, so
    result handlers see the runner as idle.
    """

    busy_changed = Signal(bool)
    succeeded = Signal(object)
    failed = Signal(object)

    def __init__(self, parent=None, thread_pool=None):
        super().__init__(parent)

        self._thread_pool = thread_pool or QThreadPool.globalInstance()
        self._signals = None

    @property
    def busy(self) -> bool:
        return self._signals is not None

    def start(self, function) -> None:
        if self.busy:
            raise RuntimeError("A task is already running")

        signals = _TaskSignals(self)
        signals.succeeded.connect(self._on_succeeded)
        signals.failed.connect(self._on_failed)

        self._signals = signals
        self.busy_changed.emit(True)

        self._thread_pool.start(_Task(function, signals))

    def _finish(self) -> None:
        self._signals.deleteLater()
        self._signals = None
        self.busy_changed.emit(False)

    def _on_succeeded(self, result) -> None:
        self._finish()
        self.succeeded.emit(result)

    def _on_failed(self, exc) -> None:
        self._finish()
        self.failed.emit(exc)
