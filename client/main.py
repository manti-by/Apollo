from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class IoTClient(App):
    title = 'IoT Client'
    icon = 'icon.png'

    def build(self):
        layout = GridLayout(cols=2)
        initial_data = {
            'Guest Room': {'temp': 22.5, 'humidity': 75.2},
            'Bedroom': {'temp': 25.1, 'humidity': 94.9},
            'Work Room': {'temp': 20.8, 'humidity': 55.7}
        }
        for room, data in initial_data:
            cell = GridLayout(rows=2)
            cell.add_widget(Label(text=room))
            cell.add_widget(Label(text='T: {}{}C, H: {}%'.format(data['temp'], chr(223), data['humidity'])))
            layout.add_widget(cell)
        layout.add_widget(Button(text='Refresh'))
        return layout


IoTClient().run()
