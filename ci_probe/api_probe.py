"""Find PySide6 calls that leak or underflow the refcount of True/False."""
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QFormLayout, QLineEdit, QRadioButton, QWidget,
)

app = QApplication.instance() or QApplication([])
w = QWidget()
form = QFormLayout(w)
edit = QLineEdit(w)
form.addRow("x", edit)
combo = QComboBox(w)
combo.addItem("a", None)
combo.addItem("b", "B")
radio = QRadioButton("r", w)
radio2 = QRadioButton("r2", w)
group = QButtonGroup(w)
group.addButton(radio)
group.addButton(radio2)
item = combo.model().item(1)

N = 10000
CASES = {
    "QStandardItem.isEnabled": lambda: item.isEnabled(),
    "QStandardItem.setEnabled(True)": lambda: item.setEnabled(True),
    "QAbstractButton.isChecked": lambda: radio.isChecked(),
    "QAbstractButton.setChecked(True)": lambda: radio.setChecked(True),
    "QWidget.isVisibleTo": lambda: edit.isVisibleTo(w),
    "QWidget.isEnabled": lambda: edit.isEnabled(),
    "QFormLayout.setRowVisible(widget, True)": lambda: form.setRowVisible(edit, True),
    "QFormLayout.setRowVisible(widget, False)": lambda: form.setRowVisible(edit, False),
    "QComboBox.setItemData(None, ToolTip)": lambda: combo.setItemData(1, None, Qt.ItemDataRole.ToolTipRole),
    "QComboBox.itemData(ToolTip)": lambda: combo.itemData(1, Qt.ItemDataRole.ToolTipRole),
    "QComboBox.currentData": lambda: combo.currentData(),
    "QLineEdit.hasAcceptableInput": lambda: edit.hasAcceptableInput(),
}

for name, call in CASES.items():
    t0, f0 = sys.getrefcount(True), sys.getrefcount(False)
    for _ in range(N):
        call()
    dt, df = sys.getrefcount(True) - t0, sys.getrefcount(False) - f0
    flag = "  <-- REFCOUNT DRIFT" if abs(dt) > 50 or abs(df) > 50 else ""
    print(f"{name:42s} dTrue={dt:+7d} dFalse={df:+7d}{flag}")
