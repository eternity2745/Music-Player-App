import os
#os.environ["KIVY_VIDEO"] = "python-vlc"
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
from kivy.graphics.vertex_instructions import Rectangle
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
from kivy.uix.image import AsyncImage
import datetime
from kivymd.uix.slider.slider import MDSlider
from kivy.core.audio import Sound, SoundLoader
from kivymd.uix.list import OneLineListItem, ILeftBodyTouch
from kivymd.uix.list.list import MDList, TwoLineAvatarIconListItem, TwoLineRightIconListItem, ImageRightWidget, ImageLeftWidget, IconRightWidget
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.effects.kinetic import KineticEffect
from kivy.uix.actionbar import ActionBar
from kivy.properties import StringProperty
import pickle
from kivy_gradient import Gradient
from kivymd.uix.selectioncontrol.selectioncontrol import MDSwitch
import time
import asyncio
import openai
import plyer
from plyer import notification
from pydub import AudioSegment
from os import listdir
import numpy as np
import math
from threading import Thread
from kivy.clock import _default_time as time
from kivymd.uix.stacklayout import MDStackLayout
from plyer import filechooser
from datetime import date
from colorthief import ColorThief
from PIL import Image as Im
from kivymd.uix.menu import MDDropdownMenu

#Window.fullscreen = 'auto'
#Window.borderless = True

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', -1500)
Config.set('graphics', 'top',  1000)
Config.set('graphics', 'resizable', 'False')
Config.set('graphics', 'borderless',  1)
Config.set('graphics', 'width', 0)
Config.set('graphics', 'height', 0)


account = ("","","")
state = 0
logged_in = False

class Database():
    cnx = None
    cursor = None
    def connect():   
        global cnx
        global cursor
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            database="musicplayer"
        )
        cursor = cnx.cursor()
        
    def create_account(username, email, phone, password):
        cursor.execute('INSERT INTO users (username, email, phone, password) VALUES (%s, %s, %s, %s)', (username, email, phone, password))
        cnx.commit()
        global account
        global logged_in
        cursor.execute('SELECT username, email, password FROM users WHERE email=%s AND password = %s', (email, password))
        account = cursor.fetchone()
        logged_in = True
        return True, account
        
    def login(email, password):
        cursor.execute('SELECT username, email, password FROM users WHERE email=%s AND password = %s', (email, password))
        global account
        global logged_in
        account = cursor.fetchone()
        if account:
            print("Login successful.")
            logged_in = True
            return True, account
        else:
            print("Incorrect username or password.")
            return False

    def acc_details():
        if logged_in:
           return account
        
    def music(limit):
        cursor.execute(f"SELECT * FROM songs ORDER BY RAND() LIMIT {limit}")
        result = cursor.fetchall()
        return result
    
    def get_song_detail(name = None, id = None):
      try:
        if name:
            cursor.execute("SELECT * FROM songs WHERE title = %s", (name,))
            result = cursor.fetchone()
            return result
        elif id:
            cursor.execute("SELECT * FROM songs WHERE id = %s", (id, ))
            result = cursor.fetchone()
            return result
      except:
        return "None"
    
    def song_match(text):
        try:
            cursor.execute(f"SELECT * FROM songs WHERE title LIKE '%{text}%'")
            result = cursor.fetchall()
            return result
        except:
            return None
        
    def playlists_info(username):
        try:
            cursor.execute("SELECT * FROM playlists WHERE user = %s", (username, ))
            result = cursor.fetchall()
            return result
        except:
            return 0
    
    def create_playlist(name, image, user, date):
        try:
            cursor.execute("INSERT INTO playlists (name, image, user, created) VALUES (%s, %s, %s, %s)", (name, image, user, date))
            cnx.commit()
        except:
            raise Exception
    
    def playlist_songs(id):
        try:
            cursor.execute("SELECT * FROM playlist_songs WHERE playlist_id = %s", (id, ))
            result = cursor.fetchall()
            return result
        except Exception:
            raise Exception
        
    def add_playlist_song(playlist_id, song_id):
        today = date.today().strftime("%d/%m/%Y")

        try:
            cursor.execute("INSERT INTO playlist_songs (playlist_id, song_id, created) VALUES (%s, %s, %s)", (playlist_id, song_id, today))
            cnx.commit()
        except Exception:
            raise Exception


class WelcomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.video = Video(source="D:\\Music Player App\\login.mp4", options = {'eos': 'loop', 'allow_stretch': True, 'keep_ratio' : True})
        self.video.state = 'play'
        self.add_widget(self.video)

        self.welc = MDBoxLayout(orientation='vertical', 
                                      size_hint = (0.37, 0.37), 
                                      pos_hint = {'center_x':0.5, 'center_y':0.5}, spacing = 20, padding = 20)

        self.img = Image(source = "D:/Chapt 5 Python/Aeris1.png", pos_hint = {'center_x':0.5, 'center_y': 0.8}, size_hint=(1, 1.5))
        self.welc.add_widget(self.img)
        self.per = MDLabel(text="Perilla", font_size='300sp', halign='center', size_hint = (1,0.4))
        self.welc.add_widget(self.per)

        self.welc_button = MDRectangleFlatButton(text="Welcome", pos_hint = {'center_x':0.5}, size_hint = (.5,.5))
        self.welc_button.bind(on_release=lambda p:self.next())
        self.welc.add_widget(self.welc_button)

        self.add_widget(self.welc)

    def next(self):
        self.video.state = 'stop'
 
        self.manager.current = 'login'


