# """
# My first application
# """

# import toga
# from toga.style import Pack
# from toga.style.pack import COLUMN, ROW


# class LondonTravelApp(toga.App):
#     def startup(self):
#         """Construct and show the Toga application.

#         Usually, you would add your application to a main content box.
#         We then create a main window (with a name matching the app), and
#         show the main window.
#         """
#         main_box = toga.Box()

#         self.main_window = toga.MainWindow(title=self.formal_name)
#         self.main_window.content = main_box
#         self.main_window.show()


# def main():
#     return LondonTravelApp()

# import toga


# def button_handler(widget):
#     print("hello")


# def build(app):
#     box = toga.Box()

#     button = toga.Button("Hello world", on_press=button_handler)
#     button.style.padding = 50
#     button.style.flex = 1
#     box.add(button)

#     return box


# def main():
#     return toga.App("First App", "org.beeware.toga.tutorial", startup=build)


# if __name__ == "__main__":
#     main().main_loop()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'  # Arranges widgets vertically

        # Add a label
        self.label = Label(text="Welcome to the Kivy App!", font_size=24)
        self.add_widget(self.label)

        # Add a button
        self.button = Button(text="Click Me", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        self.button.bind(on_press=self.on_button_click)
        self.add_widget(self.button)

    def on_button_click(self, instance):
        self.label.text = "Button Clicked!"

class MyApp(App):
    def build(self):
        return MainWidget()

if __name__ == "__main__":
    MyApp().run()
