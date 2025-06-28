from PyQt5.QtWidgets import QMenu

def attach_dropdown_to_edit_action(parent, toolbar, edit_action):
    edit_dropdown_menu = QMenu(parent)

    # Connect "Birthdata" to parent.open_birthdata_editor
    edit_dropdown_menu.addAction("Birthdata", parent.open_birthdata_editor)
    edit_dropdown_menu.addAction("Change timezone", lambda: print("Change timezone clicked"))
    edit_dropdown_menu.addAction("User defined special point", lambda: print("Special point clicked"))
    edit_dropdown_menu.addAction("Planetary Special Lagnas (research)", lambda: print("Special Lagnas clicked"))
    edit_dropdown_menu.addSeparator()
    edit_dropdown_menu.addAction("Chart notes (in notepad)", lambda: print("Notes clicked"))
    edit_dropdown_menu.addSeparator()
    edit_dropdown_menu.addAction("Copy basic calculations", lambda: print("Copy basic clicked"))
    edit_dropdown_menu.addAction("Copy complete calculations", lambda: print("Copy complete clicked"))

    def show_dropdown_menu():
        widget = toolbar.widgetForAction(edit_action)
        pos = widget.mapToGlobal(widget.rect().bottomLeft())
        edit_dropdown_menu.exec_(pos)

    edit_action.triggered.connect(show_dropdown_menu)
