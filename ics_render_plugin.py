import gi
gi.require_version ('Astroid', '0.2')
gi.require_version ('Gtk', '3.0')
gi.require_version ('GMime', '3.0')

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Astroid
from gi.repository import GMime

import email
#from email.mime.text import MIMEText
import icalendar
import mutt_ics

from email.policy import default

class IcsRenderPlugin(GObject.Object, Astroid.Activatable):
    def do_activate(self):
        print('ics: activated')

    def do_deactivate(self):
        print('ics: deactivated')

    def do_process(self, fname):
        print("ics: processing " + fname)
        with open(fname, 'rb') as fp:
            msg = email.message_from_binary_file(fp, policy = default)
            for pt in msg.walk():
                if pt.get_content_type() == 'text/calendar':
                    body = pt.get_content()
                    #print('ics: body', body)
                    ics_text = mutt_ics.get_ics_text(body)
                    cal = icalendar.Calendar.from_ical(ics_text)
                    pt.set_content(mutt_ics.get_interesting_stuff(cal))
                    #pt.set_type('text/plain')

            return GMime.StreamMem.new_with_buffer(msg.as_bytes())

# vi:set ts=4 sw=4 et
