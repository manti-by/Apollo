import json
import requests
from urlparse import urlparse

from kivy.app import App
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivymd.navigationdrawer import MDNavigationDrawer

from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField

from layout import main_widget


class ApolloNavDrawer(MDNavigationDrawer):
    pass


class ApolloApp(App):

    title = 'Apollo IoT Client'
    icon = 'assets/icon.png'

    theme_cls = ThemeManager()
    nav_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super(ApolloApp, self).__init__(**kwargs)

        self.address_dialog = MDDialog(title='Enter server address',
                                       size_hint=(.8, None),
                                       height=dp(250),
                                       auto_dismiss=False)

        self.address_input = MDTextField(hint_text='192.168.0.112')
        self.address_dialog.add_widget(self.address_input)
        self.address_dialog.add_action_button('Save',
                                              action=lambda *x: self.address_dialog.dismiss())

    def update_data_table(self):
        result = urlparse(self.address_input.text)
        if result.scheme and result.netloc:
            try:
                r = requests.get(self.address_input.text, timeout=3)
                response = json.loads(r.json())
                if r.status_code != 200 or response['result'] != 200:
                    reason = r.reason if r.status_code != 200 else response['message']
                    raise 'Get data from server failed [{}]'.format(reason)
                return response['data']
            except requests.exceptions.ConnectionError:
                pass
            except Exception:
                pass
        return None

    def show_server_address_dialog(self):
        self.address_dialog.open()

    def build(self):
        return Builder.load_string(main_widget)


if __name__ == '__main__':
    ApolloApp().run()
