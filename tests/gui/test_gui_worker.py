import threading

import pytest

pytest.importorskip("PySide6")

from tracker_tool_gui.worker import TaskRunner  # noqa: E402


@pytest.fixture
def runner(qtbot):
    task_runner = TaskRunner()
    yield task_runner
    qtbot.waitUntil(lambda: not task_runner.busy, timeout=5000)


def test_task_result_is_delivered_on_gui_thread(qtbot, runner):
    gui_thread = threading.get_ident()
    task_threads = []
    delivered_threads = []

    def task():
        task_threads.append(threading.get_ident())
        return "converted"

    runner.succeeded.connect(
        lambda result: delivered_threads.append(threading.get_ident())
    )

    with qtbot.waitSignal(runner.succeeded, timeout=5000) as blocker:
        runner.start(task)

    assert blocker.args == ["converted"]
    assert task_threads != [gui_thread]
    assert delivered_threads == [gui_thread]


@pytest.mark.parametrize(
    "exception",
    [
        ValueError("INVALID_SHOT_METADATA"),
        ValueError("descriptive reader message"),
        IndexError("list index out of range"),
        OSError("disk full"),
    ],
)
def test_task_exception_is_delivered_unchanged(qtbot, runner, exception):
    def task():
        raise exception

    with qtbot.waitSignal(runner.failed, timeout=5000) as blocker:
        runner.start(task)

    delivered = blocker.args[0]

    assert delivered is exception
    assert delivered.__traceback__ is not None


def test_busy_state_brackets_the_task(qtbot, runner):
    release = threading.Event()
    busy_changes = []

    runner.busy_changed.connect(busy_changes.append)

    with qtbot.waitSignal(runner.busy_changed, timeout=5000):
        runner.start(lambda: release.wait(5))

    assert runner.busy
    assert busy_changes == [True]

    with qtbot.waitSignal(runner.succeeded, timeout=5000):
        release.set()

    assert not runner.busy
    assert busy_changes == [True, False]


def test_runner_is_idle_when_result_handler_runs(qtbot, runner):
    busy_during_handler = []

    runner.succeeded.connect(
        lambda result: busy_during_handler.append(runner.busy)
    )
    runner.failed.connect(
        lambda exc: busy_during_handler.append(runner.busy)
    )

    with qtbot.waitSignal(runner.succeeded, timeout=5000):
        runner.start(lambda: None)

    def fail():
        raise ValueError("x")

    with qtbot.waitSignal(runner.failed, timeout=5000):
        runner.start(fail)

    assert busy_during_handler == [False, False]


def test_second_task_is_rejected_while_busy(qtbot, runner):
    release = threading.Event()

    runner.start(lambda: release.wait(5))

    with pytest.raises(RuntimeError):
        runner.start(lambda: None)

    with qtbot.waitSignal(runner.succeeded, timeout=5000):
        release.set()


def test_runner_can_start_again_after_completion(qtbot, runner):
    for value in range(3):
        with qtbot.waitSignal(runner.succeeded, timeout=5000) as blocker:
            runner.start(lambda value=value: value)

        assert blocker.args == [value]
