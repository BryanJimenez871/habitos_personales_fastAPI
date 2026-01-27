from PySide6.QtWidgets import QWidget, QVBoxLayout, QDateEdit, QCalendarWidget, QLabel, QComboBox, QHBoxLayout
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QTextCharFormat, QColor
import datetime


class Calendar(QWidget):
    def __init__(self):
        super().__init__()

        date_label = QLabel("Escoja la fecha del habito:")

        self.date_habit = QDateEdit()
        self.date_habit.setCalendarPopup(True)
        self.date_habit.setDate(QDate.currentDate())

        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        calendar.setNavigationBarVisible(True)

        calendar.setStyleSheet("""
        QCalendarWidget QAbstractItemView::item:selected {
            color: yellow;
        }
        QCalendarWidget QAbstractItemView::item:hover {
            background-color: gray;
        }
        """)

        weekend = QTextCharFormat()
        weekend.setForeground(QColor("white"))

        # Aplicar al sábado y domingo
        calendar.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, weekend)
        calendar.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, weekend)

        layout = QVBoxLayout()
        self.date_habit.setCalendarWidget(calendar)
        layout.addWidget(date_label)
        layout.addWidget(self.date_habit)

        self.setLayout(layout)

    def get_fecha(self):
        date_calendar = self.date_habit.date()
        habit_date = datetime.datetime(date_calendar.year(), date_calendar.month(), date_calendar.day()).date()
        return habit_date

class ChangeDate(QWidget):
    def __init__(self):
        super().__init__()

        year_label = QLabel("Año")
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(a) for a in range(2026, 2101)])

        self.months = {'Sin mes':0, 'Enero':1, 'Febrero':2, 'Marzo':3, 'Abril':4, 'Mayo':5, 'Junio':6, 'Julio':7,
                       'Agosto':8, 'Septiembre':9, 'Octubre':10, 'Noviembre':11, 'Diciembre':12}
        month_label = QLabel("Mes")
        self.month_combo = QComboBox()
        self.month_combo.addItems([a for a in self.months.keys()])

        day_label = QLabel("Día")
        self.day_combo = QComboBox()
        self.day_combo.addItem('Sin dia')
        self.day_combo.addItems([str(a) for a in range(1, 32)])

        year_layout = QVBoxLayout()
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_combo)

        month_layout = QVBoxLayout()
        month_layout.addWidget(month_label)
        month_layout.addWidget(self.month_combo)

        day_layout = QVBoxLayout()
        day_layout.addWidget(day_label)
        day_layout.addWidget(self.day_combo)

        main_layout = QHBoxLayout()
        main_layout.addLayout(year_layout)
        main_layout.addLayout(month_layout)
        main_layout.addLayout(day_layout)

        self.setLayout(main_layout)

    def get_year_combo(self):
        return int(self.year_combo.currentText())

    def get_month_combo(self):
        return int(self.months.get(self.month_combo.currentText()))

    def get_day_combo(self):
        index = self.day_combo.currentIndex()
        if index == 0:
            return 0
        else:
            return int(self.day_combo.currentText())

    def get_year(self):
        year = int(self.year_combo.currentText())
        start_date = datetime.date(year,1,1)
        end_date = datetime.date(year + 1, 1, 1)
        return start_date, end_date

    def get_month(self):
        year = int(self.year_combo.currentText())
        month = self.month_combo.currentText()
        int_month = self.months.get(month, 0)

        if int_month < 12:
            start_date = datetime.date(year, int_month, 1)
            end_date = datetime.date(year, int_month + 1, 1)
            return start_date, end_date
        else:
            start_date = datetime.date(year, int_month, 1)
            end_date = datetime.date(year, int_month, 1)
            return start_date, end_date

    def get_day(self):
        year = int(self.year_combo.currentText())
        month = self.month_combo.currentText()
        int_month = self.months.get(month, 0)
        day = int(self.day_combo.currentText())
        date = datetime.date(year, int_month, day)
        return date