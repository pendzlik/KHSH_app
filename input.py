from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle



def create_rounded_input(hint_text, bind_func=None):
    # Создаём контейнер для TextInput
    input_container = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=[5, 5, 5, 5])

    with input_container.canvas.before:
        # Фон с скругленными углами
        Color(1, 1, 1, 1)  # Белый цвет
        input_container.rounded_bg = RoundedRectangle(size=input_container.size, pos=input_container.pos, radius=[10])

    with input_container.canvas.after:
        # Добавляем скруглённую рамку
        Color(0, 0, 0, 0.05)  # Чёрный цвет рамки
        input_container.rounded_border = RoundedRectangle(size=input_container.size, pos=input_container.pos, radius=[10])

    def update_bg(instance, value):
        # Обновляем размеры и позиции фона и рамки
        input_container.rounded_bg.size = input_container.size
        input_container.rounded_bg.pos = input_container.pos
        input_container.rounded_border.size = input_container.size
        input_container.rounded_border.pos = input_container.pos

    input_container.bind(size=update_bg, pos=update_bg)

    # Настраиваем TextInput
    text_input = TextInput(
        hint_text=hint_text,
        input_filter='float',
        multiline=False,
        background_color=(0, 0, 0, 0),  # Отключаем стандартный фон
        foreground_color=(0, 0, 0, 1),
        cursor_color=(0, 0, 0, 1),
        font_name="DejaVuSans"
    )

    if bind_func:
        text_input.bind(text=bind_func)

    input_container.add_widget(text_input)
    return input_container, text_input