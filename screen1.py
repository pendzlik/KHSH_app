from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from input import create_rounded_input
from button import RoundedButton

# Экран для анализа pH, CO2, HCO3
class Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Заголовок экрана
        title_label = Label(
            text="Нарушения КЩС",
            font_size='24sp',           # Размер шрифта
            bold=False,                  # Жирный текст
            size_hint=(1, 0.1),         # Высота заголовка
            color=(0, 0, 0, 1),         # Цвет текста (чёрный)
            halign='center',            # Горизонтальное выравнивание
            valign='middle',            # Вертикальное выравнивание
            text_size=(self.width, None), # Размер текста будет равен ширине окна
            markup=True,
            font_name="DejaVuSans"
        )

        # Обновляем text_size при изменении размера окна
        title_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

        root_layout.add_widget(title_label)



        # Контейнер для pH
        ph_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        ph_input_container, self.ph_input = create_rounded_input("pH", self.update_ph_status)
        self.ph_status = Label(text="–", size_hint=(0.3, 1), color=(0, 0, 0, 1))
        ph_layout.add_widget(ph_input_container)
        ph_layout.add_widget(self.ph_status)
        root_layout.add_widget(ph_layout)

        # Контейнер для pCO2
        pco2_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        pco2_input_container, self.pco2_input = create_rounded_input("pCO2 (mmHg)", self.update_pco2_status)
        self.pco2_status = Label(text="–", size_hint=(0.3, 1), color=(0, 0, 0, 1))
        pco2_layout.add_widget(pco2_input_container)
        pco2_layout.add_widget(self.pco2_status)
        root_layout.add_widget(pco2_layout)

        # Контейнер для cHCO3-
        hco3_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        hco3_input_container, self.hco3_input = create_rounded_input("cHCO3⁻(P),с (mmol/L)", self.update_hco3_status)
        self.hco3_status = Label(text="–", size_hint=(0.3, 1), color=(0, 0, 0, 1))
        hco3_layout.add_widget(hco3_input_container)
        hco3_layout.add_widget(self.hco3_status)
        root_layout.add_widget(hco3_layout)









        # Прокручиваемый контейнер для длинного текста
        scroll_view = ScrollView(size_hint=(1, 0.5), bar_width=10, effect_cls='ScrollEffect')

        self.result_label = Label(
            text="Результат будет здесь.",
            halign='justify',
            valign='top',  # Выравнивание текста по верхнему краю
            size_hint=(1, None),  # Высота будет подстраиваться под текст
            text_size=(scroll_view.width, None),  # Изначально ограничиваем ширину текста шириной контейнера
            padding=(10, 10),  # Отступы вокруг текста
            font_size=20,  # Увеличенный размер шрифта
            color=(0, 0, 0, 1),
            font_name='DejaVuSans',
            markup=True
        )

        # Автоматическая настройка высоты Label на основе размера текста
        self.result_label.bind(
            texture_size=lambda instance, size: setattr(instance, 'height', size[1])
        )

        # Привязка ширины текста к ширине ScrollView
        def update_text_size(instance, value):
            self.result_label.text_size = (instance.width - 20, None)  # Учитываем отступы (padding)

        scroll_view.bind(width=update_text_size)

        # Добавляем фон и рамки
        with self.result_label.canvas.before:
            Color(0, 0, 0, 0.04)  # Светло-серый фон
            self.background = Rectangle(size=self.result_label.size, pos=self.result_label.pos)
            Color(0, 0, 0, 0.5)  # Черный цвет для рамки
            self.border = Line(rectangle=(self.result_label.x, self.result_label.y,
                                        self.result_label.width, self.result_label.height),
                            width=1)

        # Обновляем фон и рамку при изменении размеров или позиции
        def update_background_and_border(instance, value):
            self.background.size = instance.size
            self.background.pos = instance.pos
            self.border.rectangle = (instance.x, instance.y, instance.width, instance.height)

        self.result_label.bind(size=update_background_and_border, pos=update_background_and_border)

        # Добавляем Label в ScrollView и затем в root_layout
        scroll_view.add_widget(self.result_label)
        root_layout.add_widget(scroll_view)


        # Объединённая кнопка для анализа и расчёта компенсации
        analyze_and_compensate_button = RoundedButton(
            text="Диагноз",
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5},
            bg_color=(0.2, 0.6, 1, 1),  # Синий цвет
            font_size='16sp',  # Увеличенный размер шрифта
            font_name='fonts/DejaVuSans-Bold'
        )
        analyze_and_compensate_button.bind(on_press=self.analyze_and_calculate)
        root_layout.add_widget(analyze_and_compensate_button)

        # Кнопка перехода ко второму экрану
        next_button = RoundedButton(
            text="AG и gap-gap",
            size_hint=(0.6, 0.1),  # Уменьшаем ширину кнопки
            pos_hint={"center_x": 0.5},  # Центрируем кнопку по горизонтали
            font_size='16sp',  # Увеличенный размер шрифта
            font_name='fonts/DejaVuSans-Bold'
        )
        next_button.bind(on_press=self.switch_to_screen2)
        root_layout.add_widget(next_button)

        self.add_widget(root_layout)

    def update_ph_status(self, instance, value):
        try:
            ph = float(value)
            if ph > 7.450:
                self.ph_status.text = "Повышен"
                self.ph_status.color = (1, 0, 0, 1)  # Красный
            elif ph < 7.350:
                self.ph_status.text = "Понижен"
                self.ph_status.color = (1, 0.8, 0, 1)  # Жёлтый
            else:
                self.ph_status.text = "Норма"
                self.ph_status.color = (0, 1, 0, 1)  # Зелёный
        except ValueError:
            self.ph_status.text = "–"
            self.ph_status.color = (0, 0, 0, 1)  

    def update_pco2_status(self, instance, value):
        try:
            pco2 = float(value)
            if pco2 > 48.0:
                self.pco2_status.text = "Повышен"
                self.pco2_status.color = (1, 0, 0, 1)  # Красный
            elif pco2 < 32.0:
                self.pco2_status.text = "Понижен"
                self.pco2_status.color = (1, 0.8, 0, 1)  # Жёлтый
            else:
                self.pco2_status.text = "Норма"
                self.pco2_status.color = (0, 1, 0, 1)  # Зелёный
        except ValueError:
            self.pco2_status.text = "–"
            self.pco2_status.color = (0, 0, 0, 1) 

    def update_hco3_status(self, instance, value):
        try:
            hco3 = float(value)
            if hco3 > 28.0:
                self.hco3_status.text = "Повышен"
                self.hco3_status.color = (1, 0, 0, 1)  # Красный
            elif hco3 < 21.0:
                self.hco3_status.text = "Понижен"
                self.hco3_status.color = (1, 0.8, 0, 1)  # Жёлтый
            else:
                self.hco3_status.text = "Норма"
                self.hco3_status.color = (0, 1, 0, 1)  # Зелёный
        except ValueError:
            self.hco3_status.text = "–"
            self.hco3_status.color = (0, 0, 0, 1) 



    def analyze_and_calculate(self, instance):
        try:
            # Получаем значения из полей ввода
            ph = float(self.ph_input.text)
            pco2 = float(self.pco2_input.text)
            hco3 = float(self.hco3_input.text)

            # Инициализация стрелок и норм
            ph_arrow = "↑" if ph > 7.450 else "↓" if ph < 7.350 else "→"
            pco2_arrow = "↑" if pco2 > 48.0 else "↓" if pco2 < 32.0 else "→"

            # Границы нормальных значений
            normal_ph_range = (7.350, 7.450)
            normal_pco2_range = (32.0, 48.0)

            result = "Результат анализа (пошаговый):\n"

            # Существующий анализ первичных нарушений pH
            if ph < normal_ph_range[0] or ph > normal_ph_range[1]:
                if ph < normal_ph_range[0]:  # Ацидоз
                    if pco2 > normal_pco2_range[1]:
                        result += "pH ↓ и CO₂ ↑: респираторный ацидоз.\n"
                    elif pco2 < normal_pco2_range[0]:
                        result += "pH ↓ и CO₂ ↓: метаболический ацидоз.\n"
                    else:
                        result += "pH ↓, но CO₂ в норме: метаболическое нарушение (без компенсации).\n"
                elif ph > normal_ph_range[1]:  # Алкалоз
                    if pco2 < normal_pco2_range[0]:
                        result += "pH ↑ и CO₂ ↓: респираторный алкалоз.\n"
                    elif pco2 > normal_pco2_range[1]:
                        result += "pH ↑ и CO₂ ↑: метаболический алкалоз.\n"
                    else:
                        result += "pH ↑, но CO₂ в норме: метаболическое нарушение (без компенсации).\n"
            else:
                if pco2 < normal_pco2_range[0] or pco2 > normal_pco2_range[1]:
                    result += "pH в норме, но CO₂ изменено: смешанное респираторно-метаболическое расстройство.\n"
                else:
                    result += "Значения в пределах нормы. Компенсация не требуется.\n"

            # Расчёт компенсаций
            if ph < normal_ph_range[0] or ph > normal_ph_range[1]:
                if (ph < normal_ph_range[0] and pco2 < normal_pco2_range[0]) or \
                        (ph > normal_ph_range[1] and pco2 > normal_pco2_range[1]):
                    result += "\nРеспираторная компенсация для метаболических нарушений:\n"

                    if ph < normal_ph_range[0]:  # Метаболический ацидоз
                        pco2_calc = 1.5 * hco3 + 8
                        pco2_range = (pco2_calc - 2, pco2_calc + 2)
                        result += f"Рассчитанный диапазон PaCO₂: {pco2_range[0]:.2f} – {pco2_range[1]:.2f} мм рт. ст.\n"
                        if pco2 > pco2_range[1]:
                            result += "PaCO₂изм. > PaCO₂расч.: Сопутствующий респираторный ацидоз.\n"
                        elif pco2 < pco2_range[0]:
                            result += "PaCO₂изм. < PaCO₂расч.: Респираторный алкалоз.\n"
                        else:
                            result += "Компенсированное состояние.\n"
                    elif ph > normal_ph_range[1]:  # Метаболический алкалоз
                        pco2_calc = 0.7 * hco3 + 20
                        pco2_range = (pco2_calc - 5, pco2_calc + 5)
                        result += f"Рассчитанный диапазон PaCO₂: {pco2_range[0]:.2f} – {pco2_range[1]:.2f} мм рт. ст.\n"
                        if pco2 > pco2_range[1]:
                            result += "PaCO₂изм. > PaCO₂расч.: Сопутствующий респираторный ацидоз.\n"
                        elif pco2 < pco2_range[0]:
                            result += "PaCO₂изм. < PaCO₂расч.: Респираторный алкалоз.\n"
                        else:
                            result += "Компенсированное состояние.\n"

                elif (ph < normal_ph_range[0] and pco2 > normal_pco2_range[1]) or \
                        (ph > normal_ph_range[1] and pco2 < normal_pco2_range[0]):
                    result += "\nМетаболическая компенсация для респираторных нарушений:\n"

                    if pco2 > normal_pco2_range[1]:  # Респираторный ацидоз
                        hco3_calc = 24 + ((pco2 - 40) / 10)
                        result += f"Рассчитанное значение HCO₃⁻: {hco3_calc:.2f} ммоль/л.\n"
                        if hco3 > hco3_calc:
                            result += "HCO₃изм. > HCO₃расч.: Сопутствующий метаболический алкалоз.\n"
                        elif hco3 < hco3_calc:
                            result += "HCO₃изм. < HCO₃расч.: Сопутствующий метаболический ацидоз.\n"
                        else:
                            result += "Компенсированное состояние.\n"
                    elif pco2 < normal_pco2_range[0]:  # Респираторный алкалоз
                        hco3_calc = 24 - 2 * ((40 - pco2) / 10)
                        result += f"Рассчитанное значение HCO₃⁻: {hco3_calc:.2f} ммоль/л.\n"
                        if hco3 > hco3_calc:
                            result += "HCO₃изм. > HCO₃расч.: Сопутствующий метаболический алкалоз.\n"
                        elif hco3 < hco3_calc:
                            result += "HCO₃изм. < HCO₃расч.: Сопутствующий метаболический ацидоз.\n"
                        else:
                            result += "Компенсированное состояние.\n"

            # Новый алгоритм(табличный)
            result += "\nДополнительный анализ (табличный):\n"
            if normal_ph_range[0] <= ph <= normal_ph_range[1]:
                result += "Норма pH. Кислотно-щелочной баланс в пределах нормы.\n"

            elif ph > normal_ph_range[1]:  # Алкалоз
                if pco2 > normal_pco2_range[1]:  # Метаболический алкалоз
                    result += "Метаболический алкалоз.\n"
                    x_calc = 0.7 * hco3 + 20
                    x_range = (x_calc - 1.5, x_calc + 1.5)  # Диапазон x для метаболического алкалоза
                    result += f"Рассчитанный диапазон x: {x_range[0]:.2f} – {x_range[1]:.2f}\n"
                    
                    # Сравнение pCO2 с диапазоном
                    if pco2 > x_range[1]:
                        result += "pCO₂изм. > x: Сопутствующий респираторный ацидоз.\n"
                    elif pco2 < x_range[0]:
                        result += "pCO₂изм. < x.: Сопутствующий респираторный алкалоз.\n"
                    else:
                        result += "Компенсированный метаболический алкалоз.\n"

                elif pco2 < normal_pco2_range[0]:  # Респираторный алкалоз
                    y =  (7.4 - ph) / (pco2 - 40) * 100
                    result += f"Рассчитанное значение y: {y:.2f}\n"  # Вывод значения y

                    if y > 0.8:
                        result += "Сопутствующий метаболический алкалоз.\n"
                        result += f"y ({y:.2f}) > 0.8.\n"  # Показываем сравнение
                    elif y == 0.8:
                        result += "Острый респираторный алкалоз.\n"
                        result += f"y ({y:.2f}) = 0.8.\n"  # Показываем точное равенство
                    elif 0.2 < y < 0.8:
                        result += "Частично компенсированный респираторный алкалоз.\n"
                        result += f"y ({y:.2f}) находится в диапазоне 0.2–0.8.\n"  # Диапазон сравнения
                    else:
                        result += "Сопутствующий метаболический ацидоз.\n"
                        result += f"y ({y:.2f}) < 0.2.\n"  # Показываем, что y ниже диапазона


                else:  # Нормальный pCO₂
                    result += "Метаболический алкалоз.\n"
                    x_calc = 0.7 * hco3 + 20
                    x_range = (x_calc - 1.5, x_calc + 1.5)  # Диапазон x для метаболического алкалоза
                    result += f"Рассчитанный диапазон x: {x_range[0]:.2f} – {x_range[1]:.2f}\n"
                    result += "Хронический метаболический алкалоз.\n"


            elif ph < normal_ph_range[0]:  # Ацидоз
                if pco2 > normal_pco2_range[1]:  # Респираторный ацидоз
                    y = (7.4 - ph) / (pco2 - 40) * 100
                    result += f"Рассчитанное значение y: {y:.2f}\n"  # Добавляем вывод значения y

                    if y > 0.8:
                        result += f"y ({y:.2f}) > 0.8.\n"  # Показываем, как y сравнивается
                        result += "Сопутствующий метаболический ацидоз.\n"
                    elif y == 0.8:
                        result += f"y ({y:.2f}) = 0.8.\n"  # Показываем точное равенство
                        result += "Острый респираторный ацидоз.\n"
                    elif 0.3 < y < 0.8:
                        result += f"y ({y:.2f}) находится в диапазоне 0.3–0.8.\n"  # Диапазон сравнения
                        result += "Частично компенсированный респираторный ацидоз.\n"
                    else:
                        result += f"y ({y:.2f}) < 0.3.\n"  # Показываем, что y ниже диапазона
                        result += "Сопутствующий метаболический алкалоз.\n"


                else: # Метаболический ацидоз
                    result += "Метаболический ацидоз.\n"
                    x_calc = 1.5 * hco3 + 8
                    x_range = (x_calc - 2, x_calc + 2)  # Диапазон x для метаболического ацидоза
                    result += f"Рассчитанный диапазон x: {x_range[0]:.2f} – {x_range[1]:.2f}\n"
                    
                    # Сравнение pCO2 с диапазоном
                    if pco2 > x_range[1]:
                        result += "pCO₂изм. > x: Сопутствующий респираторный ацидоз.\n"
                    elif pco2 < x_range[0]:
                        result += "pCO₂изм. < x: Сопутствующий респираторный ацидоз.\n"
                    else:
                        result += "Компенсированный метаболический алкалоз.\n"


            self.result_label.text = result
            self.result_label.font_name = "DejaVuSans"  # Указываем зарегистрированный шрифт


        except ValueError:
            self.result_label.text = "Ошибка: проверьте введённые значения!"
            self.result_label.font_name = "DejaVuSans"  # Указываем зарегистрированный шрифт



    def switch_to_screen2(self, instance):
        self.manager.current = "screen2"