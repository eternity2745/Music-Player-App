import os
#os.environ["KIVY_VIDEO"] = "python-vlc"
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ShaderTransition
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.theming import ThemeManager
from kivymd.uix.button import *
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screenmanager import ScreenManager, MDScreenManager
from kivymd.uix.transition.transition import MDSwapTransition
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivymd.uix.screen import Screen, MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout 
from kivy.uix.video import Video
from kivymd.theming import ThemeManager
from kivymd.uix.gridlayout import MDGridLayout
from kivy.graphics import Color
from kivy.animation import Animation
from kivymd.toast import toast
from kivy.graphics import Rectangle
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.clock import Clock
import mysql.connector
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.image import Image
from kivymd.uix.fitimage import FitImage
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationDrawerHeader, MDNavigationDrawerItem, MDNavigationDrawerDivider, MDNavigationDrawerLabel, MDNavigationDrawerMenu, MDNavigationLayout
from kivymd.uix.list import OneLineListItem, ILeftBodyTouch
from kivymd.uix.list.list import MDList, TwoLineAvatarIconListItem, TwoLineRightIconListItem, ImageRightWidget, ImageLeftWidget
from kivy.uix.image import AsyncImage
from kivymd.uix.slider.slider import MDSlider
from kivy.core.audio import Sound, SoundLoader
from kivymd.uix.dialog import MDDialog
from kivy.uix.filechooser import FileChooserIconView
from kivymd.uix.sliverappbar.sliverappbar import MDSliverAppbarContent, MDSliverAppbarHeader, MDSliverAppbar
import pickle
from kivy_gradient import Gradient
import time
import asyncio
import openai
import datetime
from kivy.uix.actionbar import ActionView,ActionOverflow,ActionBar,ActionButton, ActionPrevious
from kivymd.uix.stacklayout import MDStackLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivymd.uix.button.button import MDFloatingActionButton
from plyer import filechooser
from kivy.uix.button import Button
from datetime import date
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.datatables import MDDataTable
from colorthief import ColorThief
from PIL import Image as Im

Config.set('graphics', 'fullscreen', 'auto')

