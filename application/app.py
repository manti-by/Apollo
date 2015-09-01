import pygtk
pygtk.require('2.0')

import gtk, gobject
import urllib2
from config import *


class Application():
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("Pybot Notification Panel")

        self.create_widgets()
        self.connect_signals()

        self.window.show_all()
        gtk.main()

    def create_widgets(self):
        self.vbox = gtk.VBox(spacing=10)

        self.hbox_1 = gtk.HBox(spacing=10)

        self.term_01 = gtk.Label('Term #1:')
        self.hbox_1.pack_start(self.term_01)

        self.term_02 = gtk.Label('Term #2:')
        self.hbox_1.pack_start(self.term_02)

        self.water_sensor = gtk.Label('Water Sensor:')
        self.hbox_1.pack_start(self.water_sensor)

        self.status = gtk.Label('Status:')
        self.hbox_1.pack_start(self.status)

        self.hbox_2 = gtk.HBox(spacing=10)

        self.button_exit = gtk.Button('Exit')
        self.hbox_2.pack_start(self.button_exit)

        self.vbox.pack_start(self.hbox_1)
        self.vbox.pack_start(self.hbox_2)

        self.window.add(self.vbox)

    def connect_signals(self):
        self.button_exit.connect('clicked', self.callback_exit)
        gobject.timeout_add_seconds(WORKER_FREQUENCY, self.callback_update)

    def callback_exit(self, widget):
        gtk.main_quit()

    def callback_update(self):
        try:
            data = urllib2.urlopen(WORKER_URL).read(1000)
            if data['status'] == 200:
                self.term_01.set_text('Term #1:' + str(data['result']['term_01']))
                self.term_02.set_text('Term #1:' + str(data['result']['term_02']))
                self.water_sensor.set_text('Water Sensor:' + str(data['result']['water_sensor']))
                self.status.set_text('Status: OK')
            else:
                self.status.set_text('Status: ERROR [' + data['message'] + ']')
        except Exception as e:
            self.status.set_text('Status: ERROR [' + e.message + ']')


if __name__ == "__main__":
    app = Application()
