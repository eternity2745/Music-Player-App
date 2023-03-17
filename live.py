from kaki.app import App 
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

class Playlist_Songs(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.but = Button(text="hai")
        self.add_widget(self.but)


class MDLive(App):
    print(1)
    CLASSES = {
        "Playlist_Songs":"live"
    }
    print(2)

    AUTORELOADER_PATH = [
        (".", {"recursive": True})
    ]
    print(3)
    def build_app(self, *args):
        print("Inside")
        #self.theme_cls.theme_style = "Light"

        return Factory.Playlist_Songs()

MDLive().run()