x = 0
class Playlist(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.back = MDIconButton(icon='chevron-left', pos_hint = {'top':1, 'left':0.95})
        self.back.bind(on_press = self.new)
        self.add_widget(self.back)

        self.head = MDLabel(text="Playlists", pos_hint = {'top':0.95, 'right':0.53}, bold = True, font_style = "H3", size_hint = (0.5, 0.1))
        self.add_widget(self.head)

        self.scroll = MDScrollView(size_hint = (0.9,0.87), pos_hint = {'top':0.87, 'right':0.95}, scroll_wheel_distance = 5, scroll_type = ['bars', 'content'], smooth_scroll_end = 75,
                                        always_overscroll = False, bar_margin = 0.5, bar_width = 7, bar_inactive_color = [0,0,0,0])
        self.add_widget(self.scroll)

        self.sub_layout = MDStackLayout(spacing = "30dp", adaptive_height = True, width = dp(1000), padding = "20dp")
        self.scroll.add_widget(self.sub_layout)

        for i in range(x):
            self.card = MDCard(orientation = 'vertical', md_bg_color = (1,1,1,1), height = "350dp", width = "300dp", size_hint = (None , None), spacing = "10dp", padding = "20dp")
            self.sub_layout.add_widget(self.card)

            self.img = Image(source = 'images/Malikappuram.jpeg', pos_hint = {'center_x':0.5, 'center_y':0.5}, size_hint_y = 1, keep_ratio = False, allow_stretch = True)
            self.card.add_widget(self.img)

            self.play_name = MDLabel(text = "Playlist Name", bold = True, font_style = 'H5', size_hint_y = 0.2)
            self.card.add_widget(self.play_name)

            self.play_date = MDLabel(text = "05/03/2023", font_style = "Subtitle2", size_hint_y = 0.1)
            self.card.add_widget(self.play_date)

        self.create_play = MDFloatingActionButton(icon='plus', pos_hint = {'top':0.1, 'right':0.95}, elevation = 5, icon_size = "35dp")
        self.add_widget(self.create_play)
        self.create_play.bind(on_release = self.play_details)

    
    def new(self, dt):
        self.sub_layout.add_widget(MDCard(md_bg_color = (1,1,1,1), height = "350dp", width = "300dp", size_hint = (None , None)))

    def play_details(self, dt):
            self.main = MDBoxLayout(orientation="horizontal",
                    spacing="12dp",
                    size_hint_y=None,
                    height="200dp")
            self.upload = Button(background_normal = 'images/upload.png', on_press = self.choose, size_hint_x = 0.7, background_down = 'images/loading.png')
            self.main.add_widget(self.upload)

            self.play_n = MDTextField(
                        hint_text="Playlist Name",
                        pos_hint = {'center_y':0.5},
                        max_text_length = 30,
                        helper_text_mode = 'on_error'
                    )
            
            self.main.add_widget(self.play_n)
            self.dialog = MDDialog(
                title="Create Playlist",
                type="custom",
                auto_dismiss = False,
                content_cls = self.main,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release = self.cancel
                    ),
                    MDFlatButton(
                        text="CREATE",
                        on_release = self.create
                    ),
                ],
            )
            
            self.dialog.open()

    def choose(self, dt):
        self.play_img = filechooser.open_file()
        print(self.play_img)
        try:
          self.upload.background_normal = self.play_img[0]
        except:
            toast(text = "Unable to load image")
    
    def cancel(self, dt):
        self.dialog.dismiss()

    def create(self, dt):
        print(self.upload.state)
        if self.play_n.text != '' and self.upload.state == 'normal' and len(self.play_n.text) <= 30:
            today = date.today()
            t = today.strftime("%d/%m/%Y")

            self.card_new = MDCard(orientation = 'vertical', md_bg_color = (1,1,1,1), height = "350dp", width = "300dp", size_hint = (None , None), spacing = "10dp", padding = "20dp")
            self.sub_layout.add_widget(self.card_new)

            self.img_new = Image(source = (self.upload.background_normal if self.upload.background_normal != 'images/upload.png' else 'images/no img.png'), pos_hint = {'center_x':0.5, 'center_y':0.5}, size_hint_y = 1, keep_ratio = False, allow_stretch = True)
            self.card_new.add_widget(self.img_new)

            self.play_name_new = MDLabel(text = self.play_n.text, bold = True, font_style = 'H5', size_hint_y = 0.2)
            self.card_new.add_widget(self.play_name_new)

            self.play_date_new = MDLabel(text = t, font_style = "Subtitle2", size_hint_y = 0.1)
            self.card_new.add_widget(self.play_date_new)
            self.dialog.dismiss()
            toast(text = "Playlist Created")

'''
class Playlist_Songs(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main = MDSliverAppbar(toolbar_cls = second())
        self.add_widget(self.main)

        self.head = MDSliverAppbarHeader(size_hint_x = 0.1, spacing = "2dp")
        self.main.add_widget(self.head)

        self.layout1 = MDBoxLayout(orientation = 'horizontal', size_hint = (0.1,0.7), spacing = "1dp", pos_hint = {'center_x':0.6, 'center_y':0.5}, padding = "5dp")
        self.head.add_widget(self.layout1)

        self.bg = Image(source = "images/Malikappuram.jpeg", size_hint_x = 2)
        self.layout1.add_widget(self.bg)
        print(self.bg.color)

        self.sub_layout = MDBoxLayout(orientation='vertical', pos_hint = {'left':0.1, 'center_y':0.5}, spacing = "5dp", padding = "70dp", size_hint_x = 8)
        self.layout1.add_widget(self.sub_layout)

        self.title = MDLabel(text = "Playlist Name", font_style = "H4", bold = True)
        self.sub_layout.add_widget(self.title)

        self.date = MDLabel(text="11/03/2023")
        self.sub_layout.add_widget(self.date)

        self.fake_label1 = MDLabel(text='', size_hint_x = 5)
        self.layout1.add_widget(self.fake_label1)

        self.cont = MDSliverAppbarContent(
            orientation = 'vertical',
            padding = '20dp',
            spacing = "12dp",
            adaptive_height = True,
            #adaptive_width = True
        )
        self.main.add_widget(self.cont)
        self.sub = MDBoxLayout()
        self.cont.add_widget(self.sub)
        self.table = MDDataTable(
            pos_hint = {'top':0.7, 'center_x':0.7}, 
            column_data=[
                ("#", dp(20)),
                ("Title", dp(50)),
                ("Authors", dp(50)),
                ("Date Added", dp(50)),
                ("Duration", dp(30)),
                ("extras", dp(30))
            ],
            row_data=[
                (
                    "1",
                    "Song Name",
                    "Author Name 1 , Author Name 2 , Author Name 3",
                    "11/03/2023",
                    "04:23",
                    "0:33",
                )
            ],
        rows_num = 1000
        )
        self.sub.add_widget(self.table)
        for i in range(20):
            self.table.row_data.append((
                    "1",
                    "Song Name",
                    "Author Name 1 , Author Name 2 , Author Name 3",
                    "11/03/2023",
                    "04:23",
                    "0:33",
                ))
            
        print(self.table.row_data)

class second(MDTopAppBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = "Playlist Name"
        self.type_height = "medium"
        self.shadow_color = (0, 0, 0, 0)
        self.left_action_items = [["arrow-left"]]
        

        #self.top = MDSliverAppbar(toolbar_cls = SliverToolbar(), background_color = "2d4a50")
        #self.add_widget(self.top)
        #self.top.add_widget(MDSliverAppbarHeader(FitImage(source = 'images/Malikappuram.jpeg')))    
'''

