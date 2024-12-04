from kivy.uix.button import Button
from kivy.properties import NumericProperty

class RoundedButton(Button):
    font_size_dynamic = NumericProperty(16)  # Изначальный размер шрифта

    def __init__(self, bg_color=(0, 0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Убираем стандартный фон кнопки
        self.color = (1, 1, 1, 1)  # Белый цвет текста
        self.bg_color = bg_color  # Цвет фона кнопки
        self.bind(pos=self.update_canvas, size=self.update_canvas)  # Обновляем Canvas при изменении размеров или позиции
        self.bind(size=self.update_font_size)  # Обновляем размер шрифта при изменении размеров кнопки

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle

            Color(*self.bg_color)  # Используем заданный цвет фона
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])  # Закруглённые углы

    def update_font_size(self, *args):
        # Пропорционально уменьшаем размер шрифта в зависимости от высоты кнопки
        self.font_size_dynamic = self.height * 0.4  # 40% от высоты кнопки
