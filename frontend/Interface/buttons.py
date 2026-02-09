import os
import datetime

from exceptions.custom_exceptions import HabitException
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QMessageBox
import requests

class SaveHabitTableButton(QWidget):
    API_URL_HABIT = "http://127.0.0.1:8000/habits/"
    added_habit_description = Signal( int,str, str,str)
    number_of_habit_charts = Signal()
    def __init__(self, habit_table_input):
        super().__init__()
        self.habit_table_input = habit_table_input

        save_habits_table_button = QPushButton("Agregar Hábito")
        save_habits_table_button.clicked.connect(self.save_habit_table)

        habit_layout = QHBoxLayout()
        habit_layout.addWidget(save_habits_table_button)
        self.setLayout(habit_layout)

    def save_habit_table(self):
        try:
            response = requests.get(self.API_URL_HABIT)
            if response.status_code != 200:
                raise Exception("Error al obtener hábitos")

            habits_table = response.json()
            habit_name = self.habit_table_input.get_habit()
            description = self.habit_table_input.get_description()
            habit_type = self.habit_table_input.get_habit_type()

            habit_name_list = [habito["habit_name"] for habito in habits_table]

            if habit_name in habit_name_list:
                raise HabitException('El hábito ya existe.')

            if any(caracter.isdigit() for caracter in habit_name):
                raise HabitException('El hábito no debe tener números.')

            if len(description) > 100:
                raise HabitException('La descripción debe ser menor de 100 caracteres.')

            # POST a la API, ya que la api lo recibe en formato JSON, ya no como un objeto
            data = {
                "habit_name": habit_name,
                "habit_type": habit_type,
                "description": description
            }
            response = requests.post(self.API_URL_HABIT, json=data)
            if response.status_code != 200:
                raise Exception("Error al crear el hábito")

            new_habit = response.json()
            habit_id = new_habit["habit_id"]

            self.added_habit_description.emit(habit_id, habit_name,habit_type, description)
            self.number_of_habit_charts.emit()

        except HabitException as e:
            ShowMessage(QMessageBox.Icon.Information, 'Información', str(e))

class SaveDailyHabitButton(QWidget):
    API_URL_HABIT = "http://127.0.0.1:8000/habits/"
    API_URL_DATE = "http://127.0.0.1:8000/dates/"
    API_URL_DAILY = "http://127.0.0.1:8000/daily_habits/"

    added_habit_record = Signal(int,int,str,int,datetime.date,bool)
    number_of_records_charts = Signal()
    def __init__(self, daily_input, calendar):
        super().__init__()
         
        self.daily_input = daily_input
        self.calendar = calendar 
        
        save_button = QPushButton('Guardar')
        save_button.clicked.connect(self.save_daily_habit)
        save_button_layout = QHBoxLayout()
        save_button_layout.addWidget(save_button)
        self.setLayout(save_button_layout)

    def save_daily_habit(self):
        try:
            habit_name = self.daily_input.get_daily_habit()
            complet = self.daily_input.get_complet()

            habit_date = self.calendar.get_fecha() 
            show_date = habit_date.strftime('%d-%m-%Y') 

            if habit_name == "":
                raise HabitException('No has seleccionado ningún hábito.')

            response_habit_id = requests.get(f'{self.API_URL_HABIT}habit_name/{habit_name}')
            if response_habit_id.status_code != 200:
                raise HabitException('El habito no existe, primero tienes que crearlo.')
            existing_habit_id = response_habit_id.json()

            response_date_id = requests.get(
                self.API_URL_DATE,params={"habit_date": habit_date.isoformat()})
            if response_date_id.status_code != 200:
                raise HabitException('No se pudo obtener la fecha.')

            existing_date_id = response_date_id.json()

            if not existing_date_id:
                response_insert_date = requests.post(self.API_URL_DATE,json={'habit_date': habit_date.isoformat()})
                existing_date_id = response_insert_date.json()['date_id']  

            daily_data = {
                "habit": {
                    "habit_id": existing_habit_id,
                    "habit_name": habit_name
                },
                "date": {
                    "date_id": existing_date_id,
                    "habit_date": habit_date.isoformat()
                },
                "complet": complet
            }
            response_insert_daily = requests.post(self.API_URL_DAILY,json=daily_data)
            new_daily_habit = response_insert_daily.json()
            daily_id = new_daily_habit['daily_id'] 
            self.added_habit_record.emit(daily_id, existing_habit_id, habit_name,existing_date_id,show_date,complet) # señal
            self.number_of_records_charts.emit()
        except HabitException as e:
            ShowMessage(QMessageBox.Icon.Critical, "Crítico", str(e)) 

class ShowMessage(QMessageBox):
    def __init__(self, icon_type, tittle, message):
        super().__init__()
        self.icon_type = icon_type
        self.tittle = tittle
        self.message = message
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'Icons', 'precaution.png')
        box = QMessageBox()
        box.setIcon(self.icon_type)
        box.setWindowTitle(self.tittle)
        box.setWindowIcon(QIcon(icon_path))
        box.setText(self.message)
        box.exec()


