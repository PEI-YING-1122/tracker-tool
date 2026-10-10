"""Measure True/False refcount drift of one PySide6 operation (argv[1]) in its own process."""
import gc
import sys

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QRadioButton, QWidget

app = QApplication([])
parent = QWidget()


class PySub(QWidget):
    pass


class Emitter(QObject):
    changed = Signal()


radio = QRadioButton("r", parent)
emitter = Emitter()
sub_shown = PySub(parent)
plain_shown = QWidget(parent)
label = QLabel("x", parent)

CASES = {
    "new_plain_qwidget_show": lambda: QWidget(parent).show(),
    "new_pysub_show": lambda: PySub(parent).show(),
    "new_pysub_hide": lambda: PySub(parent).hide(),
    "pysub_show_repeat": lambda: sub_shown.show(),
    "pysub_hide_show": lambda: (sub_shown.hide(), sub_shown.show()),
    "plain_hide_show": lambda: (plain_shown.hide(), plain_shown.show()),
    "label_hide_show": lambda: (label.hide(), label.show()),
    "pysub_setVisible_true": lambda: sub_shown.setVisible(True),
    "radio_setChecked_true": lambda: radio.setChecked(True),
    "radio_isChecked": lambda: radio.isChecked(),
    "signal_emit_noarg": lambda: emitter.changed.emit(),
    "new_qcombobox": lambda: QComboBox(parent),
}

case = sys.argv[1]
N = 500
gc.collect()
t0, f0 = sys.getrefcount(True), sys.getrefcount(False)
for _ in range(N):
    CASES[case]()
    app.processEvents()
gc.collect()
dt, df = sys.getrefcount(True) - t0, sys.getrefcount(False) - f0
flag = "  <-- NEGATIVE" if min(dt, df) < -10 else ""
print(f"{case:28s} dTrue={dt:+6d} dFalse={df:+6d} (n={N}){flag}", flush=True)
