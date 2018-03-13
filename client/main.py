import json
import requests
from urllib.parse import urlparse

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView


class ApolloLayout:

    def __init__(self):
        self.data = {
            'Guest Room': {'temp': 22.5, 'humidity': 62.2},
            'Work Room': {'temp': 20.8, 'humidity': 55.7},
            'Bedroom': {'temp': 21.1, 'humidity': 57.1},
            'Bathroom': {'temp': 25.1, 'humidity': 94.9},
            '2nd Floor': {'temp': 23.7, 'humidity': 69.3},
        }
        self.server_url = TextInput(text='http://192.168.0.112')
        self.layout = self.build()

    def update_data(self):
        r = requests.get(self.server_url.text, timeout=3)
        response = json.loads(r.json())
        if r.status_code != 200 or response['result'] != 200:
            reason = r.reason if r.status_code != 200 else response['message']
            raise 'Get data from server failed [{}]'.format(reason)
        self.data = response['data']

    def refresh(self, button_instance):
        result = urlparse(self.server_url.text)
        if result.scheme and result.netloc:
            try:
                self.update_data()
                self.build()
                return
            except requests.exceptions.ConnectionError:
                text = 'Server not responding'
            except Exception as e:
                text = str(e)
        else:
            text = 'Url is not valid'
        view = ModalView()
        view.add_widget(Label(text=text))
        view.open()

    def build(self):
        layout = GridLayout(cols=1)
        for room, data in self.data.items():
            cell = GridLayout(cols=2)
            cell.add_widget(Label(text=room))
            cell.add_widget(Label(text='T: {0:.0f}{1}C, H: {2:.0f}%'.format(data['temp'], chr(176), data['humidity'])))
            layout.add_widget(cell)

        layout.add_widget(self.server_url)
        button = Button(text='Refresh')
        button.bind(on_press=self.refresh)
        layout.add_widget(button)
        return layout


class ApolloApp(App):
    title = 'Apollo IoT Client'
    icon = 'assets/icon.png'

    def build(self):
        return ApolloLayout().layout


if __name__ == '__main__':
    ApolloApp().run()