class LoginScreen(MDScreen, MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.login_form = MDBoxLayout(orientation='vertical', 
                                      size_hint = (0.5, 0.5), 
                                      pos_hint = {'center_x':0.5, 'center_y':0.5})


        self.email = MDTextField(hint_text="Email", helper_text = "Invalid Email", helper_text_mode = 'on_error', line_anim = True)
        self.password = MDTextField(hint_text="Password", password=True, helper_text = "Invalid Password", helper_text_mode = 'on_error', line_anim = True)

        self.login_form.add_widget(self.email)
        self.login_form.add_widget(self.password)

        self.login_button = MDRectangleFlatButton(text="Login", pos_hint={'center_x':0.5, 'center_y':0.6})
        self.login_button.bind(on_press=lambda x:self.login())
        self.login_form.add_widget(self.login_button)
        self.create_account_button = MDRectangleFlatButton(text="Create Account", pos_hint={'center_x':0.5, 'center_y': 0.8})
        self.create_account_button.bind(on_release=lambda y: self.reg())

        self.login_form.add_widget(self.create_account_button)

        self.add_widget(self.login_form)

    def login(self):
        status = Database.login(email = self.email.text, password = self.password.text)
        print(status)
        if status:
            print('Logged in')
            self.manager.add_widget(MainScreen(name='main'))
            self.manager.current = 'main'
        else:
            self.email.error = True
            self.password.error = True
            print('Incorrect Email or password')

    def reg(self):
        self.manager.current = 'registration'

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            print(self.pos, self.size, Window.size)
            Color(0,0,0.3, mode = 'hex')
            self.rect = Rectangle(texture = Gradient.vertical([0,0,0.3,0.3], [0,0,0.5,0.5], [0,0,1,0.5]),
                     size=Window.size)
        Window.bind(on_resize = self.resize)
        #global logged_in
        #if logged_in:

        account = Database.acc_details()
        self.sound = None
        self.paused = True
        self.song_name = None
        self.prev_sn = None
        self.song_author = StringProperty()
        self.song_image = 'None'
        self.counter = 0

        self.top_bar = MDTopAppBar(left_action_items=[['menu',lambda x: self.nav_drawer.set_state('open'), "Menu"]],
                                   title = "Music Player",
                                   right_action_items=[['magnify',lambda x: self.search(), "Search"],['tools',lambda x: x]], pos_hint = {'top':1.0})
        self.add_widget(self.top_bar)

        self.nav_drawer = MDNavigationDrawer(enable_swiping = True, spacing = dp(25))
        self.nav_menu = MDNavigationDrawerMenu(spacing = dp(35))

        self.nav_header = MDNavigationDrawerHeader(title = account[0], text = account[1], title_color = "#FFFFFF")  
        self.nav_menu.add_widget(self.nav_header)

        self.nav_playlist = MDNavigationDrawerItem(text='Account', icon = "account", text_color = "#FFFFFF", icon_color = "#FFFFFF", selected_color = "#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)

        self.nav_playlist = MDNavigationDrawerItem(text='Playlist', icon = "playlist-music", text_color = "#FFFFFF", icon_color = "#FFFFFF", selected_color = "#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)
        self.nav_playlist.bind(on_release = self.to_playlist)

        self.nav_text_art = MDNavigationDrawerItem(text='AI Text Art', icon = "image-text", text_color = "#FFFFFF", icon_color = "#FFFFFF", selected_color = "#FFFFFF")
        self.nav_text_art.bind(on_release = self.to_textart)
        self.nav_menu.add_widget(self.nav_text_art)

        self.nav_text_art = MDNavigationDrawerItem(text='Jaadhu', icon = "robot", text_color = "#FFFFFF", icon_color = "#FFFFFF", selected_color = "#FFFFFF")
        self.nav_menu.add_widget(self.nav_text_art)
        
        self.nav_divider = MDNavigationDrawerDivider()
        self.nav_menu.add_widget(self.nav_divider)

        self.nav_settings = MDNavigationDrawerItem(text='Enikkariyilla', icon = "incognito", text_color = "#FFFFFF", icon_color = "#FFFFFF", selected_color = "#FFFFFF")
        self.nav_menu.add_widget(self.nav_settings)
        
        self.nav_settings = MDNavigationDrawerItem(text='Settings', icon = "tools", text_color = "#FFFFFF", icon_color = "#FFFFFF", selected_color = "#FFFFFF")
        self.nav_menu.add_widget(self.nav_settings)

        self.nav_logout = MDNavigationDrawerItem(text='Logout', icon = "logout", text_color = "#FFFFFF", icon_color = "#FFFFFF", selected_color = "#FFFFFF")
        self.nav_logout.bind(on_release = self.logout)
        self.nav_menu.add_widget(self.nav_logout)

        self.nav_layout = MDNavigationLayout()
        self.nav_drawer.add_widget(self.nav_menu)
        self.nav_layout.add_widget(self.nav_drawer)


        self.scroll_view = MDScrollView(do_scroll_x = False, pos_hint = {'top':0.93}, size_hint_y = 0.9, scroll_wheel_distance = 5, scroll_type = ['bars', 'content'], smooth_scroll_end = 75,
                                        always_overscroll = False, bar_margin = 0.5, bar_width = 7, bar_inactive_color = [0,0,0,0])
        self.add_widget(self.scroll_view)

        self.main_layout = MDBoxLayout(orientation='vertical', size_hint_y = None, height = "1800dp", width = "50dp", spacing = "10dp", padding = "20dp")
        self.scroll_view.add_widget(self.main_layout)

        self.recommended_section = MDGridLayout(size_hint_y = 5, width = Window.minimum_width, cols = 10, spacing = "20dp", padding = "20dp")
        self.recommended_label = MDLabel(text='Recommended Songs', font_style='H4', size_hint_y = None, height = Window.minimum_height, bold = True)
        self.main_layout.add_widget(self.recommended_label)
        self.main_layout.add_widget(self.recommended_section)

        self.malayalam_section = MDGridLayout(size_hint_y = 5, width = Window.minimum_width, cols = 10, spacing = "20dp", padding = "20dp")
        self.malayalam_label = MDLabel(text='Malayalam Songs', font_style='H4', size_hint_y = None, height = Window.minimum_height, bold = True)
        self.main_layout.add_widget(self.malayalam_label)
        self.main_layout.add_widget(self.malayalam_section)

        self.english_section = MDGridLayout(size_hint_y = 5, width = Window.minimum_width, cols = 10, spacing = "20dp", padding = "20dp")
        self.english_label = MDLabel(text='English Songs', font_style='H4', size_hint_y = None, height = Window.minimum_height, bold = True)
        self.main_layout.add_widget(self.english_label)
        self.main_layout.add_widget(self.english_section)


        self.hindi_section = MDGridLayout(size_hint_y = 5, width = Window.minimum_width, cols = 10, spacing = "20dp", padding = "20dp")
        self.hindi_label = MDLabel(text='Hindi Songs', font_style='H4', size_hint_y = None, height = Window.minimum_height, bold = True)
        self.main_layout.add_widget(self.hindi_label)
        self.main_layout.add_widget(self.hindi_section)

        self.tamil_section = MDGridLayout(size_hint_y = 5, width = Window.minimum_width, cols = 10, spacing = "20dp", padding = "20dp")
        self.tamil_label = MDLabel(text='Tamil Songs', font_style='H4', size_hint_y = None, height = Window.minimum_height, bold = True)
        self.main_layout.add_widget(self.tamil_label)
        self.main_layout.add_widget(self.tamil_section)

        self.false_section = MDGridLayout(size_hint_y = 0.5, width = Window.minimum_width, cols = 10, spacing = "20dp", padding = "20dp")
        self.false_label = MDLabel(text='', font_style='H4', size_hint_y = None, height = Window.minimum_height, bold = True)
        self.main_layout.add_widget(self.false_label)
        self.main_layout.add_widget(self.false_section)


        # Add cards to card layout
        #self.songs = get_songs_from_database() # Function to get songs from database
        #for song in self.songs:
        #l = ['Jeevamshamayi', 'Chundari Penne', 'Kaliyuga', 'Nangeli Poove', 'Harivarasanam', 'Gulumaal', 'Etho Nidrathan', 'Paathiramazhayetho', 'Thee Minnal', 'Onnam Padimele']
        songs = Database.music(limit = 30)
        s1 = songs[:10]
        print(s1)
        s2 = songs[10:20]
        s3 = songs[20:30]
        for i in s1:
              #songs = Database.music(limit=1)
              #print(songs)
            #if song.section == 'recommended':
              self.card1 = MDCard(orientation = "vertical", height = "250dp", padding = dp(4), size_hint_y = None, size_hint_x = 1, spacing = dp(5), 
                                  ripple_behavior = True, focus_behavior = True, elevation = 5, focus_color = (31,31,31,0.15))#, unfocus_color = (40,40,40,0.1), md_bg_color = (0,0,0,0))
              self.card1.add_widget(Image(source=i[3]))
              self.card1.add_widget(MDLabel(text=i[1], font_style='Subtitle1', bold=True, size_hint = (1,0.2)))
              self.card1.add_widget(MDLabel(text=i[2], size_hint = (1,0.2), font_style='Subtitle2'))
              self.card1.bind(on_release = self.song)
              self.recommended_section.add_widget(self.card1)

        for x in s2:   
                 
              #songs = Database.music(limit=1)
              self.card2 = MDCard(orientation = "vertical", height = "250dp", padding = dp(4), size_hint_y = None, size_hint_x = 1, spacing = dp(5), 
                                  ripple_behavior = True, focus_behavior = True, elevation = 3, focus_color = (31,31,31,0.15))#,  unfocus_color = (40,40,40,0.1))
              self.card2.add_widget(Image(source=x[3]))
              self.card2.add_widget(MDLabel(text=x[1], font_style='Subtitle1', bold=True, size_hint = (1,0.2)))
              self.card2.add_widget(MDLabel(text=x[2], size_hint = (1,0.2), font_style='Subtitle2'))
              self.card2.bind(on_release = self.song)
              self.malayalam_section.add_widget(self.card2)

        for y in s3:
              
              #songs = Database.music(limit=1)
              self.card3 = MDCard(orientation = "vertical", height = "250dp", padding = dp(4), size_hint_y = None, size_hint_x = 1, spacing = dp(5), 
                                  ripple_behavior = True, focus_behavior = True, elevation = 3, focus_color = (31,31,31,0.15))#,  unfocus_color = (40,40,40,0.1))
              self.card3.add_widget(Image(source=y[3]))
              self.card3.add_widget(MDLabel(text=y[1], font_style='Subtitle1', bold=True, size_hint = (1,0.2)))
              self.card3.add_widget(MDLabel(text=y[2], size_hint = (1,0.2), font_style='Subtitle2'))
              self.card3.bind(on_release = self.song)
              self.english_section.add_widget(self.card3)

              #songs = Database.music(limit=1)
              self.card4 = MDCard(orientation = "vertical", height = "250dp", padding = dp(4), size_hint_y = None, size_hint_x = 1, spacing = dp(5), 
                                  ripple_behavior = True, focus_behavior = True, elevation = 3, focus_color = (31,31,31,0.15))#,  unfocus_color = (40,40,40,0.1))
              self.card4.add_widget(Image(source=y[3]))
              self.card4.add_widget(MDLabel(text=y[1], font_style='Subtitle1', bold=True, size_hint = (1,0.2)))
              self.card4.add_widget(MDLabel(text=y[2], size_hint = (1,0.2), font_style='Subtitle2'))
              self.card4.bind(on_release = self.song)
              self.hindi_section.add_widget(self.card4)

              #songs = Database.music(limit=1)
              self.card5 = MDCard(orientation = "vertical", height = "250dp", padding = dp(4), size_hint_y = None, size_hint_x = 1, spacing = dp(5), 
                                  ripple_behavior = True, focus_behavior = True, elevation = 3, focus_color = (31,31,31,0.15))#,  unfocus_color = (40,40,40,0.1))
              self.card5.add_widget(Image(source=y[3]))
              self.card5.add_widget(MDLabel(text=y[1], font_style='Subtitle1', bold=True, size_hint = (1,0.2)))
              self.card5.add_widget(MDLabel(text=y[2], size_hint = (1,0.2), font_style = 'Subtitle2'))
              self.card5.bind(on_release = self.song)
              self.tamil_section.add_widget(self.card5)

        self.add_widget(self.nav_layout)

    def resize(self, window, width, height):
        print("Resizing")
        self.rect.size = Window.size

    def logout(self, dt):
        self.manager.remove_widget(MainScreen(name='main'))
        self.manager.current = 'login'

    def to_textart(self, dt):
        self.nav_drawer.set_state('close')
        self.manager.current = 'aiart'

    def to_playlist(self, dt):
        self.nav_drawer.set_state('close')
        self.manager.current = 'playlist'

    def song(self, instance):
        self.song_name = instance.children[1].text
        print(self.song_name)
        self.manager.get_screen("musicplayer").playlist = False
        self.manager.get_screen('musicplayer').playlist_songs = None
        self.manager.get_screen('musicplayer').prev_screen = 'main'
        self.manager.get_screen("musicplayer").song_name = self.song_name
        #print(self.play_pause.icon)
       # if self.play_pause and self.counter > 1:
            #print("yes")
           # self.manager.get_screen("musicplayer").play_button.icon == self.play_pause.icon
        self.manager.current = 'musicplayer'
    
    def song_clicked(self):
        song = self.song_name
        return song
    
    def search(self):
        print(1339013190)
        #self.manager.add_widget(SearchScreen(name='search'))
        self.manager.current = 'search'

    def se(self, instance):
        pass

    def on_pre_enter(self):
        print(Window.size)
        print("Entered Main")
        for card in self.recommended_section.children:
            card.focus_color = (31,31,31,0.15)

        for card in self.malayalam_section.children:
            card.focus_color = (31,31,31,0.15)

        for card in self.english_section.children:
            card.focus_color = (31,31,31,0.15)

        for card in self.hindi_section.children:
            card.focus_color = (31,31,31,0.15)

        for card in self.tamil_section.children:
            card.focus_color = (31,31,31,0.15)

        if self.counter == 0:
            self.layout = MDCard(size_hint = (1, 0.1), pos_hint = {'center_x': 0.5, 'bottom': 1}, md_bg_color = (0,0,0,1), elevation = 3)
            self.layout.bind(on_press = self.se)
            self.add_widget(self.layout)
            self.counter += 1
            print(self.song_author)
            print(self.sound)
            print(self.song_image)
            print(self.song_name)
            print(type(self.song_name))
            #self.layout = MDCard(size_hint = (1, 0.1), pos_hint = {'center_x': 0.5, 'bottom': 1}, md_bg_color = (0,0,0,1), elevation = 3)
            #self.layout.bind(on_press = self.se)
            #self.add_widget(self.layout)

            self.sub_layout1 = MDBoxLayout(size_hint_x = None, width = self.height)
            self.layout.add_widget(self.sub_layout1)

            self.img = Image(source='images/test.png', pos_hint = {'center_x':0.5, 'center_y': 0.5}, size_hint = (0.75,0.75))
            self.sub_layout1.add_widget(self.img)

            self.sub_layout2 = MDBoxLayout(orientation = 'horizontal')
            self.layout.add_widget(self.sub_layout2)

            self.sub_layout2_1 = MDBoxLayout(orientation = 'vertical', size_hint_x = 0.2, spacing = "0.5dp", padding = "20dp")
            self.sub_layout2.add_widget(self.sub_layout2_1)

            self.song_n = MDLabel(text = '', halign = "left")
            self.sub_layout2_1.add_widget(self.song_n)
            self.song_auth = MDLabel(text = '', halign = "left")
            self.sub_layout2_1.add_widget(self.song_auth)

            self.sub_layout5 = MDBoxLayout(orientation = 'vertical', size_hint_x = 0.8, spacing = "1dp", padding = "20dp", pos_hint = {'center_x':0.5, 'center_y':0.5})
            self.sub_layout2.add_widget(self.sub_layout5)

            self.sub_layout2_1_1 = MDBoxLayout(orientation = 'horizontal', spacing = "5dp", pos_hint = {'center_x':0.88, 'center_y':0.3})
            self.sub_layout5.add_widget(self.sub_layout2_1_1)

            #self.sub_layout2_1_1.add_widget(MDLabel(text = "Song Name", halign = "left"))
            self.skip_prev = MDIconButton(icon='skip-previous', halign = "center")
            self.sub_layout2_1_1.add_widget(self.skip_prev)
            self.play_pause = MDIconButton(icon='play', halign = "center", icon_color = [0,0,0,1], theme_icon_color = "Custom", md_bg_color = "white")
            self.sub_layout2_1_1.add_widget(self.play_pause)
            self.skip_next = MDIconButton(icon='skip-next', halign = "center")
            self.sub_layout2_1_1.add_widget(self.skip_next)
            #self.sub_layout2_1_1.add_widget(MDLabel(text = "Author Name", halign = "left"))

            self.sub_layout5_2 = MDBoxLayout(orientation = 'horizontal', spacing = "0.1dp", size_hint_x = 0.8, padding = "5dp")
            self.sub_layout5.add_widget(self.sub_layout5_2)

            self.start = MDLabel(text = "00:00", size_hint_x = 0.2, font_style = "Subtitle2", halign = "right")
            self.sub_layout5_2.add_widget(self.start)
            self.slider = MDSlider(size_hint_x = 0.7, cursor_image = 'images/test.png', hint = False)
            self.sub_layout5_2.add_widget(self.slider)
            self.end = MDLabel(text = "00:00", size_hint_x = 0.1, font_style = "Subtitle2")
            self.sub_layout5_2.add_widget(self.end)

            self.sub_layout_3 = MDAnchorLayout(anchor_x = 'center', anchor_y = 'center', size_hint = (0.2, 1))
            self.sub_layout2.add_widget(self.sub_layout_3)

            self.sub_layout_3_1 = MDBoxLayout(orientation = 'horizontal', size_hint = (None, None), height = Window.minimum_height, width = Window.minimum_width)
            self.sub_layout_3.add_widget(self.sub_layout_3_1)

            self.switch = MDIconButton(icon='music-accidental-double-flat', on_press = lambda x: Thread(target=self.booster, name='Song Booster').start())
            self.sub_layout_3_1.add_widget(self.switch)
            #self.sub_layout_3_1.add_widget(MDIconButton(icon='play'))
            #self.sub_layout_3_1.add_widget(MDIconButton(icon='skip-next'))




            #self.sub_layout.add_widget(MDLabel(text="Song Name\nAuthor Name", size_hint = (0.01,0.3), halign = 'left'))
            #self.layout.add_widget(MDIconButton(icon="play", pos_hint = {'center_x': 0.5, 'center_y': 0.5, 'right':0.5}))

        elif self.counter > 0 and self.sound != None:
            print("Entered Counter")
            self.counter += 1
            print(self.img.source, self.song_image)
            self.img.source = self.song_image
            print("Changed Image")
            self.song_n.text = self.song_name
            self.song_auth.text = self.song_author
            self.end.text = self.convert_seconds_to_min(self.sound.length)
            self.slider.bind(on_touch_up = self.touch_up)
            print(self.sound.state)
            self.play_pause.icon = ('play' if self.sound.state == 'stop' else 'pause')
            self.play_pause.bind(on_press = self.playpause)
            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)

    def booster(self):
        if self.sound:
            BassBoost.audio(path=self.sound.source)
            self.sound.source = self.sound.source.replace('.mp3', '-boosted.mp3')
            self.sound.seek((self.slider.value/100)*self.sound.length)
            self.sound.play()
            self.bass_on

    def bass_on(self):
        toast(text="Bass enabled for the current song!", background=[1,0,0,1])


    def update_slider(self, dt):
        self.slider.value = (self.sound.get_pos() / self.sound.length) * 100

    def update_time(self, dt):
        total_seconds = int(self.sound.get_pos())
        current_minute = total_seconds // 60
        current_seconds = total_seconds - current_minute * 60
        current_time = f"{current_minute:02}:{current_seconds:02}"
        self.start.text = current_time

    def touch_up(self, touch, widget):
        if widget.pos[1] < 50:
            if self.sound:
                self.sound.seek((self.slider.value/100)*self.sound.length)

    def convert_seconds_to_min(self, sec):
        val = str(datetime.timedelta(seconds = sec)).split(':')
        return f'{val[1]}:{val[2].split(".")[0]}'

    def playpause(self, dt):
        global current_pos
        if self.sound.state == 'play':
           self.paused = True
           self.finished = False
           self.sound.stop()
           self.play_pause.icon = 'play'
           Clock.unschedule(self.update_slider)
           Clock.unschedule(self.update_time)
           current_pos = self.sound.get_pos()
        else:
           if self.sound:
              self.sound.play()
              self.play_pause.icon = 'pause'
              Clock.schedule_interval(self.update_slider, 1)
              Clock.schedule_interval(self.update_time, 1)
              self.finished = False
              if self.paused:
                self.sound.seek(current_pos)     
                self.paused = False   

    def check(self):
        print("Entered")
        if self.song_name != self.prev_sn:
            Clock.schedule_once(self.on_pre_enter)

class RegistrationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.go_back = MDAnchorLayout(anchor_x = "left", anchor_y = "top")
        
        self.back_button = MDRaisedButton(text="Back")
        self.back_button.bind(on_release = lambda x: self.back())
        self.go_back.add_widget(self.back_button)

        self.add_widget(self.go_back)

        self.registration_form = MDBoxLayout(orientation='vertical', size_hint=(0.5, 0.5), pos_hint={'center_x':0.5, 'center_y':0.5})
        
        self.username = MDTextField(hint_text = "Username")
        self.email = MDTextField(hint_text='Email')
        self.phone = MDTextField(hint_text='Phone')
        self.password = MDTextField(hint_text='Password', password=True, helper_text = "Passwords doesnt match", helper_text_mode = "on_error")
        self.conf_pass = MDTextField(hint_text='Confirm Password', password=True, helper_text = "Passwords doesnt match", helper_text_mode = "on_error")
        self.registration_form.add_widget(self.username)
        self.registration_form.add_widget(self.email)
        self.registration_form.add_widget(self.phone)
        self.registration_form.add_widget(self.password)
        self.registration_form.add_widget(self.conf_pass)

        # Create a register button
        self.register_button = MDRectangleFlatButton(text='Register', pos_hint={'center_x':0.5})
        self.register_button.bind(on_release=self.register)
        self.registration_form.add_widget(self.register_button)

        # Add the registration form to the screen
        self.add_widget(self.registration_form)

    def back(self):
        self.manager.current = 'login'


    def register(self, dt):
          if self.password.text == self.conf_pass.text:
            Database.create_account(self.username.text, self.email.text, self.phone.text, self.password.text)
            self.manager.add_widget(MainScreen(name='main'))
            self.manager.current = 'main'
          else:
            self.password.error = True
            self.conf_pass.error = True

class AITextArtScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = False
        self.layout = MDBoxLayout(orientation='vertical')
        self.text_input = MDTextField(multiline=False, size_hint_y=None, height=50, hint_text='Enter text here')
        self.submit_button = MDRectangleFlatButton(text='Submit', size_hint_y=None, height=50)
        if self.running == False:
           self.submit_button.bind(on_press=self.generate_image)
        else:
            return
        self.image_space = AsyncImage(source = "images/gm.png", opacity=0.5, pos_hint = {'center_x':0.5, 'center_y': 0.5})
        self.layout.add_widget(self.image_space)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.submit_button)
        self.add_widget(self.layout)
        
    def generate_image(self, instance):
        self.running = True
        text = self.text_input.text
        if not text:
            return
        self.image_space.source = 'images/gi.png'

        openai.api_key = "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"
        
        image = openai.Image.create(
            prompt = text,
            size = "1024x1024",
            n = 1
        )
        image_url = image['data'][0]['url']
        self.image_space.source = image_url
        self.image_space.size_hint = (0.3,0.3)
        self.image_space.opacity = 1
        self.running = False

class MusicPlayer(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stop = False
        self.next_song = []
        self.previous_song = []
        self.playlist = False
        self.playlist_songs = None
        self.counter = 0
        self.song_name = "None"
        self.paused = False
        self.finished = True
        self.is_playing = False
        self.sound = SoundLoader.load('music/Chundari Penne.mp3')
        self.screen_switched = False
        self.upcoming = None
        self.prev_screen = None
        self.queue = False
        self.queue_songs = []
        self.new = False
        self.counter2 = 0
        self.counter3 = 0
        self.played_songs = []

    def on_pre_enter(self, *args):
        self.song = Database.get_song_detail(name=self.song_name)
        new = Database.music(limit=1)
        self.upcoming = new[0]
        print(self.upcoming)
        if self.finished == True and self.counter == 0:
            print(1)
            self.previous_song.append(self.song)
            self.stop = True
            self.counter += 1
            self.sn = self.song[1]
            #print(self.song)
            self.sound = SoundLoader.load(self.song[4])
            self.sound.play()
            self.is_playing = True
            self.bg_image = FitImage(source = self.song[3], opacity = '0.3')
            self.add_widget(self.bg_image)
                
            self.back = MDIconButton(icon='chevron-left', pos_hint = {'top':1, 'left':0.85})
            self.back.bind(on_press=self.go_back)
            self.add_widget(self.back)
                        
            self.song_image = Image(source=self.song[3], pos_hint = {'left':1.0, 'center_x':0.1}, keep_ratio = True)
            self.add_widget(self.song_image)
            self.song_title = MDLabel(text=self.song[1], pos_hint = {'left':1.0, 'center_x':0.7, 'center_y': 0.5}, bold = True, font_style = "H2", size_hint = (1,0.1), padding = (0,dp(4)))
            self.add_widget(self.song_title)
            self.song_author = MDLabel(text=self.song[2], pos_hint = {'left':1.0, 'center_x':0.7, 'center_y': 0.45}, font_style = "H6", size_hint = (1,0.1), padding = (0,dp(4)))
            self.add_widget(self.song_author)

            self.slider = MDSlider(pos_hint = {'center_x': 0.5, 'center_y': 0.2}, size_hint = (0.5,0.1), hint = False, on_touch_up = self.touch_down)
            self.add_widget(self.slider)
            #self.slider.bind(self.set_pos)
            self.start_time = MDLabel(text="00:00", pos_hint = {'center_x': 0.33, 'center_y': 0.2}, id = 'start_time', size_hint = (0.2,0.1), font_style = "Subtitle1")
            self.add_widget(self.start_time)
            self.end_time = MDLabel(text=self.convert_seconds_to_min(self.sound.length), pos_hint = {'center_x': 0.85, 'center_y': 0.2}, id='end_time', size_hint = (0.2,0.1), font_style = "Subtitle1")
            self.add_widget(self.end_time)
                        
            self.play_button = MDIconButton(icon = 'pause', pos_hint = {'center_x': 0.5, 'center_y': 0.1}, icon_color = [0,0,0,1], theme_icon_color = "Custom", md_bg_color = "white")
            self.add_widget(self.play_button)
            self.play_button.bind(on_press = self.play_pause)

            self.next_button = MDIconButton(icon = 'skip-next', pos_hint = {'center_x':0.55, 'center_y':0.1})
            self.add_widget(self.next_button)
            self.next_button.bind(on_press = self.next)

            self.prev_button = MDIconButton(icon = 'skip-previous', pos_hint = {'center_x':0.45, 'center_y':0.1})
            self.add_widget(self.prev_button)
            self.prev_button.bind(on_press =self.previous)

            self.sound.bind(on_stop=self.on_stop)
            self.play_button.icon = ('play' if self.sound.state == 'stop' else 'pause')
            self.sound.play()
            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)
            self.finished = False
            self.paused = False
            #self.layout = MDAnchorLayout(anchor_x = "left", anchor_y = "bottom", md_bg_color = "red", size_hint = (0.1,0.1))
            #self.up = MDLabel(text = f"UPCOMING:\n{self.upcoming[1]}\n{self.upcoming[2]}")
            #self.layout.add_widget(self.up)
            #self.add_widget(self.layout)
            #print(self.up)
        
        if self.song[1] != self.sn and self.counter > 0:
            print(100)
            self.screen_switched = False
            self.sn = self.song[1]
            self.new = True
            self.sound.stop()
            self.bg_image.source = self.song[3]
            self.song_title.text = self.song[1]
            self.song_author.text = self.song[2]
            self.song_image.source = self.song[3]

            self.sound = SoundLoader.load(self.song[4])
            self.start_time.text = "00:00"
            self.end_time.text = self.convert_seconds_to_min(self.sound.length)
            self.sound.play()
            self.sound.bind(on_stop = self.on_stop)
            self.play_button.icon = ('play' if self.sound.state == 'stop' else 'pause')
            self.play_button.bind(on_press = self.play_pause)
            self.paused = False
            self.finished = False

            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)

        else:
            self.play_button.icon = ('play' if self.sound.state == 'stop' else 'pause')
            print(self.sn, self.song[1])
            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)   

    def convert_seconds_to_min(self, sec):
        val = str(datetime.timedelta(seconds = sec)).split(':')
        return f'{val[1]}:{val[2].split(".")[0]}'

    def play_pause(self, dt):
        global current_pos
        if self.sound.state == 'play':
           self.paused = True
           self.finished = False
           self.sound.stop()
           self.play_button.icon = 'play'
           Clock.unschedule(self.update_slider)
           Clock.unschedule(self.update_time)
           current_pos = self.sound.get_pos()
        else:
           if self.sound:
              self.sound.play()
              self.play_button.icon = 'pause'
              Clock.schedule_interval(self.update_slider, 1)
              Clock.schedule_interval(self.update_time, 1)
              self.finished = False
              if self.paused:
                self.sound.seek(current_pos)     
                self.paused = False   

    def next(self, dt):
        pass

    def previous(self, dt):
        song = self.played_songs[self.index]





        print(self.next_song, self.previous_song)
        self.new = True
        self.next_song.insert(0, Database.get_song_detail(name = self.sn))
        self.paused = False
        self.play_button.icon = 'play'
        self.sound.stop()
        self.slider.value = 0
        Clock.unschedule(self.update_slider)
        Clock.unschedule(self.update_time)
        print("On previous:", self.previous_song)
        #self.previous_song = Database.get_song_detail(name = self.sn)
        print(self.sn)
        self.sn = self.previous_song[0][1]
        
        self.bg_image.source = self.previous_song[0][3]
        self.song_title.text = self.previous_song[0][1]
        self.song_author.text = self.previous_song[0][2]
        self.song_image.source = self.previous_song[0][3]

        self.sound = SoundLoader.load(self.previous_song[0][4])
        self.start_time.text = "00:00"
        self.end_time.text = self.convert_seconds_to_min(self.sound.length)
        self.sound.play()
        self.sound.bind(on_stop = self.on_stop)
        self.play_button.icon = 'pause'
        self.play_button.bind(on_press = self.play_pause)

        Clock.schedule_interval(self.update_slider, 1)
        Clock.schedule_interval(self.update_time, 1)
        self.manager.get_screen("main").sound = self.sound
        self.manager.get_screen("main").is_playing = self.paused
        self.manager.get_screen("main").song_name = self.song_title.text
        self.manager.get_screen("main").song_n.text = self.song_title.text
        self.manager.get_screen("main").song_author = self.song_author.text
        self.manager.get_screen("main").song_auth.text = self.song_author.text
        self.manager.get_screen("main").song_image = self.song_image.source
        self.manager.get_screen("main").img.source = self.song_image.source
        self.manager.get_screen("main").end.text = self.convert_seconds_to_min(self.sound.length)
        MainScreen.on_pre_enter

        self.previous_song.pop(0)

        #notification.notify(app_icon = None, title = self.song_title.text, app_name = "Music Player", 
                            #message = self.song_author.text, timeout = 10, toast = False)

    def on_stop(self, dt):
        if self.paused == False and self.slider.value > 98.5 and self.new == False:
            self.paused = False
            self.play_button.icon = 'play'
            Clock.unschedule(self.update_slider)
            Clock.unschedule(self.update_time)

            if self.queue != False:
                if len(self.queue_songs) != 0:
                    print(self.queue_songs)
                    if len(self.queue_songs) != 1:
                        self.previous_song = self.queue_songs[0]
                    self.sn = self.queue_songs[0][1]
                
                    self.bg_image.source = self.queue_songs[0][3]
                    self.song_title.text = self.queue_songs[0][1]
                    self.song_author.text = self.queue_songs[0][2]
                    self.song_image.source = self.queue_songs[0][3]

                    self.sound = SoundLoader.load(self.queue_songs[0][4])
                    self.start_time.text = "00:00"
                    self.end_time.text = self.convert_seconds_to_min(self.sound.length)
                    self.sound.play()
                    self.sound.bind(on_stop = self.on_stop)
                    self.play_button.icon = 'pause'
                    self.play_button.bind(on_press = self.play_pause)

                    Clock.schedule_interval(self.update_slider, 1)
                    Clock.schedule_interval(self.update_time, 1)
                    self.queue_songs.pop(0)
                    if len(self.queue_songs) == 0:
                        self.queue_songs = []
                        self.queue = False  

            elif self.playlist:
                if self.playlist_songs != None:
                    if len(self.playlist_songs) != 1:
                        self.previous_song = self.playlist_songs[0]
                    self.sn = self.playlist_songs[0][1]
                
                    self.bg_image.source = self.playlist_songs[0][3]
                    self.song_title.text = self.playlist_songs[0][1]
                    self.song_author.text = self.playlist_songs[0][2]
                    self.song_image.source = self.playlist_songs[0][3]

                    self.sound = SoundLoader.load(self.playlist_songs[0][4])
                    self.start_time.text = "00:00"
                    self.end_time.text = self.convert_seconds_to_min(self.sound.length)
                    self.sound.play()
                    self.sound.bind(on_stop = self.on_stop)
                    self.play_button.icon = 'pause'
                    self.play_button.bind(on_press = self.play_pause)

                    Clock.schedule_interval(self.update_slider, 1)
                    Clock.schedule_interval(self.update_time, 1)
                    self.playlist_songs.pop(0)
                    if len(self.playlist_songs) == 0:
                        self.playlist_songs = None
                        self.playlist = False              
           
            else:
                song = Database.music(limit=1)
                print("On stop:", song)
                self.previous_song = Database.get_song_detail(name = self.sn)
                self.sn = song[0][1]
                
                self.bg_image.source = song[0][3]
                self.song_title.text = song[0][1]
                self.song_author.text = song[0][2]
                self.song_image.source = song[0][3]

                self.sound = SoundLoader.load(song[0][4])
                self.start_time.text = "00:00"
                self.end_time.text = self.convert_seconds_to_min(self.sound.length)
                self.sound.play()
                self.sound.bind(on_stop = self.on_stop)
                self.play_button.icon = 'pause'
                self.play_button.bind(on_press = self.play_pause)

                Clock.schedule_interval(self.update_slider, 1)
                Clock.schedule_interval(self.update_time, 1)
            self.manager.get_screen("main").sound = self.sound
            self.manager.get_screen("main").is_playing = self.paused
            self.manager.get_screen("main").song_name = self.song_title.text
            self.manager.get_screen("main").song_n.text = self.song_title.text
            print(self.manager.get_screen("main").song_n.text, self.song_title.text)
            self.manager.get_screen("main").song_author = self.song_author.text
            self.manager.get_screen("main").song_auth.text = self.song_author.text
            self.manager.get_screen("main").song_image = self.song_image.source
            self.manager.get_screen("main").img.source = self.song_image.source
            print(self.manager.get_screen("main").song_image, self.song_image.source)
            self.manager.get_screen("main").end.text = self.convert_seconds_to_min(self.sound.length)
            MainScreen.on_pre_enter

            notification.notify(app_icon = None, title = self.song_title.text, app_name = "Music Player", 
                                message = self.song_author.text, timeout = 10, toast = False)
            
            self.stop = True
 
        elif self.new == True:
            self.new = False
            self.stop = True


    def update_slider(self, dt):
        self.slider.value = (self.sound.get_pos() / self.sound.length) * 100

    def update_time(self, dt):
        total_seconds = int(self.sound.get_pos())
        current_minute = total_seconds // 60
        current_seconds = total_seconds - current_minute * 60
        current_time = f"{current_minute:02}:{current_seconds:02}"
        self.start_time.text = current_time

    def touch_down(self, *args):
        if self.sound:
            self.sound.seek((self.slider.value/100)*self.sound.length)

    def go_back(self, dt):
        self.manager.get_screen("main").sound = self.sound
        self.manager.get_screen("main").paused = self.paused
        self.manager.get_screen("main").song_name = self.song_title.text
        self.manager.get_screen("main").song_author = self.song_author.text
        self.manager.get_screen("main").song_image = self.song_image.source
        self.manager.current = self.prev_screen

