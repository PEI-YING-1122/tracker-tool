"""Measure True/False refcount drift per MainWindow lifecycle step on this platform."""
import gc
import sys
import tempfile
from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from tracker_tool_gui.main_window import MainWindow
from tracker_tool_gui.preferences import Preferences
from tracker_tool_gui.selection import SourceSection, TargetSection
from tracker_tool_gui.widgets import PathField, ResultPanel, ShotFields

app = QApplication([])
tmp = Path(tempfile.mkdtemp())


def drift(name, action, n=200):
    gc.collect()
    t0, f0 = sys.getrefcount(True), sys.getrefcount(False)
    for i in range(n):
        action(i)
        app.processEvents()
    gc.collect()
    print(f"{name:45s} dTrue={sys.getrefcount(True) - t0:+6d} dFalse={sys.getrefcount(False) - f0:+6d}  (n={n})", flush=True)


def prefs():
    return Preferences(QSettings(str(tmp / "p.ini"), QSettings.Format.IniFormat))


drift("ShotFields create/delete", lambda i: ShotFields().deleteLater())
drift("PathField create/delete", lambda i: PathField("x").deleteLater())
drift("ResultPanel create/delete", lambda i: ResultPanel().deleteLater())
drift("SourceSection create/delete", lambda i: SourceSection().deleteLater())
drift("TargetSection create/delete", lambda i: TargetSection().deleteLater())
drift("MainWindow create/close/delete", lambda i: (lambda w: (w.close(), w.deleteLater()))(MainWindow(preferences=prefs())), n=50)

w = MainWindow(preferences=prefs())
drift("select source (combo index)", lambda i: w.source.software.setCurrentIndex(1 + i % 3))
drift("toggle source-set radio", lambda i: (w.source.software.setCurrentIndex(2), (w.source.source_set_mode if i % 2 else w.source.single_file_mode).setChecked(True)))
drift("target.set_source", lambda i: w.target.set_source(("3DE_R5", "PFTRACK_2017", "SYNTHEYES_2304")[i % 3]))
drift("can_convert", lambda i: w.can_convert())
drift("isVisibleTo", lambda i: w.source.role.isVisibleTo(w.source))
drift("item_enabled", lambda i: w.target.item_enabled("3DE_R5"))
drift("result_panel.show_failure", lambda i: w.result_panel.show_failure("X", "y", details="z", diagnostics="d"))
drift("result_panel.show_success", lambda i: w.result_panel.show_success("o", diagnostics="d"))
drift("_on_busy_changed True/False", lambda i: w._on_busy_changed(i % 2 == 0))
