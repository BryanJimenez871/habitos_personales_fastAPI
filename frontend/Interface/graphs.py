import requests
from PySide6.QtWidgets import QGridLayout, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtWidgets import QWidget, QVBoxLayout
from fastapi import HTTPException

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from frontend import Interface
from frontend.exceptions.custom_exceptions import HabitException
from frontend.Interface import ShowMessage


class GridGraphs(QWidget):
    def __init__(self):
        super().__init__()
        self.change_date = Interface.ChangeDate()
        self.numbers_habit_pie_chart = HabitsCountPieChart()
        self.daily_pie_chart = GoodHabitsPieChart(self.change_date)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.numbers_habit_pie_chart, 0, 0)
        grid_layout.addWidget(self.daily_pie_chart, 1, 0)
        self.setLayout(grid_layout)

class HabitsCountPieChart(QWidget):
    API_URL_HABIT = "http://127.0.0.1:8000/habits/"
    def __init__(self):
        super().__init__()

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.pie_chart()

    def pie_chart(self):
        response = requests.get(self.API_URL_HABIT)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code)

        habits_table = response.json()

        list_dictionary = []

        for habit in habits_table:
            daily_habits_dictionary = {
                'tipo_habito': habit['habit_type']}
            list_dictionary.append(daily_habits_dictionary)

        good_habit = 0
        bad_habit = 0

        for dictionary in list_dictionary:
            if dictionary['tipo_habito'] == 'Es bueno':
                good_habit += 1
            else:
                bad_habit += 1

        category = ["Buenos", "Malos"]
        values =[good_habit, bad_habit]
        explode = (0.09, 0)

        if sum(values) == 0:
            self.ax.text(0.5,0.5,"Sin datos", ha='center')
            self.ax.axis("off")
            self.canvas.draw()
            return

        wedges, *_ = self.ax.pie(
            values,
            explode=explode,
            labels=category,
            autopct=lambda pct: self.show_percent(pct, values)
        )
        for w in wedges:
            w.set_edgecolor('black')

        self.ax.set_title("Cantidad de hábitos")
        self.canvas.draw()

    @staticmethod
    def show_percent(percent, total_values):
        total = sum(total_values)
        quantity = int((percent / 100) * total)
        text = f"{percent:.1f}%\n({quantity} hábitos)"
        return text

    def update_chart(self):
        self.ax.clear()
        self.pie_chart()
        self.canvas.draw()