'''
    def next(self, dt):
        print(self.next_song, self.previous_song)
        self.new = True
        self.paused = False
        self.play_button.icon = 'play'
        self.sound.stop()
        self.slider.value = 0
        Clock.unschedule(self.update_slider)
        Clock.unschedule(self.update_time)
        self.counter2 += 1

        if len(self.next_song) != 0:
            if self.stop == False:
                self.previous_song.insert(0, Database.get_song_detail(name = self.sn))

            self.stop = False
            self.sn = self.next_song[0][1]
            
            self.bg_image.source = self.next_song[0][3]
            self.song_title.text = self.next_song[0][1]
            self.song_author.text = self.next_song[0][2]
            self.song_image.source = self.next_song[0][3]

            self.sound = SoundLoader.load(self.next_song[0][4])
            self.start_time.text = "00:00"
            self.end_time.text = self.convert_seconds_to_min(self.sound.length)
            self.sound.play()
            self.sound.bind(on_stop = self.on_stop)
            self.play_button.icon = 'pause'
            self.play_button.bind(on_press = self.play_pause)

            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)
            self.next_song.pop(0)

        elif self.queue != False:
            if len(self.queue_songs) != 0:
                print(self.queue_songs)
                self.stop = False
                if len(self.queue_songs) != 1 and self.stop == False:
                    self.previous_song.insert(0, self.queue_songs[0])

                self.stop = False
                self.sn = self.queue_songs[0][1]
            
                self.bg_image.source = self.queue_songs[0][3]
                self.song_title.text = self.queue_songs[0][1]
                self.song_author.text = self.queue_songs[0][2]
                self.song_image.source = self.queue_songs[0][3]

                self.sound = SoundLoader.load(self.queue_songs[0][4])
                self.start_time.text = "00:00"
                self.end_time.text = self.convert_seconds_to_min(self.sound.length)
                self.sound.play()
                self.sound.bind(on_stop = self.on_stop)
                self.play_button.icon = 'pause'
                self.play_button.bind(on_press = self.play_pause)

                Clock.schedule_interval(self.update_slider, 1)
                Clock.schedule_interval(self.update_time, 1)
                self.queue_songs.pop(0)
                if len(self.queue_songs) == 0:
                    self.queue_songs = []
                    self.queue = False  

        elif self.playlist:
            if self.playlist_songs != None:
                print(self.playlist_songs)
                print(len(self.playlist_songs), self.stop)
                if len(self.playlist_songs) != 1 and self.new == False or self.counter2 == 1:
                    print(self.playlist_songs[0])
                    self.previous_song.insert(0, self.playlist_songs[0])

                self.stop = False
                self.sn = self.playlist_songs[0][1]
            
                self.bg_image.source = self.playlist_songs[0][3]
                self.song_title.text = self.playlist_songs[0][1]
                self.song_author.text = self.playlist_songs[0][2]
                self.song_image.source = self.playlist_songs[0][3]

                self.sound = SoundLoader.load(self.playlist_songs[0][4])
                self.start_time.text = "00:00"
                self.end_time.text = self.convert_seconds_to_min(self.sound.length)
                self.sound.play()
                self.sound.bind(on_stop = self.on_stop)
                self.play_button.icon = 'pause'
                self.play_button.bind(on_press = self.play_pause)

                Clock.schedule_interval(self.update_slider, 1)
                Clock.schedule_interval(self.update_time, 1)
                self.playlist_songs.pop(0)
                if len(self.playlist_songs) == 0:
                    self.playlist_songs = None
                    self.playlist = False              
        
        else:
            song = Database.music(limit=1)
            print("On stop:", song)
            if self.stop == False:
                self.previous_song.insert(0, Database.get_song_detail(name = self.sn))

            self.stop = False
            self.sn = song[0][1]
            
            self.bg_image.source = song[0][3]
            self.song_title.text = song[0][1]
            self.song_author.text = song[0][2]
            self.song_image.source = song[0][3]

            self.sound = SoundLoader.load(song[0][4])
            self.start_time.text = "00:00"
            self.end_time.text = self.convert_seconds_to_min(self.sound.length)
            self.sound.play()
            self.sound.bind(on_stop = self.on_stop)
            self.play_button.icon = 'pause'
            self.play_button.bind(on_press = self.play_pause)

            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)
        self.manager.get_screen("main").sound = self.sound
        self.manager.get_screen("main").is_playing = self.paused
        self.manager.get_screen("main").song_name = self.song_title.text
        self.manager.get_screen("main").song_n.text = self.song_title.text
        print(self.manager.get_screen("main").song_n.text, self.song_title.text)
        self.manager.get_screen("main").song_author = self.song_author.text
        self.manager.get_screen("main").song_auth.text = self.song_author.text
        self.manager.get_screen("main").song_image = self.song_image.source
        self.manager.get_screen("main").img.source = self.song_image.source
        print(self.manager.get_screen("main").song_image, self.song_image.source)
        self.manager.get_screen("main").end.text = self.convert_seconds_to_min(self.sound.length)
        MainScreen.on_pre_enter

        #notification.notify(app_icon = None, title = self.song_title.text, app_name = "Music Player", 
                            #message = self.song_author.text, timeout = 10, toast = False)
'''

