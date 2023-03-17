from kivy.app import App
from kivy.clock import Clock, _default_time as time  # ok, no better way to use the same clock as kivy, hmm
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.properties import ListProperty

from threading import Thread
from time import sleep

MAX_TIME = 5.

kv = '''
BoxLayout:
    ScrollView:
        GridLayout:
            cols: 1
            id: target
            size_hint: 1, None
            height: self.minimum_height

    MyButton:
        text: 'run'

<MyLabel@Label>:
    size_hint_y: None
    height: self.texture_size[1]
'''

class MyButton(Button):
    def on_press(self, *args):
        x = Thread(target=self.worker, daemon=True, name='monitor').start()

    def worker(self):
        sleep(5) # blocking operation
        App.get_running_app().consommables.append("done")

class PubConApp(App):
    consommables = ListProperty([])

    def build(self):
        Clock.schedule_interval(self.consume, 0)
        return Builder.load_string(kv)

    def consume(self, *args):
            if len(self.consommables) > 0:
                item = self.consommables.pop(0)  # i want the first one
                label = Factory.MyLabel(text=item)
                self.root.ids.target.add_widget(label)

if __name__ == '__main__':
    PubConApp().run()
    
