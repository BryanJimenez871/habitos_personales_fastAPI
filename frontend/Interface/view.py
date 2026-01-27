from datetime import datetime
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
                               QAbstractItemView, QLabel, QMessageBox)
from .menu import ContextMenuManager
from fastapi import HTTPException

import requests

class HabitView(QWidget):
    API_URL_HABIT = "http://127.0.0.1:8000/habits/"
    API_URL_DAILY = "http://127.0.0.1:8000/daily_habits/"

    selected_habit = Signal(str)
    deleted_habit= Signal(int)
    number_habit_pie_chart = Signal()
    def __init__(self, main_window, pie_chart):
        super().__init__()

        response = requests.get(self.API_URL_HABIT)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code)
        self.show_habits = response.json()

        self.main_window = main_window
        self.main_window.delete_all_habits_signal.connect(self.delete_all)

        self.pie_chart = pie_chart
        self.number_habit_pie_chart.connect(self.pie_chart.update_chart) 

        self.habits_description = QTableWidget(columnCount=4)
        self.habits_description.setHorizontalHeaderLabels(['Id', 'Hábitos', 'Tipo de Hábito', 'Descripción'])
        self.habits_description.verticalHeader().setVisible(False)
        self.habits_description.setColumnHidden(0, True) 
        self.habits_description.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.habits_description.resizeColumnToContents(3)
        encabezado = self.habits_description.horizontalHeader()
        encabezado.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        encabezado.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        encabezado.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.habits_description.itemClicked.connect(self.select_habit) 

        self.menu_contextual = ContextMenuManager(
            table= self.habits_description,
            clicked_column= 1, 
            delete= self.delete_habit)

        ModifyTable(self.habits_description)
        self.view_table()

        title_label = QLabel('Tabla de Hábitos')
        font = QFont('Calibri', 15)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setContentsMargins(0, 0, 50, 0)
        title_label.setStyleSheet("color: #5555FF;")
        show_habits_layout = QVBoxLayout()
        show_habits_layout.addWidget(title_label)
        show_habits_layout.addWidget(self.habits_description)
        self.setLayout(show_habits_layout)

    def view_table(self):
        for habit in self.show_habits:
            habits_dictionary = {
                'habit_id': habit["habit_id"],
                'habit_name': habit["habit_name"],
                'habit_type': habit["habit_type"],
                'description': habit["description"],
            }
            self.insert_row_habit_table(habits_dictionary)

    def new_habit(self, habit_id, habit_name, habit_type, description):
        new_description_habit = {
            'habit_id': habit_id,
            'habit_name': habit_name,
            'habit_type': habit_type,
            'description': description,
        }
        self.insert_row_habit_table(new_description_habit)

        habit_dict = {
            "habit_id": habit_id,
            "habit_name": habit_name,
            "habit_type": habit_type,
            "description": description
        }

        self.show_habits.append(habit_dict)

    def insert_row_habit_table(self, dictionary):
        row = self.habits_description.rowCount()
        self.habits_description.insertRow(row)

        item_id = QTableWidgetItem(str(dictionary['habit_id']))
        self.habits_description.setItem(row, 0, item_id)

        if dictionary['habit_type'] == 'Es bueno':
            f = ModifyItem.align_item
        else:
            f = ModifyItem.bad_color_habit

        self.habits_description.setItem(row, 1, f(dictionary, 'habit_name'))
        self.habits_description.setItem(row, 2, f(dictionary, 'habit_type'))
        self.habits_description.setItem(row, 3, f(dictionary, 'description'))

    def select_habit(self, item):
        habits_column = 1
        if item.column() == habits_column:
            habit_text = item.text()
            self.selected_habit.emit(habit_text)
    #
    def delete_habit(self, row):
        habit_id = int(self.habits_description.item(row, 0).text())
        response_daily_habit = requests.delete(f'{self.API_URL_DAILY}habit_id_deleted/{habit_id}') #aqui se borra por parte de la tabla registro porque tiene el foreing key con habito
        if response_daily_habit.status_code != 204:
            QMessageBox.warning(self, "Error al eliminar habito", response_daily_habit.text)
            return

        response_habit = requests.delete(f'{self.API_URL_HABIT}habit_id_deleted/{habit_id}') # ahi recien borro el id_habito de la tabla habito
        if response_habit.status_code != 204:
            QMessageBox.warning(self, "Error al eliminar habito", response_habit.text)
            return
        self.habits_description.removeRow(row)
        self.deleted_habit.emit(habit_id)
        self.number_habit_pie_chart.emit()

    def delete_all(self):
        self.habits_description.clearContents()
        self.habits_description.setRowCount(0)
        self.number_habit_pie_chart.emit()

    def get_habits_type(self):
        type_habit_list = []
        for habit in self.show_habits:
            habits_dictionary = {
                habit['habit_name']: habit['habit_type']
            }
            type_habit_list.append(habits_dictionary)
        return type_habit_list