class BassBoost():
    global attenuate_db
    global accentuate_db
    attenuate_db = -5
    accentuate_db = 5


    def bass_line_freq(track):
        sample_track = list(track)

        est_mean = np.mean(sample_track)

        est_std = 3 * np.std(sample_track) / (math.sqrt(2))

        bass_factor = int(round((est_std - est_mean) * 0.005))
        
        return bass_factor
    
    def audio(path):
        sample = AudioSegment.from_mp3(path)
        filtered = sample.low_pass_filter(BassBoost.bass_line_freq(sample.get_array_of_samples()))

        combined = (sample - attenuate_db).overlay(filtered + accentuate_db)
        combined.export("D:\\Music Player App\\" + path[20:].replace(".mp3", "") + "-boosted.mp3", format="mp3")

        print("Done")


class SearchScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.song_id = None

        self.songs = Database.music(limit = 27)

        self.back = MDIconButton(icon='chevron-left', pos_hint = {'top':1, 'left':0.85})
        self.add_widget(self.back)
        self.back.bind(on_press = self.go_back)

        self.search_bar = MDTextField(mode='fill', hint_text = 'Search', icon_left = 'magnify', 
                                      pos_hint = {'top':0.95, 'center_x': 0.5}, size_hint = (0.9,0.2), 
                                      background_color = "yellow", fill_color_focus = "white", fill_color_normal = "grey",
                                      hint_text_color_normal = "white", icon_left_color_normal = "white", text_validate_unfocus = False)
        self.add_widget(self.search_bar)
        self.search_bar.bind(text = self.update_list)
        self.search_bar.bind(on_text_validate = self.update_suggestion)

        self.scroll = MDScrollView(pos_hint = {'top':0.9}, do_scroll_x = False, scroll_wheel_distance = 5, scroll_type = ['bars', 'content'], smooth_scroll_end = 20,
                                        always_overscroll = False, bar_margin = 0.5, bar_width = 7, bar_inactive_color = [0,0,0,0])
        self.add_widget(self.scroll)

        self.list = MDList()
        self.scroll.add_widget(self.list)


        for i in self.songs:
            self.sugg_songs = TwoLineAvatarIconListItem(IconRightWidget(id = str(i[0]), icon = 'dots-vertical', on_press = self.dropdown), ImageLeftWidget(source = i[3]), text=i[1], secondary_text = i[2])
            self.list.add_widget(self.sugg_songs)
            self.sugg_songs.bind(on_release = self.musicplayer)

       #self.menu.open()

        #self.list.add_widget(MDLabel(text='gaga\ngagaga\ngagagag\nagagagagaga', size_hint = (2,2)))
        
    def update_list(self, instance, value):
        text = self.search_bar.text
        self.list.clear_widgets()
        
        filtered_items = Database.song_match(text)

        if len(filtered_items) > 0:
          for it in filtered_items:
            self.sugg_songs = TwoLineAvatarIconListItem(IconRightWidget(id = str(it[0]), icon = 'dots-vertical', on_press = self.dropdown), ImageLeftWidget(source = it[3]), text=it[1], secondary_text = it[2])
            self.list.add_widget(self.sugg_songs)
            self.sugg_songs.bind(on_release = self.musicplayer)

        if len(filtered_items) > 0 and len(self.search_bar.text) > 0:
            self.search_bar.hint_text = filtered_items[0][1]
        if len(self.search_bar.text) == 0:
            self.search_bar.hint_text = "Search"

    def update_suggestion(self, instance):
        if len(self.search_bar.text) != 0 and self.search_bar.hint_text != "Search":
            self.search_bar.text = self.search_bar.hint_text
            self.search_bar.hint_text = "Search"

    def go_back(self, dt):
        self.manager.current = 'main'

    def musicplayer(self, instance):
        self.song_name = instance.text
        print(self.song_name)
        self.manager.get_screen("musicplayer").song_name = self.song_name
        self.manager.get_screen('musicplayer').playlist = False
        self.manager.get_screen('musicplayer').playlist_songs = None
        self.manager.get_screen('musicplayer').prev_screen = 'search'
        self.manager.current = 'musicplayer'

    def dropdown(self, instance):
        self.song_id = int(instance.id)
        self.menu_items = [
        {
            'text' : 'Add to Queue',            
            'viewclass'  : 'OneLineListItem',
            'on_release' :  self.queue
        },
        {
             'text' : 'Add to Playlist',
             'viewclass' : 'OneLineListItem',
             'on_release' :  self.playlists
        }
        ]
        #print(self.sugg_songs.children)
        self.menu = MDDropdownMenu(
            caller = instance,
            items = self.menu_items,
            width_mult = 4) 
        self.menu.open()
        print("opened")

    def playlists(self):
        #self.scroll2 = MDScrollView(pos_hint = {'top':0.95}, height = "200dp")
        self.box = MDBoxLayout(size_hint_y = None, orientation = 'vertical', adaptive_height = True)
        #self.scroll2.add_widget(self.box)
        print(self.plays)
        for k in self.plays:
            #print(k)
            self.play_name = OneLineListItem(id = str(k[0]), text=k[1])
            self.play_name.bind(on_press = self.select_playlist)
            self.box.add_widget(self.play_name)

        self.dialog = MDDialog(
            title = "Select Playlist",
            type = "custom",
            auto_dismiss = True,
            content_cls = self.box
        )
        self.dialog.open()

    def queue(self):
        self.song_info = Database.get_song_detail(id = int(self.song_id))
        self.manager.get_screen('musicplayer').queue = True
        self.manager.get_screen('musicplayer').queue_songs.append(self.song_info)
        toast(text="Song Added To Queue")

    def select_playlist(self, instance):
        Database.add_playlist_song(playlist_id = int(instance.id), song_id = int(self.song_id))
        self.dialog.dismiss()
        toast(text="Song Added To Playlist")

    def on_pre_enter(self):
        self.account = Database.acc_details()[0]
        self.plays = Database.playlists_info(username = self.account)
        print(self.plays)


