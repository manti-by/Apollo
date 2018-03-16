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
from kivymd.label import MDLabel
from kivymd.textfields import MDTextField

from layout import main_widget


class ApolloNavDrawer(MDNavigationDrawer):
    pass


class ApolloApp(App):

    title = 'Apollo IoT Client'
    icon = 'assets/icon.png'

    theme_cls = ThemeManager()
    nav_drawer = ObjectProperty()

    def get_data(self, server_url):
        result = urlparse(server_url)
        if result.scheme and result.netloc:
            try:
                r = requests.get(self.server_url.text, timeout=3)
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
        label = MDLabel(font_style='Body1',
                        theme_text_color='Secondary',
                        text='Server address',
                        valign='top')

        input = MDTextField(hint_text='No helper text')

        dialog = MDDialog(title='Enter server address',
                          size_hint=(.8, None),
                          height=dp(250),
                          auto_dismiss=False)

        dialog.add_widget(label)
        dialog.add_widget(input)

        dialog.add_action_button('Dismiss',
                                 action=lambda *x: dialog.dismiss())
        dialog.open()

    def show_about_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="About this app text.",
                          valign='top')

        content.bind(size=content.setter('text_size'))
        self.dialog = MDDialog(title="About this app",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def build(self):
        return Builder.load_string(main_widget)


if __name__ == '__main__':
    ApolloApp().run()