class DailyView(QWidget):
    API_URL_DAILY = "http://127.0.0.1:8000/daily_habits/"
    API_URL_DATE = "http://127.0.0.1:8000/dates/"

    number_daily_habit = Signal()
    def __init__(self, main_window, view_habits, daily_pie_chart):
        super().__init__()

        response = requests.get(self.API_URL_DAILY)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code)

        self.show_habits = response.json()

        self.view_habits = view_habits
        self.view_habits.deleted_habit.connect(self.delete_habits)

        self.main_window = main_window
        self.main_window.delete_all_dailys.connect(self.delete_all)

        self.daily_pie_chart = daily_pie_chart
        self.number_daily_habit.connect(self.daily_pie_chart.update_pie_chart)

        self.daily_habits = QTableWidget(columnCount=7)
        self.daily_habits.setHorizontalHeaderLabels(['Id_registro', 'Id_hábito', 'Hábito', 'Tipo hábito', 'Id_fecha', 'Fecha', 'Completado'])
        self.daily_habits.verticalHeader().setVisible(False)
        self.daily_habits.setColumnHidden(0, True)
        self.daily_habits.setColumnHidden(1, True)
        self.daily_habits.setColumnHidden(4, True)
        self.daily_habits.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.menu_manager = ContextMenuManager(
            table=self.daily_habits,
            clicked_column=2,
            delete=self.delete_daily_habit)

        ModifyTable(self.daily_habits)
        self.view_table()

        head = self.daily_habits.horizontalHeader()
        head.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        head.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        head.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        tittle_label = QLabel('Tabla de Registros')
        font = QFont('Calibri', 15)
        font.setBold(True)
        tittle_label.setFont(font)
        tittle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tittle_label.setStyleSheet("color: #E33D3D;")
        tittle_label.setContentsMargins(0, 0, 50, 0)

        show_habits_layout = QVBoxLayout()
        show_habits_layout.addWidget(tittle_label)
        show_habits_layout.addWidget(self.daily_habits)
        self.setLayout(show_habits_layout)

    def view_table(self):

        for daily_habit in self.show_habits:
            date = datetime.strptime(daily_habit['date']['habit_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            daily_habit_dictionary = {
                'daily_id': daily_habit['daily_id'],
                'habit_id': daily_habit['habit']['habit_id'],
                'habit_name': daily_habit['habit']['habit_name'],
                'habit_type': daily_habit['habit']['habit_type'],
                'date_id': daily_habit['date']['date_id'],
                'habit_date': date,
                'complet': daily_habit['complet']
            }
            value = daily_habit_dictionary['habit_type']
            self.insert_row_join_table(daily_habit_dictionary, value)

    def add_daily_habit(self, daily_id, habit_id, habit_name, date_id, habit_date, complet):

        new_daily_habit = {
            'daily_id': daily_id,
            'habit_id': habit_id,
            'habit_name': habit_name,
            'habit_type': None,
            'date_id': date_id,
            'habit_date': habit_date,
            'complet': complet
        }

        type_habit_list = self.view_habits.get_habits_type()

        for habit_type in type_habit_list:
            for key, value in habit_type.items():
                if key == habit_name:
                    new_daily_habit['habit_type'] = value
                    self.insert_row_join_table(new_daily_habit, value)
                    return

    def insert_row_join_table(self, dictionary, value):
        row = self.daily_habits.rowCount()
        self.daily_habits.insertRow(row)

        item_daily_id = QTableWidgetItem(str(dictionary['daily_id']))
        self.daily_habits.setItem(row, 0, item_daily_id)

        if value == 'Es bueno':
            f = ModifyItem.align_item
        else:
            f = ModifyItem.bad_color_habit

        self.daily_habits.setItem(row, 1, f(dictionary, 'habit_id'))
        self.daily_habits.setItem(row, 2, f(dictionary, 'habit_name'))
        self.daily_habits.setItem(row, 3, f(dictionary, 'habit_type'))
        self.daily_habits.setItem(row, 4, f(dictionary, 'date_id'))
        self.daily_habits.setItem(row, 5, f(dictionary, 'habit_date'))
        self.daily_habits.setItem(row, 6, ModifyItem.icon_complet(dictionary, 'complet'))

    def delete_daily_habit(self, fila):
        daily_id = int(self.daily_habits.item(fila, 0).text())
        date_id = int(self.daily_habits.item(fila, 4).text())

        response_daily_habit = requests.delete(f'{self.API_URL_DAILY}daily_id_deleted/{daily_id}')
        if response_daily_habit.status_code != 204:
            QMessageBox.warning(self, "Error al eliminar registro", response_daily_habit.text)
            return

        total = 0
        row_number = self.daily_habits.rowCount()

        for f in range(row_number):
            item = self.daily_habits.item(f, 4)
            if date_id == item.text():
                total += 1

        if total == 1:
            response_date_id = requests.delete(f'{self.API_URL_DATE}date_id_deleted{date_id}')
            if response_date_id.status_code != 204:
                QMessageBox.warning(self, "Error al eliminar la fecha", response_date_id.text)
                return

        self.daily_habits.removeRow(fila)
        self.number_daily_habit.emit()
#
    def delete_habits(self, habit_id):
        column_id = 1
        rows = self.daily_habits.rowCount()

        delete_rows = []

        for row in range(rows):
            item = self.daily_habits.item(row, column_id)
            if item.text() == str(habit_id):
                delete_rows.append(row)

        for row in reversed(delete_rows):
            self.daily_habits.removeRow(row)
        self.number_daily_habit.emit()

    def delete_all(self):
        self.daily_habits.clearContents()
        self.daily_habits.setRowCount(0)
        self.number_daily_habit.emit()

class ModifyTable:
    def __init__(self, table):
        self.table = table
        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {"
            "background-color: #2D492F;"
            "color: black;"
            "font-family: 'Calibri';"
            "font-size: 11pt;"
            "padding: 4px;"
            "font-weight: bold;"
            "}")

class ModifyItem:
    @staticmethod
    def align_item(dictionary, text):
        value = str(dictionary[text])
        item = QTableWidgetItem(value)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#527D55"))
        item.setForeground(QColor("black"))
        item.setFont(QFont('Calibri', 12))
        return item

    @staticmethod
    def icon_complet(dictionary, text):
        value = str(dictionary[text])
        if str(value) == 'True':
            final_text = '✔'
        else:
            final_text = '✖︎︎'

        item = QTableWidgetItem(final_text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#527D55"))
        item.setForeground(QColor("black"))
        item.setFont(QFont('Calibri', 15))
        return item

    @staticmethod
    def bad_color_habit(dictionary, text):
        value = str(dictionary[text])
        item = QTableWidgetItem(value)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#D93030"))
        item.setForeground(QColor("black"))
        item.setFont(QFont('Calibri', 12))
        return item