class Playlist(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.prev_len = 0

    
    def go_to_main(self, dt):
        self.manager.current = 'main'

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
        print(self.play_img, self.play_img[0])
        try:
          self.upload.background_normal = self.play_img[0]
          print(self.play_img[0], self.upload.background_normal)
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
            self.card_new.bind(on_press = self.playlist_songs)

            self.img_new = Image(source = (self.upload.background_normal if self.upload.background_normal != 'images/upload.png' else 'images/no img.png'), pos_hint = {'center_x':0.5, 'center_y':0.5}, size_hint_y = 1, keep_ratio = False, allow_stretch = True)
            self.card_new.add_widget(self.img_new)

            self.play_name_new = MDLabel(text = self.play_n.text, bold = True, font_style = 'H5', size_hint_y = 0.2)
            self.card_new.add_widget(self.play_name_new)

            self.play_date_new = MDLabel(text = t, font_style = "Subtitle2", size_hint_y = 0.1)
            self.card_new.add_widget(self.play_date_new)
            print(self.play_name_new.text, self.img_new.source, self.username, self.play_date_new.text)
            Database.create_playlist(name = self.play_name_new.text, image = self.play_img[0], user = self.username, date = self.play_date_new.text)
            self.dialog.dismiss()
            toast(text = "Playlist Created")
    
    def on_pre_enter(self):
        self.account = Database.acc_details()
        self.username = self.account[0]
        self.playlists = Database.playlists_info(username = self.username)
        print(self.playlists)
        self.prev_len = len(self.playlists)
         
        if self.counter == 0:
            self.counter += 1
            self.back = MDIconButton(icon='chevron-left', pos_hint = {'top':1, 'left':0.95})
            self.back.bind(on_press = self.go_to_main)
            self.add_widget(self.back)

            self.head = MDLabel(text="Playlists", pos_hint = {'top':0.95, 'right':0.53}, bold = True, font_style = "H3", size_hint = (0.5, 0.1))
            self.add_widget(self.head)

            self.scroll = MDScrollView(size_hint = (0.9,0.87), pos_hint = {'top':0.87, 'right':0.95}, scroll_wheel_distance = 5, scroll_type = ['bars', 'content'], smooth_scroll_end = 75,
                                            always_overscroll = False, bar_margin = 0.5, bar_width = 7, bar_inactive_color = [0,0,0,0])
            self.add_widget(self.scroll)

            self.sub_layout = MDStackLayout(spacing = "30dp", adaptive_height = True, width = dp(1000), padding = "20dp")
            self.scroll.add_widget(self.sub_layout)

            for i in range(len(self.playlists)):
                self.card = MDCard(id = str(self.playlists[i][0]), orientation = 'vertical', md_bg_color = (1,1,1,1), height = "350dp", width = "300dp", size_hint = (None , None), spacing = "10dp", padding = "20dp")
                self.sub_layout.add_widget(self.card)
                self.card.bind(on_press = self.playlist_songs)

                self.img = Image(source = self.playlists[i][2], pos_hint = {'center_x':0.5, 'center_y':0.5}, size_hint_y = 1, keep_ratio = False, allow_stretch = True)
                self.card.add_widget(self.img)

                self.play_name = MDLabel(text = self.playlists[i][1], bold = True, font_style = 'H5', size_hint_y = 0.2)
                self.card.add_widget(self.play_name)

                self.play_date = MDLabel(text = self.playlists[i][4], font_style = "Subtitle2", size_hint_y = 0.1)
                self.card.add_widget(self.play_date)

            self.create_play = MDFloatingActionButton(icon='plus', pos_hint = {'top':0.1, 'right':0.95}, elevation = 5, icon_size = "35dp")
            self.add_widget(self.create_play)
            self.create_play.bind(on_release = self.play_details)

        elif self.counter > 0 and self.prev_len < len(self.playlists):

            for y in range(self.prev_len, len(self.playlists)):
                self.new_card = MDCard(orientation = 'vertical', md_bg_color = (1,1,1,1), height = "350dp", width = "300dp", size_hint = (None , None), spacing = "10dp", padding = "20dp")
                self.sub_layout.add_widget(self.new_card)

                self.new_img = Image(source = self.playlists[y][2], pos_hint = {'center_x':0.5, 'center_y':0.5}, size_hint_y = 1, keep_ratio = False, allow_stretch = True)
                self.card_new.add_widget(self.img_new)

                self.new_play_name = MDLabel(text = self.playlists[y][1], bold = True, font_style = 'H5', size_hint_y = 0.2)
                self.card_new.add_widget(self.play_name_new)

                self.new_play_date = MDLabel(text = self.playlists[y][4], font_style = "Subtitle2", size_hint_y = 0.1)
                self.card_new.add_widget(self.play_date_new)
            self.prev_len = len(self.playlists)

    def playlist_songs(self, instance):
        self.manager.get_screen("playlist_songs").playlist_id = int(instance.id)
        self.manager.get_screen("playlist_songs").bg_img = instance.children[2].source
        self.manager.get_screen("playlist_songs").play_name = instance.children[1].text
        self.manager.get_screen("playlist_songs").play_date = instance.children[0].text
        self.manager.current = 'playlist_songs'



class Playlist_Songs(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlist_id = None
        print("Playlist ID:", self.playlist_id)
        self.bg_img = None
        self.play_name = None
        self.play_date = None

    def on_pre_enter(self):
        self.songs = Database.playlist_songs(id = self.playlist_id)
        print(self.songs)
        
        self.song_infos = []
        for i in self.songs:
            self.song_info = Database.get_song_detail(id = i[1])
            print(self.song_info)
            self.song_infos.append(self.song_info)
        print(self.song_infos)

        self.hex = self.colour_extractor(self.bg_img)

        with self.canvas:
            Color(0.5,0.5,0.5,
                    mode='hex')
            Rectangle(texture = Gradient.vertical(get_color_from_hex(self.hex[1]), get_color_from_hex(self.hex[0])),
                       pos=[0,-8], size=[2000,1000])

        self.bar = MDTopAppBar(title = self.play_name, shadow_color = (0,0,0,0), left_action_items = [["arrow-left", lambda x: self.go_back(), 'back']], pos_hint = {'top':1})
        self.add_widget(self.bar)

        self.scroll = MDScrollView(pos_hint = {'top':0.93}, scroll_wheel_distance = 5, scroll_type = ['bars', 'content'], smooth_scroll_end = 75,
                                        always_overscroll = False, bar_margin = 0.5, bar_width = 7, bar_inactive_color = [0,0,0,0])
        self.add_widget(self.scroll)

        self.main = MDBoxLayout(orientation = 'vertical', spacing = "1dp", size_hint_y = None, adaptive_height = True, padding = [0,0,0,100])
        self.scroll.add_widget(self.main) 

        self.layout = MDBoxLayout(orientation = 'horizontal', pos_hint = {'top':0.95}, size_hint_y = None, height = "300dp", size_hint_x = 0.4, spacing = "2dp")
        self.main.add_widget(self.layout)
        self.layout_sub = MDBoxLayout(orientation = 'horizontal', size_hint_y = None, height = "100dp", size_hint_x = 0.33, padding = [0,0,200,0], pos_hint = {'center_x':0.2}, spacing = "20dp")
        self.main.add_widget(self.layout_sub)

        self.bg = Image(source=self.bg_img, pos_hint = {'right':0.7, 'center_y':0.5}, size_hint_x = 0.5)
        if self.bg.texture.size != (248,248):
            image = Im.open(self.bg_img)
            new = image.resize((248, 248))
            new.save('-new.'.join(self.bg_img.rsplit('.', 1)))
            self.bg.source = '-new.'.join(self.bg_img.rsplit('.', 1))
        self.layout.add_widget(self.bg)

        self.sub_layout1 = MDBoxLayout(orientation = 'vertical', size_hint = (0.5,0.2), pos_hint = {'right':0.6, 'center_y':0.5}, spacing = "50dp")
        self.layout.add_widget(self.sub_layout1)

        self.song_name = MDLabel(text=self.play_name, font_style = "H4", bold = True)
        self.sub_layout1.add_widget(self.song_name)

        self.song_author = MDLabel(text= self.play_date, font_style = "Subtitle1")
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


        for i in range(len(self.song_infos)):
            self.card = MDCard(size_hint_y = None, orientation='horizontal', padding = [50,10,50,10], height="150dp", radius = 20, size_hint_x = 0.85, pos_hint = {'center_x':0.5})
            self.card.bind(on_release = self.musicplayer)
            self.layout2.add_widget(self.card)
            self.number.text = f"{i}"
            self.card.add_widget(MDLabel(text=f"{i+1}", size_hint_x = 0.1, font_style = "H5"))
            self.card.add_widget(Image(source=self.song_infos[i][3]))
            self.card.add_widget(MDLabel(text=self.song_infos[i][1], font_style = 'H5'))
            self.card.add_widget(MDLabel(text=self.song_infos[i][2], font_style = "H5"))
            self.card.add_widget(MDLabel(text='', size_hint_x = 0.4))
            self.card.add_widget(MDLabel(text=self.songs[i][2], pos_hint = {'center_x':0.5}, font_style = "H5", size_hint_x = 0.7))
            self.card.add_widget(MDIconButton(icon='dots-vertical', pos_hint = {'center_y':0.5}, size_hint_x = 0.2))

    def musicplayer(self, instance):
        self.index = int(instance.children[6].text)
        self.manager.get_screen('musicplayer').playlist = True
        try:
           self.manager.get_screen('musicplayer').playlist_songs = self.song_infos[self.index::]
        except:
           self.manager.get_screen('musicplayer').playlist_songs = None
        self.manager.get_screen('musicplayer').prev_screen = 'playlist_songs'
        self.manager.get_screen("musicplayer").song_name = instance.children[4].text
        self.manager.current = 'musicplayer'

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
    
    def go_back(self):
        print(self.manager.transition.direction)
        self.manager.transition.direction = 'right'
        self.manager.current = 'playlist'
        self.manager.transition.direction = 'left'


class spotify(MDApp):
    def build(self):
       Database.connect()
       self.icon = 'images/bheeshma parvam.jpg'
       self.title = "Music Player"
       self.theme_cls.theme_style = "Dark"
       self.theme_cls.primary_hue = "A100"
       self.theme_cls.primary_palette = "Blue"
       sm = MDScreenManager()
       #sm.add_widget(Welcome(name='welcome'))

       sm.add_widget(WelcomeScreen(name=''))
       sm.add_widget(LoginScreen(name='login'))
       sm.add_widget(RegistrationScreen(name='registration'))
       sm.add_widget(AITextArtScreen(name='aiart'))
       sm.add_widget(MusicPlayer(name='musicplayer'))
       sm.add_widget(SearchScreen(name='search'))
       sm.add_widget(Playlist(name = 'playlist'))
       sm.add_widget(Playlist_Songs(name='playlist_songs'))
       return sm

if __name__ == '__main__':
    spotify().run()