class GoodHabitsPieChart(QWidget):
    API_URL_DAILY = "http://127.0.0.1:8000/daily_habits/"
    API_URL_DATE = "http://127.0.0.1:8000/dates/"

    def __init__(self, change_date):
        super().__init__()

        self.figure = Figure(figsize=(12, 5))
        self.canvas = FigureCanvas(self.figure)
        self.change_date = change_date


        gs = self.figure.add_gridspec(1, 3, width_ratios=[1, 1.5, 1])
        self.ax_bad = self.figure.add_subplot(gs[0])
        self.ax_pie_chart = self.figure.add_subplot(gs[1])
        self.ax_good = self.figure.add_subplot(gs[2])

        self.figure.subplots_adjust(wspace=0.1)  # Un poco de espacio

        self.update_botton = QPushButton("Actualizar")
        self.update_botton.clicked.connect(self.update_year_pie_chart)

        self.view_all = QPushButton("Desde de la creación")
        self.view_all.clicked.connect(self.update_pie_chart)

        change_date_layout = QHBoxLayout()
        change_date_layout.addWidget(self.change_date)

        bottons_layout = QVBoxLayout()
        bottons_layout.addWidget(self.view_all)
        bottons_layout.addWidget(self.update_botton)

        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(change_date_layout,5)
        bottom_layout.addLayout(bottons_layout,2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        self.pie_chart()

    def pie_chart(self):
        self.ax_bad.axis('off')
        self.ax_pie_chart.axis('off')
        self.ax_good.axis('off')

        response_pie_char = requests.get(self.API_URL_DAILY+'pie_chart/')
        daily_table = response_pie_char.json()
        self.show_pie_chart(daily_table, "Desde el origen")

    def year_pie_chart(self):
        self.ax_bad.axis('off')
        self.ax_pie_chart.axis('off')
        self.ax_good.axis('off')
        start_date, end_date = self.change_date.get_year()
        year = start_date.year

        response_year_pie_char = requests.get(self.API_URL_DATE + 'range/',
                                              params={'start_date':start_date.isoformat(),
                                                      'end_date':end_date.isoformat()})
        only_year_table = response_year_pie_char.json()
        self.show_pie_chart(only_year_table, f'Año {year}')

    def month_pie_chart(self):
        self.ax_bad.axis('off')
        self.ax_pie_chart.axis('off')
        self.ax_good.axis('off')
        start_date, end_date = self.change_date.get_month()
        year = start_date.year
        dictionary = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio',
                       8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
        month = start_date.month

        response_month_pie_char = requests.get(self.API_URL_DATE + "range/",
                                              params={'start_date': start_date.isoformat(),
                                                      'end_date': end_date.isoformat()})
        only_month_table = response_month_pie_char.json()

        self.show_pie_chart(only_month_table, f'Año: {year} | Mes: {dictionary[month]}')

    def day_pie_chart(self):
        self.ax_bad.axis('off')
        self.ax_pie_chart.axis('off')
        self.ax_good.axis('off')
        daily_date = self.change_date.get_day()
        year = daily_date.year
        dictionary = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio',
                       8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
        month = daily_date.month
        day = daily_date.day
        response_day_pie_chart = requests.get(self.API_URL_DATE + "day_pie_chart/",params={'start_date':daily_date.isoformat()})
        only_day_table = response_day_pie_chart.json()
        self.show_pie_chart(only_day_table, f'Año: {year} | Mes: {dictionary[month]} | Día: {day}')

    def show_pie_chart(self, daily_habit_table, daily_date):
        personal_improvement = 0
        personal_decline = 0
        improvement_details = [0, 0]
        decline_details = [0, 0]

        for daily_habit in daily_habit_table:
            habit_type = daily_habit['habit']['habit_type']
            complet = daily_habit['complet']

            # Lógica simplificada de clasificación
            is_improvement = (habit_type == 'Es bueno' and complet) or (habit_type == 'Es malo' and not complet)

            if is_improvement:
                personal_improvement += 1
                idx = 0 if habit_type == 'Es bueno' else 1
                improvement_details[idx] += 1
            else:
                personal_decline += 1
                idx = 0 if habit_type == 'Es malo' else 1
                decline_details[idx] += 1

        pie_chart_values = [personal_improvement, personal_decline]
        total = sum(pie_chart_values)

        # Validación de vacío
        if total == 0:
            self.ax_pie_chart.text(0.5, 0.5, "Sin datos", ha='center')
            self.canvas.draw()
            return

        pie_chart_category = ["Mejora", "Deterioro"]
        colors = ['#90EE90', '#FF7F7F']
        explode = (0.05, 0)
        angle = -180 * (pie_chart_values[0] / total)

        wedges, *_ = self.ax_pie_chart.pie(
            pie_chart_values,
            autopct=lambda pct: self.show_percent(pct, total),
            startangle=angle,
            labels=pie_chart_category,
            explode=explode,
            colors=colors
        )
        for w in wedges: w.set_edgecolor('black')

        if personal_improvement:
            self.draw_detail_bar(
                ax=self.ax_good,
                values=improvement_details,
                labels=['H. Bueno\nCompletado', 'H. Malo\nNo Completado'],
                color='#90EE90',
                side='derecha'
            )
        if personal_decline:
            self.draw_detail_bar(
                ax=self.ax_bad,
                values=decline_details,
                labels=['H. Malo\nCompletado', 'H. Bueno\nNo complet'],
                color='#FF7F7F',
                side='izquierda'
            )
        self.ax_pie_chart.set_title(daily_date)
        self.canvas.draw()

    @staticmethod
    def draw_detail_bar(ax, values, labels, color, side):
        total = sum(values)
        if total == 0: return

        width = 0.3
        ratios = [v / total for v in values]
        bottom = 0

        for j, (height, label) in enumerate((zip(ratios, labels))):
            alpha = 0.5 + (0.4 * j)
            bc = ax.bar(0, height, width, bottom=bottom, label=label,
                        color=color, alpha=alpha, edgecolor='black')
            ax.bar_label(bc, labels=[f'{values[j]}\n({height:.0%})'], label_type='center')
            bottom += height

        ax.set_xlim(-0.5, 0.5)
        ax.axis('off')

        loc_anchor = (0.7, 0.5) if side == "derecha" else (0.3, 0.5)
        loc_align = "center left" if side == "derecha" else "center right"
        handles, labels_legend = ax.get_legend_handles_labels()
        ax.legend(
            handles[::-1],
            labels_legend[::-1],
            loc=loc_align,
            bbox_to_anchor=loc_anchor,
            fontsize='small'
        )
    @staticmethod
    def show_percent(pct, total_abs):
        quantity = int((pct / 100) * total_abs)
        return f"{pct:.1f}%\n({quantity})"

    def update_pie_chart(self):
        self.ax_bad.clear()
        self.ax_pie_chart.clear()
        self.ax_good.clear()
        self.pie_chart()
        self.canvas.draw()

    def update_year_pie_chart(self):
        year = self.change_date.get_year_combo()
        month = self.change_date.get_month_combo()
        day = self.change_date.get_day_combo()

        self.ax_bad.clear()
        self.ax_pie_chart.clear()
        self.ax_good.clear()

        try:
            if year > 1 and month == 0 and day == 0:
                self.year_pie_chart()
                self.canvas.draw()
            elif year > 1 and month >= 1 and day == 0:
                self.month_pie_chart()
                self.canvas.draw()
            elif year > 1 and month >= 1 and day > 0:
                self.day_pie_chart()
                self.canvas.draw()
            else:
                raise HabitException('Si quieres ver el día, te falta el month!')
        except HabitException as e:
            ShowMessage(QMessageBox.Icon.Information, "Información", str(e))
