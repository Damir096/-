import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
import random  # Добавляем модуль random для генерации случайных цветов и стилей линий

class GravidogramApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Программа Гравидограмма')

        self.patients_data = {}
        self.percentile_styles = ['-', '--', '-.', ':']
        self.percentile_90_style = self.percentile_styles[0]
        self.percentile_30_style = self.percentile_styles[1]
        self.percentile_10_style = self.percentile_styles[2]
        self.percentile_50_style = self.percentile_styles[3]

        self.initialize_ui()
        
    def initialize_ui(self):
        self.create_widgets()
    
    def create_widgets(self):
        # Комбо-бокс для выбора пациента
        self.patient_combobox = ttk.Combobox(self.root, values=list(self.patients_data.keys()), state='readonly')
        self.patient_combobox.pack()

        # Кнопка для добавления данных пациента
        add_patient_button = ttk.Button(self.root, text='Добавить данные пациента', command=self.add_patient_data)
        add_patient_button.pack()

        # Кнопка для построения гравидограммы
        plot_gravidogram_button = ttk.Button(self.root, text='Построить гравидограмму', command=self.plot_gravidogram)
        plot_gravidogram_button.pack()

        # Кнопка для сохранения гравидограммы в PDF
        save_to_pdf_button = ttk.Button(self.root, text='Сохранить в PDF', command=self.save_to_pdf)
        save_to_pdf_button.pack()

        # Создаем холст для отображения графика
        self.fig = plt.figure(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def add_patient_data(self):
        patient_name_iin = simpledialog.askstring('Добавить пациента', 'Введите Ф.И.О и ИИН пациента (через запятую):')
        if not patient_name_iin:
            return

        patient_name, patient_iin = map(str.strip, patient_name_iin.split(','))

        weeks_str = simpledialog.askstring('Добавить пациента', 'Введите недели беременности (через запятую):')
        if not weeks_str:
            return

        vdu_str = simpledialog.askstring('Добавить пациента', 'Введите ВДМ (см) (через запятую):')
        if not vdu_str:
            return

        weeks = list(map(int, weeks_str.split(',')))
        vdu = list(map(int, vdu_str.split(',')))

        # Генерируем случайный цвет и стиль линии для этого приема
        line_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        line_style = random.choice(self.percentile_styles)

        # Проверяем, есть ли уже данные для этого пациента
        if patient_iin in self.patients_data:
            self.patients_data[patient_iin]['visits'].append({'weeks': weeks, 'vdu': vdu, 'color': line_color, 'style': line_style})
        else:
            self.patients_data[patient_iin] = {'name': patient_name, 'visits': [{'weeks': weeks, 'vdu': vdu, 'color': line_color, 'style': line_style}]}

        self.patient_combobox['values'] = list(self.patients_data.keys())

    def plot_gravidogram(self):
        patient_iin = self.patient_combobox.get()
        if patient_iin not in self.patients_data:
            return

        patient_data = self.patients_data[patient_iin]

        plt.clf()

        for visit in patient_data['visits']:
            weeks = visit['weeks']
            vdu = visit['vdu']
            color = visit['color']
            style = visit['style']

            prev_week = weeks[0]
            prev_vdu = vdu[0]

            for week, vdu_value in zip(weeks, vdu):
                plt.plot([prev_week, week], [prev_vdu, vdu_value], marker='o', linestyle=style, label='Высота дна матки (ВДМ)', color=color)
                prev_week = week
                prev_vdu = vdu_value

        vdu_values = [vdu_value for visit in patient_data['visits'] for vdu_value in visit['vdu']]
        percentile_90 = np.percentile(vdu_values, 90)
        percentile_30 = np.percentile(vdu_values, 30)
        percentile_10 = np.percentile(vdu_values, 10)

        plt.axhline(y=percentile_90, color='red', linestyle=self.percentile_90_style, label='Percentile 90')
        plt.axhline(y=percentile_30, color='blue', linestyle=self.percentile_30_style, label='Percentile 30')
        plt.axhline(y=percentile_10, color='green', linestyle=self.percentile_10_style, label='Percentile 10')

        plt.xlabel('Недели беременности')
        plt.ylabel('ВДМ (см)')
        plt.title(f'Гравидограмма для пациента {patient_data["name"]} (ИИН: {patient_iin})')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        self.canvas.draw()

    def save_to_pdf(self):
        patient_iin = self.patient_combobox.get()
        if patient_iin not in self.patients_data:
            return

        patient_data = self.patients_data[patient_iin]

        plt.clf()

        for visit in patient_data['visits']:
            weeks = visit['weeks']
            vdu = visit['vdu']
            color = visit['color']
            style = visit['style']

            prev_week = weeks[0]
            prev_vdu = vdu[0]

            for week, vdu_value in zip(weeks, vdu):
                plt.plot([prev_week, week], [prev_vdu, vdu_value], marker='o', linestyle=style, label='Высота дна матки (ВДМ)', color=color)
                prev_week = week
                prev_vdu = vdu_value

        vdu_values = [vdu_value for visit in patient_data['visits'] for vdu_value in visit['vdu']]
        percentile_90 = np.percentile(vdu_values, 90)
        percentile_30 = np.percentile(vdu_values, 30)
        percentile_10 = np.percentile(vdu_values, 10)

        plt.axhline(y=percentile_90, color='red', linestyle=self.percentile_90_style, label='Percentile 90')
        plt.axhline(y=percentile_30, color='blue', linestyle=self.percentile_30_style, label='Percentile 30')
        plt.axhline(y=percentile_10, color='green', linestyle=self.percentile_10_style, label='Percentile 10')

        plt.xlabel('Недели беременности')
        plt.ylabel('ВДМ (см)')
        plt.title(f'Гравидограмма для пациента {patient_data["name"]} (ИИН: {patient_iin})')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        with PdfPages(f'gravidogram_{patient_iin}.pdf') as pdf:
            pdf.savefig()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = GravidogramApp(root)
    app.run()
