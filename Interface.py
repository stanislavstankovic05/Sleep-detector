import json

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner

Window.clearcolor = (0.2, 0.2, 0.2, 1)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, padding=20, size_hint=(0.5, 0.6))
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        button_color = (0.4, 0.6, 0.9, 1)

        layout.add_widget(Label(text="WakeUp", font_size=32, bold=True, size_hint=(1, 0.3)))
        layout.add_widget(Label(text="Menu", font_size=24, size_hint=(1, 0.2)))

        layout.add_widget(ToggleButton(
            text="Start", state='normal',
            on_press=self.toggle,
            background_normal='', background_color=button_color
        ))

        about_button = Button(
            text="About",
            background_normal='', background_color=button_color
        )
        about_button.bind(on_press=self.open_about)
        layout.add_widget(about_button)

        settings_button = Button(
            text="Settings",
            background_normal='', background_color=button_color
        )
        settings_button.bind(on_press=self.open_settings)
        layout.add_widget(settings_button)

        layout.add_widget(Button(
            text="Exit",
            on_press=self.exit_app,
            background_normal='', background_color=button_color
        ))

        self.add_widget(layout)

    def toggle(self, instance):
        if instance.state == 'down':
            instance.text = "Stop"
        else:
            instance.text = "Start"

    def exit_app(self, instance):
        App.get_running_app().stop()

    def open_about(self, instance):
        self.manager.current = 'about'

    def open_settings(self, instance):
        self.manager.current = 'settings'

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="This is the About Page", font_size=32, pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        layout.add_widget(Button(
            text="Back to Menu",
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=self.go_back
        ))
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'menu'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=10, padding=20, size_hint=(0.8, 0.5))
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        layout.add_widget(Label(text="Choose your settings", font_size=24, size_hint=(1, 0.2)))

        row_layout = GridLayout(cols=3, spacing=10, size_hint=(1, 0.2))
        row_layout.add_widget(Label(text="Time: ", font_size=18, halign='left', valign='middle'))

        hour_values = [str(i).zfill(2) for i in range(24)]
        minute_values = [str(i).zfill(2) for i in range(60)]

        self.hour_spinner = Spinner(
            text="00", values=hour_values,
            size_hint=(None, None), size=(80, 40)
        )
        self.minute_spinner = Spinner(
            text="00", values=minute_values,
            size_hint=(None, None), size=(80, 40)
        )

        spinner_row = GridLayout(cols=2, spacing=10, size_hint=(None, None), size=(180, 40))
        spinner_row.add_widget(self.hour_spinner)
        spinner_row.add_widget(self.minute_spinner)

        row_layout.add_widget(spinner_row)
        layout.add_widget(row_layout)

        save_button = Button(
            text="Save Alarm Time",
            size_hint=(0.4, 0.15),
            pos_hint={'center_x': 0.5},
            on_press=self.save_alarm_time
        )
        layout.add_widget(save_button)

        back_button = Button(
            text="Back to Menu",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5},
            on_press=self.go_back
        )
        layout.add_widget(back_button)

        self.add_widget(layout)

    def save_alarm_time(self, instance):
        hour = self.hour_spinner.text
        minute = self.minute_spinner.text
        alarm_data={
            "hour": hour,
            "minute": minute
        }
        with open('alarm_time.json', 'w') as f:
            json.dump(alarm_data, f)

        print(f"Alarm time saved: {hour}:{minute}")
        print(f"Alarm time saved: {hour}:{minute}")

    def go_back(self, instance):
        self.manager.current = 'menu'

class MyApp(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(MenuScreen(name='menu'))
        manager.add_widget(AboutScreen(name='about'))
        manager.add_widget(SettingsScreen(name='settings'))
        return manager

if __name__ == "__main__":
    MyApp().run()
