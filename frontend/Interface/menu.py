import os

from PySide6.QtGui import QAction, Qt, QIcon
from PySide6.QtWidgets import QMessageBox, QMenu


class ContextMenuManager:
    def __init__(self, table, clicked_column, delete):
        self.table = table
        self.clicked_column = clicked_column
        self.delete = delete

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_menu_manager)

    def show_menu_manager(self, position):
        delete_icon_path = os.path.join(os.path.dirname(__file__), '..', 'Icons', 'delete.png')

        column = self.table.columnAt(position.x())
        row = self.table.rowAt(position.y())

        if row < 0 or column != self.clicked_column:
            return

        menu = QMenu(self.table)

        delete_action = QAction(QIcon(delete_icon_path),'Eliminar', self.table)
        delete_action.triggered.connect(lambda:self.confirm_and_delete(row))
        menu.addAction(delete_action)

        menu.exec(self.table.mapToGlobal(position))

    def confirm_and_delete(self, fila):
        confirm_msg = QMessageBox()
        confirm_msg.setIcon(QMessageBox.Icon.Warning)
        confirm_msg.setWindowTitle('Confirmar eliminación')
        confirm_msg.setText('¿Estás seguro que deseas eliminar este elemento?')
        confirm_msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirm_msg.setDefaultButton(QMessageBox.StandardButton.No)

        if confirm_msg.exec() == QMessageBox.StandardButton.Yes:
            self.delete(fila)

