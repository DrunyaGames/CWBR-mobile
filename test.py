from __future__ import print_function
#
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivydnd.dragndropwidget import DragNDropWidget
#
#
kv = '''
FloatLayout:
    BoxLayout:
        id: from_box
        canvas:
            Color:
                rgb: 1, 0.2, 0.2
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: 0.8, 0.25
        pos_hint: {'x': 0.1, 'y': 0.4}
        # Here's our DragNDropWidget. See below for the class declaration.
        DraggableButton:
            text: 'Button 1'
            droppable_zone_objects: [upper_to_box]
            drop_func: app.greet
            failed_drop_func: app.oops
            size_hint: None, None
            size: 100, 100 
    Label:
        id: upper_to_box
        text: 'drop here'
        canvas.before:
            Color:
                rgb: 0.4, 0.4, 1
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: 0.8, 0.2
        pos_hint: {'x': 0.1, 'y': 0.8}
'''
#
#
class  DraggableButton(Button, DragNDropWidget):
    def __init__(self, **kw):
        super(DraggableButton, self).__init__(**kw)
#
#
class DnDExample1(App):
    def __init__(self, **kw):
        super(DnDExample1, self).__init__(**kw)

    def build(self):
        return Builder.load_string(kv)

    def greet(self, calling_widget):
        print ("App says: Nicely Dropped!!")

    def oops(self, the_widget=None, parent=None, kv_root=None):
        print("App says: Ooops! Can't drop there!")


if __name__ == '__main__':
    DnDExample1().run()