class Playlist_Songs(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hex = self.colour_extractor('images/Malikappuram.jpeg')
        print(self.hex)

        with self.canvas:
            #print(self.layout.pos, self.size)
            #Color(self.constants[0][0]+self.constants[1][0],
            #      self.constants[0][1]+self.constants[1][1],
            #      self.constants[0][2]+self.constants[1][2],
            #         mode='rgb')
            Color(0.5,0.5,0.5,
                    mode='hex')
            Rectangle(texture = Gradient.vertical(get_color_from_hex(self.hex[1]), get_color_from_hex(self.hex[0])),
                       pos=[0,-8], size=[2000,1000])

        self.bar = MDTopAppBar(title = "Playlist Name", shadow_color = (0,0,0,0), left_action_items = [["arrow-left"]], pos_hint = {'top':1})
        self.add_widget(self.bar)

        self.scroll = MDScrollView(pos_hint = {'top':0.93}, scroll_wheel_distance = 5, scroll_type = ['bars', 'content'], smooth_scroll_end = 75,
                                        always_overscroll = False, bar_margin = 0.5, bar_width = 7, bar_inactive_color = [0,0,0,0])
        self.add_widget(self.scroll)

        self.main = MDBoxLayout(orientation = 'vertical', spacing = "1dp", size_hint_y = None, adaptive_height = True, padding = [0,0,0,100])
        self.scroll.add_widget(self.main)

        #with self.canvas:
        #self.rect = Rectangle(texture = Gradient.horizontal(get_color_from_hex('#000000'), get_color_from_hex('#00FF00')), size = self.size, pos = self.pos)

        self.layout = MDBoxLayout(orientation = 'horizontal', pos_hint = {'top':0.95}, size_hint_y = None, height = "300dp", size_hint_x = 0.4, spacing = "2dp")
        self.main.add_widget(self.layout)
        self.layout_sub = MDBoxLayout(orientation = 'horizontal', size_hint_y = None, height = "100dp", size_hint_x = 0.33, padding = [0,0,200,0], pos_hint = {'center_x':0.2}, spacing = "20dp")
        self.main.add_widget(self.layout_sub)

        #self.hex = self.colour_extractor('images/Manichithrathazhu.jpeg')
        #print('g', self.hex)
        #self.constants = (get_color_from_hex(self.hex[0]), get_color_from_hex('#000000'))
        #print(self.constants)

        self.bg = Image(source="images/Malikappuram.jpeg", pos_hint = {'right':0.7, 'center_y':0.5}, size_hint_x = 0.5)#, width = "248dp", height = "248dp", size_hint = (None, None))
        print(self.bg.texture.size)
        if self.bg.texture.size != (248,248):
            image = Im.open('images/bheeshma parvam.jpg')
            new = image.resize((248, 248))
            print(new)
            new.save('images/bheeshma parvam-new.jpg')
            self.bg.source = 'images/bheeshma parvam-new.jpg'
        self.layout.add_widget(self.bg)

        self.sub_layout1 = MDBoxLayout(orientation = 'vertical', size_hint = (0.5,0.2), pos_hint = {'right':0.6, 'center_y':0.5}, spacing = "50dp")
        self.layout.add_widget(self.sub_layout1)

        self.song_name = MDLabel(text="Song Name, Song Name, Song Name", font_style = "H4", bold = True)
        self.sub_layout1.add_widget(self.song_name)

        self.song_author = MDLabel(text= "Song Authors, Song Authors, Song Authors", font_style = "Subtitle1")
        self.sub_layout1.add_widget(self.song_author)

        self.icon1 = MDIconButton(icon = 'delete', pos_hint = {'top':1}, icon_size = "35dp", md_bg_color = [0,1,1,0.5])
        self.layout_sub.add_widget(self.icon1)
        self.icon2 = MDIconButton(icon = 'play', pos_hint = {'top':1}, icon_size = "35dp", md_bg_color = [0,1,1,0.5])
        self.layout_sub.add_widget(self.icon2)
        self.icon3 = MDIconButton(icon = 'play', pos_hint = {'top':1}, icon_size = "35dp", md_bg_color = [0,1,1,0.5])
        self.layout_sub.add_widget(self.icon3)
        self.icon4 = MDIconButton(icon = 'play', pos_hint = {'top':1}, icon_size = "35dp", md_bg_color = [0,1,1,0.5])
        self.layout_sub.add_widget(self.icon4)

        self.layout2 = MDBoxLayout(orientation = 'vertical', spacing = "20dp", padding = "20dp", size_hint_y = None, adaptive_height = True)
        self.main.add_widget(self.layout2)

        self.number = MDLabel(text='')
        self.img = Image(source='images/Malikappuram.jpeg')
        self.s_name = MDLabel(text="Nangeli Poove")
        self.auth_name = MDLabel(text="Ranjin Raj, Ranjin Raj, Ranjin Raj")
        self.duration = MDLabel(text="07:14")
        self.icon = MDIconButton(icon='three-dots')


        for i in range(1,11):
            self.card = MDCard(size_hint_y = None, orientation='horizontal', padding = [50,10,50,10], height="150dp", radius = 20, size_hint_x = 0.85, pos_hint = {'center_x':0.5})
            self.layout2.add_widget(self.card)
            self.number.text = f"{i}"
            self.card.add_widget(MDLabel(text=f"{i}", size_hint_x = 0.1, font_style = "H5"))
            self.card.add_widget(Image(source='images/Charlie.png'))
            self.card.add_widget(MDLabel(text="Nangeli Poove, Thathaka Theithare", font_style = 'H5'))
            self.card.add_widget(MDLabel(text="Ranjin Raj, Ranjin Raj, Ranjin Raj", font_style = "H5"))
            self.card.add_widget(MDLabel(text='', size_hint_x = 0.4))
            self.card.add_widget(MDLabel(text="07:14", pos_hint = {'center_x':0.5}, font_style = "H5", size_hint_x = 0.7))
            self.card.add_widget(MDIconButton(icon='delete', pos_hint = {'center_y':0.5}, size_hint_x = 0.2))

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb
    
    def colour_extractor(self, path):
        color_thief = ColorThief(path)
        palette = color_thief.get_palette(color_count=2)
        print(palette)
        l = []

        for i in palette:
            l.append(self.rgb_to_hex(i))
        
        return l

'''
        self.table = MDDataTable(
            size_hint = (0.7,1),
            pos_hint = {'center_y':0.8, 'center_x':0.5},
            background_color_cell = [1,0,0,1],
            column_data=[
                ("#", dp(55)),
                ("Title", dp(75)),
                ("Authors", dp(75)),
                ("Date Added", dp(75)),
                ("Duration", dp(75)),
                ("", dp(10))
            ],
            row_data=[
                (
                    "1",
                    "Song Name",
                    "Author Name 1 , Author Name 2 , Author Name 3",
                    "11/03/2023",
                    "04:23",
                    "0:33",
                )
            ],
        rows_num = 1000
        )
        self.main.add_widget(self.table)
        for i in range(20):
            self.table.row_data.append((
                    f"{i+2}",
                    "Song Name",
                    "Author Name 1 , Author Name 2 , Author Name 3",
                    "11/03/2023",
                    "04:23",
                    "0:33",
                ))'''



#class SM(MDScreenManager):  
##    def get_classes(self):  
 #       return {screen.__class__.__name__: screen.__class__.__module__ for screen in self.screens}

class Test(MDApp):

    def build(self):
       self.theme_cls.theme_style = "Dark"
       self.theme_cls.primary_hue = "500"
       self.theme_cls.primary_palette = "Blue"

       self.sm = MDScreenManager()
       self.sm.add_widget(Playlist_Songs(name='playlist'))
       return self.sm
       #self.fps_monitor_start()     
       


if __name__ == '__main__':
    Test().run()