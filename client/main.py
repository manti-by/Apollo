from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class IoTClient(App):
    title = 'Apollo IoT Client'
    icon = 'assets/icon.png'

    def build(self):
        initial_data = {
            'Guest Room': {'temp': 22.5, 'humidity': 62.2},
            'Work Room': {'temp': 20.8, 'humidity': 55.7},
            'Bedroom': {'temp': 21.1, 'humidity': 57.1},
            'Bathroom': {'temp': 25.1, 'humidity': 94.9},
            '2nd Floor': {'temp': 23.7, 'humidity': 69.3},
        }
        layout = GridLayout(cols=1)
        for room, data in initial_data.items():
            cell = GridLayout(cols=2)
            cell.add_widget(Label(text=room))
            cell.add_widget(Label(text='T: {0:.0f}{1}C, H: {2:.0f}%'.format(data['temp'], chr(176), data['humidity'])))
            layout.add_widget(cell)
        layout.add_widget(Button(text='Refresh'))
        return layout


if __name__ == '__main__':
    IoTClient().run()
