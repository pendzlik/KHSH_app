from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from input import create_rounded_input
from button import RoundedButton


# Экран для расчёта AG и Gap-Gap
class Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Заголовок экрана
        title_label = Label(
            text="Расчёт AG и gap-gap",
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

        # Контейнер для cK+
        k_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        k_input_container, self.k_input = create_rounded_input("cK⁺ (mmol/L)", self.update_k_status)
        self.k_status = Label(text="–", size_hint=(0.3, 1), color=(0, 0, 0, 1))
        k_layout.add_widget(k_input_container)
        k_layout.add_widget(self.k_status)
        root_layout.add_widget(k_layout)

        # Контейнер для cNa+
        na_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        na_input_container, self.na_input = create_rounded_input("cNa⁺ (mmol/L)", self.update_na_status)
        self.na_status = Label(text="–", size_hint=(0.3, 1), color=(0, 0, 0, 1))
        na_layout.add_widget(na_input_container)
        na_layout.add_widget(self.na_status)
        root_layout.add_widget(na_layout)

        # Контейнер для cCl-
        cl_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        cl_input_container, self.cl_input = create_rounded_input("cCl⁻ (mmol/L)", self.update_cl_status)
        self.cl_status = Label(text="–", size_hint=(0.3, 1), color=(0, 0, 0, 1))
        cl_layout.add_widget(cl_input_container)
        cl_layout.add_widget(self.cl_status)
        root_layout.add_widget(cl_layout)

        # Контейнер для cHCO3-
        hco3_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        hco3_input_container, self.hco3_input = create_rounded_input("cHCO3⁻ (mmol/L)", self.update_hco3_status)
        self.hco3_status = Label(text="–", size_hint=(0.3, 1), color=(0, 0, 0, 1))
        hco3_layout.add_widget(hco3_input_container)
        hco3_layout.add_widget(self.hco3_status)
        root_layout.add_widget(hco3_layout)




        # Прокручиваемый контейнер для вывода результатов AG и Gap-Gap
        scroll_view = ScrollView(size_hint=(1, 0.5), bar_width=10, effect_cls='ScrollEffect')

        self.ag_gap_result_label = Label(
            text="Результат AG и Gap-Gap будет здесь.",
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
        self.ag_gap_result_label.bind(
            texture_size=lambda instance, size: setattr(instance, 'height', size[1])
        )

        # Привязка ширины текста к ширине ScrollView
        def update_ag_gap_text_size(instance, value):
            self.ag_gap_result_label.text_size = (instance.width - 20, None)  # Учитываем отступы (padding)

        scroll_view.bind(width=update_ag_gap_text_size)

        # Добавляем фон и рамки
        with self.ag_gap_result_label.canvas.before:
            Color(0, 0, 0, 0.04)  # Светло-серый фон
            self.ag_gap_background = Rectangle(size=self.ag_gap_result_label.size, pos=self.ag_gap_result_label.pos)
            Color(0, 0, 0, 0.5)  # Черный цвет для рамки
            self.ag_gap_border = Line(rectangle=(self.ag_gap_result_label.x, self.ag_gap_result_label.y,
                                                self.ag_gap_result_label.width, self.ag_gap_result_label.height),
                                    width=1)

        # Обновляем фон и рамку при изменении размеров или позиции
        def update_ag_gap_background_and_border(instance, value):
            self.ag_gap_background.size = instance.size
            self.ag_gap_background.pos = instance.pos
            self.ag_gap_border.rectangle = (instance.x, instance.y, instance.width, instance.height)

        self.ag_gap_result_label.bind(size=update_ag_gap_background_and_border, pos=update_ag_gap_background_and_border)

        # Добавляем Label в ScrollView и затем в root_layout
        scroll_view.add_widget(self.ag_gap_result_label)
        root_layout.add_widget(scroll_view)



        # Кнопка для расчёта AG и Gap-Gap
        ag_gap_button = RoundedButton(
            text="AG и Gap-Gap",
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5},
            bg_color=(0.2, 0.6, 1, 1),  # Синий цвет
            font_size='16sp',  # Увеличенный размер шрифта
            font_name='fonts/DejaVuSans-Bold'
        )
        ag_gap_button.bind(on_press=self.calculate_ag_gap)
        root_layout.add_widget(ag_gap_button)

        # Кнопка для перехода на первый экран
        prev_button = RoundedButton(
            text="Назад", 
            size_hint=(0.6, 0.1),  # Уменьшаем ширину кнопки
            pos_hint={"center_x": 0.5},  # Центрируем кнопку по горизонтали
            font_size='16sp',  # Увеличенный размер шрифта
            font_name='fonts/DejaVuSans-Bold'
            )
        prev_button.bind(on_press=self.switch_to_screen1)
        root_layout.add_widget(prev_button)

        self.add_widget(root_layout)

    def update_k_status(self, instance, value):
        try:
            k = float(value)
            if k > 5.1:
                self.k_status.text = "Повышен"
                self.k_status.color = (1, 0, 0, 1)  # Красный
            elif k < 3.4:
                self.k_status.text = "Понижен"
                self.k_status.color = (1, 0.8, 0, 1)  # Жёлтый
            else:
                self.k_status.text = "Норма"
                self.k_status.color = (0, 1, 0, 1)  # Зелёный
        except ValueError:
            self.k_status.text = "–"
            self.k_status.color = (0, 0, 0, 1)

    def update_na_status(self, instance, value):
        try:
            na = float(value)
            if na > 150.0:
                self.na_status.text = "Повышен"
                self.na_status.color = (1, 0, 0, 1)  # Красный
            elif na < 130.0:
                self.na_status.text = "Понижен"
                self.na_status.color = (1, 0.8, 0, 1)  # Жёлтый
            else:
                self.na_status.text = "Норма"
                self.na_status.color = (0, 1, 0, 1)  # Зелёный
        except ValueError:
            self.na_status.text = "–"
            self.na_status.color = (0, 0, 0, 1)

    def update_cl_status(self, instance, value):
        try:
            cl = float(value)
            if cl > 109.0:
                self.cl_status.text = "Повышен"
                self.cl_status.color = (1, 0, 0, 1)  # Красный
            elif cl < 95.0:
                self.cl_status.text = "Понижен"
                self.cl_status.color = (1, 0.8, 0, 1)  # Жёлтый
            else:
                self.cl_status.text = "Норма"
                self.cl_status.color = (0, 1, 0, 1)  # Зелёный
        except ValueError:
            self.cl_status.text = "–"
            self.cl_status.color = (0, 0, 0, 1)

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

    def calculate_ag_gap(self, instance):
        try:
            ck = float(self.k_input.text)
            cna = float(self.na_input.text)
            ccl = float(self.cl_input.text)
            hco3 = float(self.hco3_input.text)
            
            # Расчёт AG
            ag = cna + ck - (ccl + hco3)
            normal_ag = 12
            delta_be = (ag - normal_ag) / (24 - hco3)

            # Анализ AG/BE
            if delta_be < 0.4:
                result = "Гиперхлоремический ацидоз с нормальной AG."
            elif 0.4 <= delta_be <= 0.8:
                result = "Комбинированный метаболический ацидоз с ↑ или N AG, часто связано с ацидозом при почечной недостаточности."
            elif delta_be == 1:
                result = "Наиболее характерно для диабетического кетоацидоза вследствие потерь кетоновых тел с мочой."
            elif 1 < delta_be <= 2:
                result = "Типично для ацидоза с увеличенной AG."
            else:
                result = "Предполагает изначальное ↑ HCO3 (cосуществующий метаболический алкалоз или предшествующий респираторный ацидоз с метаболической компенсацией)."

            self.ag_gap_result_label.text = f"AG: {ag:.2f} ммоль/л\nGap-Gap: {delta_be:.2f}\n{result}"
            self.ag_gap_result_label.font_name = "DejaVuSans"
        except ValueError:
            self.ag_gap_result_label.text = "Ошибка: проверьте введённые значения!"
            self.ag_gap_result_label.font_name = "DejaVuSans"


    def switch_to_screen1(self, instance):
        self.manager.current = "screen1"