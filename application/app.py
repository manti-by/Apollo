import pygtk
pygtk.require('2.0')

import gtk, gobject
import urllib2
from config import *


class Application():

    def __init__(self):
        # Build and show window
        self.builder = gtk.Builder()
        self.builder.add_from_file('window.glade')
        window = self.builder.get_object('window')
        window.show_all()
        gtk.main()

        # Add update every 5 seconds
        gobject.timeout_add_seconds(WORKER_FREQUENCY, self.callback_update)

    def elem(self, name):
        return self.builder.get_object(name)

    def callback_update(self):
        try:
            data = urllib2.urlopen(WORKER_URL).read(1000)
            if data['status'] == 200:
                self.elem('term_01').set_text(str(data['result']['term_01']))
                self.elem('pbar_01').set_fraction(float(data['result']['term_01'] / 100))

                self.elem('term_02').set_text(str(data['result']['term_02']))
                self.elem('pbar_02').set_fraction(float(data['result']['term_01'] / 100))

                self.elem('water_sensor').set_text('Water Sensor:' + ('yes' if data['result']['water_sensor'] else 'no'))

                self.elem('status').set_text('OK')
                self.elem('error').set_text('')
            else:
                self.elem('status').set_text('ERROR')
                self.elem('error').set_text(data['message'])
        except Exception as e:
            self.elem('status').set_text('ERROR')
            self.elem('error').set_text(e.message)


if __name__ == "__main__":
    app = Application()
