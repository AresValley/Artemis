from collections import namedtuple

class Filters(object):
    def __init__(self, *all_filters):
        self.filter_widgets = all_filters

    def activate(self):
        for f in self.filter_widgets:
            f.setEnabled(True)

    def deactivate(self):
        for f in self.filter_widgets:
            f.setEnabled(False)
