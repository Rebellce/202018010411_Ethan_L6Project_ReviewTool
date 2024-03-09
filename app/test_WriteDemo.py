import pytest
from .WriteDemo import TextEditor, Qt, QFont

def test_set_bold(qtbot):
    window = TextEditor()
    qtbot.addWidget(window)

    # Simulate the bold action
    qtbot.mouseClick(window.toolbar.actions()[0], Qt.LeftButton)

    # Assert the text edit is now bold
    assert window.text_edit.fontWeight() == QFont.Bold
