import os
import requests
import Interface

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (QHBoxLayout, QWidget, QMainWindow, QVBoxLayout, QFrame, QMessageBox,
    QTabWidget)


class MainWindow(QMainWindow):
    API_URL_DATE = "http://127.0.0.1:8000/dates/"
    API_URL_DAILY = "http://127.0.0.1:8000/daily_habits/"
    API_URL_HABIT = "http://127.0.0.1:8000/habits/"

    delete_all_dailys = Signal()
    delete_all_habits_signal = Signal()
    def __init__(self):
        super().__init__()
        window_icon_path = os.path.join(os.path.dirname(__file__), '..', 'Icons', 'personal_habit.png')
        menu_icon_path = os.path.join(os.path.dirname(__file__), '..', 'Icons', 'add_new_habit.png')
        delete_icon_path = os.path.join(os.path.dirname(__file__), '..', 'Icons', 'delete.png')
        delete_all_icon_path = os.path.join(os.path.dirname(__file__), '..', 'Icons', 'delete_all_habits.png')
        self.precaution_icon_path = os.path.join(os.path.dirname(__file__), '..', 'Icons', 'precaution.png')

        self.setWindowTitle('Habitos Personales')
        self.setWindowIcon(QIcon(window_icon_path))
        self.resize(1200,800)
        self.graphs = Interface.GridGraphs()
        self.input_daily_habit = Interface.DailyHabitInput()
        self.calendar = Interface.Calendar()
        self.view_habit = Interface.HabitView(self, self.graphs.numbers_habit_pie_chart)
        self.view_daily = Interface.DailyView(self, self.view_habit, self.graphs.daily_pie_chart)
        self.save_daily_habit_button = Interface.SaveDailyHabitButton(self.input_daily_habit, self.calendar)
        self.save_daily_habit_button.added_habit_record.connect(self.view_daily.add_daily_habit)
        self.save_daily_habit_button.number_of_records_charts.connect(self.graphs.daily_pie_chart.update_pie_chart)
        self.view_habit.selected_habit.connect(self.input_daily_habit.set_habit)
        self.input_daily_habit.layout().setContentsMargins(0, 0, 0, 0)

        self.calendar.layout().setContentsMargins(0, 0, 0, 0)
        new_habit_action = QAction(QIcon(menu_icon_path), 'Agregar hábito', self)
        new_habit_action.triggered.connect(self.open_habit_dialog)

        delete_all_dailys_action = QAction(QIcon(delete_icon_path), 'Eliminar todos los registros', self)
        delete_all_dailys_action.triggered.connect(self.delete_all_daily_habits)

        delete_all_habits_action = QAction(QIcon(delete_all_icon_path),'Eliminar todos los los hábitos', self)
        delete_all_habits_action.triggered.connect(self.delete_all_habits)

        self.tabs = QTabWidget()

        # Crear menu
        menu = self.menuBar()
        ModifyMenu(menu)
        habit_menu = menu.addMenu('Nuevo hábito')
        habit_menu.addAction(new_habit_action)
        habit_menu.addAction(delete_all_dailys_action)
        habit_menu.addAction(delete_all_habits_action)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Plain)

        # Habits table layout
        habits_table_layout = QVBoxLayout()
        habits_table_layout.addWidget(self.view_habit)
        # ---

        # Daily habits table layout
        daily_habit_layout = QVBoxLayout()
        daily_habit_layout.addWidget(self.view_daily)
        # ---


        top_layout = QVBoxLayout()
        top_layout.addLayout(habits_table_layout,1)
        top_layout.addWidget(line)
        top_layout.addLayout(daily_habit_layout,2)
        # ---

        # # Contenedor bottom
        input_daily_habit_layout = QVBoxLayout()
        input_daily_habit_layout.addWidget(self.input_daily_habit, alignment=Qt.AlignmentFlag.AlignTop)

        calendar_and_botton_layout = QVBoxLayout()
        calendar_and_botton_layout.addWidget(self.calendar)
        calendar_and_botton_layout.addWidget(self.save_daily_habit_button)

        botton_layout = QHBoxLayout()
        botton_layout.addLayout(input_daily_habit_layout)
        botton_layout.addLayout(calendar_and_botton_layout)
        botton_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout,5)
        main_layout.addLayout(botton_layout,1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.tabs.addTab(central_widget, "Hábitos Personales")
        self.tabs.addTab(self.graphs, "Graficos")
        self.setCentralWidget(self.tabs)

    def open_habit_dialog(self):
        pie_chart = self.graphs.numbers_habit_pie_chart
        dialogo = Interface.AddHabitDialog(self.view_habit, pie_chart)
        dialogo.exec()

    def delete_all_daily_habits(self):
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(self.precaution_icon_path))
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Eliminar todos los registros habitos")
        msg_box.setText("¿Estás seguro de eliminar todos los registros habitos?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            response_daily_habit = requests.delete(self.API_URL_DAILY)
            if response_daily_habit.status_code != 204:
                QMessageBox.warning(self, "Error al eliminar registro", response_daily_habit.text)
                return

            response_date_habit = requests.delete(self.API_URL_DATE)
            if response_date_habit.status_code != 204:
                QMessageBox.warning(self, "Error al eliminar la fecha", response_date_habit.text)
                return

            self.delete_all_dailys.emit()

    def delete_all_habits(self):
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(self.precaution_icon_path))
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Eliminar todos los habitos")
        msg_box.setText("¿Estás seguro de eliminar todos los hábitos?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        if msg_box.exec() == QMessageBox.StandardButton.Yes:

            response_daily_habit = requests.delete(self.API_URL_DAILY)
            if response_daily_habit.status_code != 204:
                QMessageBox.warning(self, "Error al eliminar registro", response_daily_habit.text)
                return

            response_habit = requests.delete(self.API_URL_HABIT)
            if response_habit.status_code != 204:
                QMessageBox.warning(self, "Error al eliminar registro", response_habit.text)
                return

            response_date_habit = requests.delete(self.API_URL_DATE)
            if response_date_habit.status_code != 204:
                QMessageBox.warning(self, "Error al eliminar la fecha", response_date_habit.text)
                return

            self.view_daily.delete_all()
            self.delete_all_habits_signal.emit()
#
class ModifyMenu:
    def __init__(self, menu):
        self.menu = menu
        menu.setStyleSheet("""
        QMenuBar {
        background: qlineargradient(
            spread:pad,
            x1:0, y1:0,
            x2:1, y2:0,
            stop:0 #feda75,      /* amarillo */
            stop:0.25 #fa7e1e,   /* naranja */
            stop:0.50 #d62976,   /* rosado fuerte */
            stop:0.75 #962fbf,   /* púrpura */
            stop:1 #4f5bd5       /* azul */
        );
        color: black;
        font-weight: bold;
        font-style: italic;
    }
    QMenuBar::item:selected {
        background: rgba(255,255,255,50);
    }

    QMenu {
        background-color: #2b2b2b;
        color: white;
        font-family: Calibri;
        font-size: 14px;
    }

    QMenu::item:selected {
        background-color: #505050;
    }
    """)
