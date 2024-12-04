from screen1 import Screen1
from screen2 import Screen2

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.core.text import LabelBase

# Регистрация шрифта DejaVu Sans
LabelBase.register(name="DejaVuSans", fn_regular="fonts/DejaVuSans.ttf")



Window.clearcolor = (1, 1, 1, 1)  # белый (RGBA)
#Window.size = (360, 640)  # Размер для стандартного Android-экрана




# Главное приложение
class AcidBaseApp(App):
    title ="КЩС"

    def build(self):
        screen_manager = ScreenManager()

        # Добавление экранов в ScreenManager
        screen_manager.add_widget(Screen1(name="screen1"))
        screen_manager.add_widget(Screen2(name="screen2"))

        return screen_manager



if __name__ == "__main__":
    AcidBaseApp().run()