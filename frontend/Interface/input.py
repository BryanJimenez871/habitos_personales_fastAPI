import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QTextEdit, QLineEdit, QLabel, QListWidget, QMessageBox, QDialog, )

from frontend.exceptions.custom_exceptions import HabitException

from frontend import Interface


class AddHabitDialog(QDialog):

    def __init__(self, view_habits, pie_chart):
        super().__init__()
        ruta_icono_menu = os.path.join(os.path.dirname(__file__), '..', 'Icons', 'add_new_habit.png')
        self.setWindowIcon(QIcon(ruta_icono_menu))
        self.setWindowTitle('Agregar hábito')
        self.setFixedSize(600, 200)
        self.view_habits = view_habits
        self.pie_chart = pie_chart
        self.save_habit_table_button = Interface.SaveHabitTableButton(self)
        self.save_habit_table_button.added_habit_description.connect(self.view_habits.new_habit)
        self.save_habit_table_button.number_of_habit_charts.connect(self.pie_chart.update_chart)

        self.name_habit_label = QLabel('Ingresa un hábito\n'
                                            '[50 caracteres máx]')
        self.description_label = QLabel('Ingresa una descripción\n'
                                           '[100 caracteres máx]') # mejor ajustar
        self.type_habit_label = QLabel('¿Es bueno o malo el hábito?')

        #Input Habit
        self.new_habit_text = QLineEdit()
        self.new_habit_text.setPlaceholderText('Estudiar')
        self.new_habit_text.setMaxLength(50)

        #Input Description
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Estudiaré todos los días miércoles a las 4 pm.")

        #Input Type Habit
        self.type_habit_list = QListWidget()
        self.type_habit_list.addItems(['Es bueno', 'Es malo'])
        self.type_habit_list.setCurrentRow(0)

        new_habit_layout = QVBoxLayout()
        new_habit_layout.addWidget(self.name_habit_label)
        new_habit_layout.addWidget(self.new_habit_text)
        new_habit_layout.addWidget(self.save_habit_table_button)
        new_habit_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        description_layout = QVBoxLayout()
        description_layout.addWidget(self.description_label)
        description_layout.addWidget(self.description_text)

        habit_type_layout = QVBoxLayout()
        habit_type_layout.addWidget(self.type_habit_label)
        habit_type_layout.addWidget(self.type_habit_list)

        main_layout = QHBoxLayout()
        main_layout.addLayout(new_habit_layout)
        main_layout.addLayout(description_layout)
        main_layout.addLayout(habit_type_layout)
        self.setLayout(main_layout)

    def get_habit(self):
        habit = self.new_habit_text.text()
        try:
            if habit:
                first_character = habit[0].upper()
                habit = first_character + habit[1:].lower()
                return habit
            else:
                raise HabitException('Debes ingresar un hábito.')

        except HabitException as e:
            Interface.ShowMessage(QMessageBox.Icon.Critical, 'Crítico', str(e))

    def get_description(self):
        description = self.description_text.toPlainText()
        return description

    def get_habit_type(self):
        type_habit = self.type_habit_list.currentItem()
        return type_habit.text()
#
class DailyHabitInput(QWidget):
    def __init__(self):
        super().__init__()

        daily_habit_label = QLabel('¿Qué habito hiciste hoy? 😎')
        complet_label = QLabel('¿Completaste el habito?')

        self.habit_text = QLineEdit()

        self.complet = QListWidget()
        self.complet.addItems(['Si', 'No'])
        self.complet.setCurrentRow(0)

        habit_layout = QVBoxLayout()
        habit_layout.addWidget(daily_habit_label)
        habit_layout.addWidget(self.habit_text)
        habit_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        complet_layout = QVBoxLayout()
        complet_layout.addWidget(complet_label)
        complet_layout.addWidget(self.complet)


        main_layout = QHBoxLayout()
        main_layout.addLayout(habit_layout)
        main_layout.addLayout(complet_layout)

        self.setLayout(main_layout)

    def set_habit(self, habito):
        self.habit_text.setText(habito)

    def get_daily_habit(self):
        return self.habit_text.text()

    def get_complet(self):
        item = self.complet.currentRow()
        if item == 0:
            return True
        elif item == 1:
            return False
        return True
