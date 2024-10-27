from langchain.tools import StructuredTool
import time
from datetime import datetime as dt
from toastify import notify
import json
import azapi
import lyricsgenius
from lyrics_extractor import SongLyrics
from gtts import gTTS
from playsound import playsound
from kivymd.uix.pickers import MDTimePicker
from kivy.core.text import LabelBase
import random
from langchain import SQLDatabase
from langchain.utilities import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.chains import SQLDatabaseSequentialChain
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.tools.file_management import (
    ReadFileTool, MoveFileTool, WriteFileTool)
from langchain.agents.agent_toolkits import GmailToolkit
from datetime import datetime
from langchain.memory import ConversationBufferMemory
from langchain.sql_database import SQLDatabase
import ast
import speech_recognition
import os
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import *
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.graphics import Color
from kivy.animation import Animation
from kivymd.toast import toast
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock
import mysql.connector
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.fitimage import FitImage
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationDrawerHeader, MDNavigationDrawerItem, MDNavigationDrawerDivider, MDNavigationDrawerLabel, MDNavigationDrawerMenu, MDNavigationLayout
from kivymd.uix.list import OneLineListItem
import datetime
from kivymd.uix.slider.slider import MDSlider
from kivy.core.audio import SoundLoader
from kivymd.uix.list.list import MDList, TwoLineAvatarIconListItem, TwoLineRightIconListItem, ImageRightWidget, ImageLeftWidget, IconRightWidget, TwoLineListItem
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.properties import StringProperty
from kivy_gradient import Gradient
from kivymd.uix.selectioncontrol.selectioncontrol import MDSwitch
from pydub import AudioSegment
import numpy as np
import math
from threading import Thread
from kivymd.uix.stacklayout import MDStackLayout
from plyer import filechooser
from datetime import date
from colorthief import ColorThief
from PIL import Image as Im
from kivymd.uix.menu import MDDropdownMenu
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailMenuButton, MDNavigationRailItem
from kivy.graphics.vertex_instructions import Ellipse
from kivymd.uix.imagelist.imagelist import MDSmartTile

account = ("", "", "")
state = 0
logged_in = False

os.environ['OPENAI_API_KEY'] = ""
os.environ['SERPAPI_API_KEY'] = ""

repo_id = "google/flan-t5-xl"
os.environ['HUGGINGFACEHUB_API_TOKEN'] = ''


class Database():  # Intialising Database Class
    cnx = None
    cursor = None

    def connect():  # Connecting to Database
        global cnx
        global cursor
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            database="musicplayer"
        )
        cursor = cnx.cursor()

    def create_account(username, email, phone, password, image):  # Function to create account
        id = int(str((random.random())).split('.')[1])
        today = date.today()
        t = today.strftime("%Y-%m-%d")
        cursor.execute('INSERT INTO users (id, username, email, phone, password, image, created) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                       (id, username, email, phone, password, 'images/account.png', t))
        cnx.commit()
        global account
        global logged_in
        cursor.execute(
            'SELECT username, email, password, phone, image, created FROM users WHERE email=%s AND password = %s', (email, password))
        account = cursor.fetchone()
        logged_in = True
        return True, account

    def login(email, password):  # Function to login to account
        cursor.execute(
            'SELECT username, email, password, phone, image, created FROM users WHERE email=%s AND password = %s', (email, password))
        global account
        global logged_in
        account = cursor.fetchone()
        if account:
            logged_in = True
            return True, account
        else:
            return False

    def acc_details():  # Function to get account details
        if logged_in:
            return account

    # Function to edit account details
    def account_edit(acc, username=None, email=None, password=None, image=None):
        global account
        if username:
            cursor.execute(
                "UPDATE users SET username = %s WHERE username = %s", (username, acc[0]))
            cnx.commit()

        if email:
            cursor.execute(
                "UPDATE users SET email = %s WHERE email = %s", (email, acc[1]))
            cnx.commit()

        if password:
            cursor.execute(
                "UPDATE users SET password = %s WHERE password = %s", (password, acc[2]))
            cnx.commit()

        if image:
            cursor.execute(
                "UPDATE users SET image = %s WHERE username = %s", (image, acc[0]))
            cnx.commit()

        cursor.execute(
            "SELECT username, email, password, phone, image, created FROM users WHERE email=%s", (email if email != None else account[1], ))
        account = cursor.fetchone()

    def playlist_count(username):  # Function to take count of playlists
        cursor.execute(
            f"SELECT count(*) FROM playlists WHERE user = '{username}'")
        return cursor.fetchone()

    def music(limit, rec=None, lang=None, genre=None):  # Function to fetch music from database

        if rec == None and lang == None:
            cursor.execute(
                f"SELECT * FROM songs ORDER BY RAND() LIMIT {limit}")
            result = cursor.fetchall()
            return result

        elif lang == None:
            cursor.execute(
                f"SELECT * FROM songs ORDER BY RAND() LIMIT {limit}")

            result = cursor.fetchall()
            return result

        elif rec == None:
            cursor.execute(
                f"SELECT * FROM songs WHERE language = '{lang}' ORDER BY RAND() LIMIT {limit}")

            result = cursor.fetchall()
            return result

        elif lang != None and genre != None:
            cursor.execute(
                f"SELECT * FROM songs WHERE language = {lang} AND genre = {genre} ORDER BY RAND() LIMIT {limit}")

            result = cursor.fetchall()

            if result == []:
                cursor.execute(
                    f"SELECT * FROM songs WHERE language = {lang} ORDER BY RAND() LIMIT {limit}")
                result = cursor.fetchall()

            return result

    def get_song_detail(name=None, id=None):  # Function to get song detail
        try:
            if name:
                cursor.execute("SELECT * FROM songs WHERE title = %s", (name,))
                result = cursor.fetchone()
                return result
            elif id:
                cursor.execute("SELECT * FROM songs WHERE id = %s", (id, ))
                result = cursor.fetchone()
                return result
        except Exception as e:
            return "None"

    def song_match(text):  # Function to search song
        try:
            cursor.execute(
                f"SELECT * FROM songs WHERE title LIKE '{text}%' OR composer LIKE '%{text}%' OR image LIKE '%{text}%' OR language LIKE '%{text}%' OR genre LIKE '%{text}%' GROUP BY title LIMIT 20")
            result = cursor.fetchall()
            return result
        except:
            pass

    # Function to get info about playlists
    def playlists_info(username=None, id=None, play_name=None):
        try:
            if username and play_name == None:
                cursor.execute(
                    "SELECT * FROM playlists WHERE user = %s", (username, ))
                result = cursor.fetchall()
                return result
            elif id:
                cursor.execute("SELECT * FROM playlists WHERE id = %s", (id, ))
                result = cursor.fetchone()
                return result
            elif play_name and username:
                cursor.execute(
                    f"SELECT * FROM playlists WHERE name = '{play_name}' AND user = '{username}'")
                result = cursor.fetchone()
                return result
        except:
            return 0

    def create_playlist(name, image, user, date, colours):  # Function to create playlist
        try:
            cursor.execute(
                "INSERT INTO playlists (name, image, user, created, colour) VALUES (%s, %s, %s, %s, %s)", (name, image, user, date, colours))
            cnx.commit()
        except Exception:
            raise Exception

    def playlist_songs(id, order_by=None):  # Function to get songs in playlists
        try:
            if order_by != None:
                cursor.execute(
                    f"SELECT * FROM playlist_songs WHERE playlist_id = {id} ORDER BY {order_by}")
                result = cursor.fetchall()
                return result
            else:
                cursor.execute(
                    "SELECT * FROM playlist_songs WHERE playlist_id = %s", (id, ))
                result = cursor.fetchall()
                return result
        except Exception:
            raise Exception

    # Function to add songs to playlist
    def add_playlist_song(playlist_id, song_id, song_name):
        today = date.today().strftime("%Y/%m/%d")
        try:
            cursor.execute(
                "INSERT INTO playlist_songs (playlist_id, song_id, song_name, created) VALUES (%s, %s, %s, %s)", (playlist_id, song_id, song_name, today))
            cnx.commit()
        except Exception as e:
            raise Exception

    def delete_playlist(playlist_id):  # Function to delete a playlist
        try:

            cursor.execute(
                f"DELETE FROM playlist_songs WHERE playlist_id = {playlist_id}")
            cnx.commit()

            cursor.execute(f"DELETE FROM playlists WHERE id = {playlist_id}")
            cnx.commit()

        except Exception:
            raise Exception

    # Function to delete song from playlist
    def delete_playlist_song(playlist_id, song_id):
        try:
            cursor.execute(
                f'DELETE FROM playlist_songs WHERE playlist_id = {playlist_id} AND song_id = {song_id}')
            cnx.commit()
        except Exception:
            raise Exception

    # Function to edit playlist details
    def playlist_edit(playlist_id, rename=None, image=None):
        try:
            if rename:
                cursor.execute(
                    "UPDATE playlists SET name = %s WHERE id = %s", (rename, playlist_id, ))
                cnx.commit()
            elif image:
                cursor.execute(
                    "UPDATE playlists SET image = %s WHERE id = %s", (image, playlist_id, ))
                cnx.commit()
        except Exception:
            raise Exception

    # Add song to listening history
    def add_to_listening_history(song_id, username, author, language, genre):
        cursor.execute(
            "INSERT INTO listening_history VALUES(%s, %s, %s, %s, %s)", (song_id, username, author, language, genre))
        cnx.commit()

    def top_played(username):  # Function to get top 3 played songs
        cursor.execute(
            f"SELECT song_id FROM listening_history WHERE username='{username}' GROUP BY song_id ORDER BY count(*) DESC LIMIT 3")
        l = cursor.fetchall()
        return l

    def recommendations(username):  # Function to get song recommendations
        cursor.execute(f"""select s.id, s.title, s.composer, s.image, s.mp3, s.language, s.genre from songs s, listening_history lh WHERE s.id NOT IN (SELECT DISTINCT song_id FROM listening_history WHERE username = '{username}') 
                       AND ((s.language, s.genre) IN (SELECT language, genre FROM listening_history WHERE username = '{username}' GROUP BY genre) 
                       OR s.composer IN (SELECT DISTINCT composer FROM listening_history WHERE username = '{username}')) GROUP BY s.title ORDER BY RAND() LIMIT 8""")
        return cursor.fetchall()


class LoginScreen(MDScreen, MDFloatLayout):  # Initialising Login Screen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        LabelBase.register(
            name='cracky', fn_regular='fonts/CurlzMT.ttf', fn_bold='fonts/CURLZ.ttf')  # Registering A new font

        self.login_form = MDCard(orientation='vertical',
                                 size_hint=(0.3, 0.5),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 elevation=5, spacing="10dp", padding="40dp", md_bg_color=[0, 0, 0, 0.8])
        self.img = FitImage(source='images/login.jpg',)
        self.add_widget(self.img)

        self.app_img = Image(source='images/Chorduce icon.png')
        self.login_form.add_widget(self.app_img)

        self.email = MDTextField(mode='rectangle', icon_left='email',
                                 hint_text="Email", helper_text_mode='on_error', line_anim=True, size_hint=(0.8, 0.5), pos_hint={'center_x': 0.5, 'top': 1})
        self.password = MDTextField(hint_text="Password", password=True, mode='rectangle', helper_text_mode='on_error',
                                    line_anim=True, size_hint=(0.8, 0.5), pos_hint={'center_x': 0.5, 'top': 1}, icon_left='key')

        self.login_form.add_widget(self.email)
        self.login_form.add_widget(self.password)

        self.login_button = MDRectangleFlatButton(
            text="Login", pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.login_button.bind(on_press=lambda x: self.login())
        self.login_form.add_widget(self.login_button)
        self.create_account_button = MDRectangleFlatButton(
            text="Create Account", pos_hint={'center_x': 0.5, 'center_y': 0.8})
        self.create_account_button.bind(on_release=lambda y: self.reg())

        self.login_form.add_widget(self.create_account_button)
        self.add_widget(self.login_form)

    def login(self):  # Function to login
        status = Database.login(email=self.email.text,
                                password=self.password.text)
        if status:
            self.manager.add_widget(SplashScreen(name='splashy'))
            self.manager.current = 'splashy'
        else:
            self.email.error = True
            self.password.error = True

    def reg(self):  # Change to registration screen
        self.manager.current = 'registration'
        self.manager.transition.direction = 'left'


class RegistrationScreen(MDScreen):  # Initialising Registration Screen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.back_button = MDIconButton(
            icon='arrow-left', pos_hint={'top': 1, 'left': 1})
        self.back_button.bind(on_release=lambda x: self.back())
        self.add_widget(self.back_button)

        self.registration_form = MDCard(orientation='vertical', size_hint=(
            0.35, 0.55), pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing="12dp", padding=[20, 30, 20, 30])

        self.text = MDLabel(text="[font=cracky]Registration[/font]",
                            halign='center', font_style="H1", bold=True, font_family="fonts/CurlzMT.ttf", markup=True)
        self.username = MDTextField(
            hint_text="Username", mode='rectangle', size_hint_x=0.65, pos_hint={'center_x': 0.5}, icon_left='account')
        self.email = MDTextField(
            hint_text='Email', mode='rectangle', size_hint_x=0.65, pos_hint={'center_x': 0.5}, icon_left='email')
        self.phone = MDTextField(
            hint_text='Phone', mode='rectangle', size_hint_x=0.65, pos_hint={'center_x': 0.5}, icon_left='phone')
        self.password = MDTextField(hint_text='Password', password=True,
                                    helper_text="Passwords doesnt match", helper_text_mode="on_error", mode='rectangle', size_hint_x=0.65, pos_hint={'center_x': 0.5}, icon_left='key')
        self.conf_pass = MDTextField(hint_text='Confirm Password', password=True,
                                     helper_text="Passwords doesnt match", helper_text_mode="on_error", mode='rectangle', size_hint_x=0.65, pos_hint={'center_x': 0.5}, icon_left='key')
        self.registration_form.add_widget(self.text)
        self.registration_form.add_widget(self.username)
        self.registration_form.add_widget(self.email)
        self.registration_form.add_widget(self.phone)
        self.registration_form.add_widget(self.password)
        self.registration_form.add_widget(self.conf_pass)

        self.register_button = MDRectangleFlatButton(
            text='Create Account', pos_hint={'center_x': 0.5})
        self.register_button.bind(on_release=self.register)
        self.registration_form.add_widget(self.register_button)

        self.add_widget(self.registration_form)

    def back(self):  # Go back to login screen
        self.manager.current = 'login'
        self.manager.transition.direction = 'right'

    def register(self, dt):  # Registering a new account
        if self.password.text == self.conf_pass.text:
            Database.create_account(
                self.username.text, self.email.text, self.phone.text, self.password.text, 'images/account.png')
            self.manager.add_widget(MainScreen(name='main'))
            self.manager.current = 'main'
            self.manager.transition.direction = 'left'
        else:
            self.password.error = True
            self.conf_pass.error = True


class SplashScreen(MDScreen):  # Initialising Splash Screen
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LabelBase.register(name='mercy',
                           fn_regular='fonts/Mercy Christole.ttf')

        with self.canvas.before:
            Color(1, 1, 1, mode='hex')
            self.rect = Rectangle(texture=Gradient.horizontal(get_color_from_hex('#7F7FD5'), get_color_from_hex('#91EAE4')),
                                  size=Window.size)
        Window.bind(on_resize=self.resize)
        self.md_bg_color = [0, 0, 0, 0]
        self.username = Database.acc_details()[0]

        self.img = Image(source='images/Chorduce icon.png',
                         size_hint=(0.1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.95})
        self.add_widget(self.img)

        self.animation1 = Animation(size_hint=(
            0.5, 0.5), duration=5.0, transition='in_out_bounce', pos_hint={'center_x': 0.5, 'center_y': 0.5}) + Animation(size_hint=(0.3, 0.3), duration=2, pos_hint={
                'center_x': 0.5, 'center_y': 0.55}, transition='out_quad')
        self.animation1.bind(
            on_complete=self.loading)
        self.animation1.start(self.img)

    def loading(self, anim, widget):  # Executing animations and initializing spinner and adding label
        self.spinner = MDSpinner(size_hint=(0.025, 0.025), pos_hint={'center_x': 0.5, 'center_y': 0.3}, palette=[
            [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
            [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
            [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
            [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
        ])
        self.animation2 = Animation(size_hint=(
            0.32, 0.32), duration=1)+Animation(size_hint=(0.3, 0.3), duration=1)
        part = self.times_of_day(dt.now().hour)
        self.add_widget(self.spinner)
        self.spinner.active = False
        self.animation2.repeat = True
        self.animation2.start(self.img)
        self.spinner.active = True

        self.label = MDLabel(text=f"[font=mercy]Good {part}, {self.username}[/font]", pos_hint={
                             'center_x': 0.5, 'center_y': 0.84}, bold=True, font_style='H1', halign='center', italic=True, markup=True, size_hint=(3, 3))
        self.add_widget(self.label)
        Clock.schedule_once(self.add_screens)

    def add_screens(self, dt):  # Adding other screens
        self.manager.add_widget(MainScreen(name='main'))
        self.manager.add_widget(Playlist(name='playlist'))
        self.manager.add_widget(Playlist_Songs(name='playlist_songs'))
        self.manager.add_widget(UserProfile(name='profile'))
        self.manager.add_widget(Settings(name='settings'))
        self.manager.add_widget(SearchScreen(name='search'))
        self.animation2.stop(self.img)
        self.spinner.active = False
        self.manager.current = 'main'

    def times_of_day(self, h):  # Getting the time of day
        return (
            "Morning"
            if 1 <= h < 12
            else "Afternoon"
            if 12 <= h < 17
            else "Evening"
        )

    def resize(self, window, width, height):  # Resize background gradient w.r.t screen resizing
        self.rect.size = Window.size


class MainScreen(MDScreen):  # Initialising the MainScreen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bass = False
        self.new_recs = False
        self.recs_details = []
        self.counter = 0

        self.update_recs = Clock.create_trigger(self.recommendation_updated)
        self.bass_event = Clock.create_trigger(self.bass_confirmation)

        with self.canvas.before:
            Color(0, 0, 0.3, mode='hex')
            self.rect = Rectangle(texture=Gradient.vertical([0, 0, 0.3, 0.3], [0, 0, 0.5, 0.5], [0, 0, 1, 0.5]),
                                  size=Window.size)
        Window.bind(on_resize=self.resize)

        account = Database.acc_details()
        self.sound = None
        self.paused = True
        self.song_name = None
        self.prev_sn = None
        self.song_author = StringProperty()
        self.song_image = 'None'
        self.counter = 0

        self.scroll_view = MDScrollView(do_scroll_x=False, pos_hint={'top': 0.93}, size_hint_y=0.9, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                        always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll_view)

        self.main_layout = MDBoxLayout(orientation='vertical', size_hint_y=None,
                                       height="1800dp", width="50dp", spacing="10dp", padding="20dp")
        self.scroll_view.add_widget(self.main_layout)

        self.recommended_section = MDGridLayout(
            size_hint_y=5, width=Window.minimum_width, cols=10, spacing="30dp", padding="25dp", pos_hint={'center_x': 0.545, 'top': 1})
        self.recommended_label = MDLabel(
            text='Recommended Songs', font_style='H4', size_hint_y=None, height=Window.minimum_height, bold=True, pos_hint={'center_x': 0.545, 'top': 1})
        self.main_layout.add_widget(self.recommended_label)
        self.main_layout.add_widget(self.recommended_section)

        self.malayalam_section = MDGridLayout(
            size_hint_y=5, width=Window.minimum_width, cols=10, spacing="30dp", padding="25dp", pos_hint={'center_x': 0.545, 'top': 1})
        self.malayalam_label = MDLabel(
            text='Malayalam Songs', font_style='H4', size_hint_y=None, height=Window.minimum_height, bold=True, pos_hint={'center_x': 0.545, 'top': 1})
        self.main_layout.add_widget(self.malayalam_label)
        self.main_layout.add_widget(self.malayalam_section)

        self.english_section = MDGridLayout(
            size_hint_y=5, width=Window.minimum_width, cols=10, spacing="30dp", padding="25dp", pos_hint={'center_x': 0.545, 'top': 1})
        self.english_label = MDLabel(text='English Songs', font_style='H4',
                                     size_hint_y=None, height=Window.minimum_height, bold=True, pos_hint={'center_x': 0.545, 'top': 1})
        self.main_layout.add_widget(self.english_label)
        self.main_layout.add_widget(self.english_section)

        self.hindi_section = MDGridLayout(
            size_hint_y=5, width=Window.minimum_width, cols=10, spacing="30dp", padding="25dp", pos_hint={'center_x': 0.545, 'top': 1})
        self.hindi_label = MDLabel(text='Hindi Songs', font_style='H4',
                                   size_hint_y=None, height=Window.minimum_height, bold=True, pos_hint={'center_x': 0.545, 'top': 1})
        self.main_layout.add_widget(self.hindi_label)
        self.main_layout.add_widget(self.hindi_section)

        self.tamil_section = MDGridLayout(
            size_hint_y=5, width=Window.minimum_width, cols=10, spacing="30dp", padding="25dp", pos_hint={'center_x': 0.545, 'top': 1})
        self.tamil_label = MDLabel(text='Tamil Songs', font_style='H4',
                                   size_hint_y=None, height=Window.minimum_height, bold=True, pos_hint={'center_x': 0.545, 'top': 1})
        self.main_layout.add_widget(self.tamil_label)
        self.main_layout.add_widget(self.tamil_section)

        self.false_section = MDGridLayout(
            size_hint_y=0.5, width=Window.minimum_width, cols=10, spacing="30dp", padding="25dp", pos_hint={'center_x': 0.545, 'top': 1})
        self.false_label = MDLabel(
            text='', font_style='H4', size_hint_y=None, height=Window.minimum_height, bold=True, pos_hint={'center_x': 0.545, 'top': 1})
        self.main_layout.add_widget(self.false_label)
        self.main_layout.add_widget(self.false_section)

        # fetching music from database
        s1 = Database.music(limit=8)
        s2 = Database.music(limit=8, lang='malayalam')
        s3 = Database.music(limit=8, lang='english')
        s4 = Database.music(limit=8, lang='hindi')
        s5 = Database.music(limit=8, lang='tamil')

        for i in s1:
            self.card1 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))
            self.card1.add_widget(Image(source=i[3]))
            self.card1.add_widget(
                MDLabel(text=i[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card1.add_widget(
                MDLabel(text=i[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card1.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.recommended_section.add_widget(self.card1)

        for x in s2:
            self.card2 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))
            self.card2.add_widget(Image(source=x[3]))
            self.card2.add_widget(
                MDLabel(text=x[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card2.add_widget(
                MDLabel(text=x[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card2.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.malayalam_section.add_widget(self.card2)

        for y in s3:
            self.card3 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))
            self.card3.add_widget(Image(source=y[3]))
            self.card3.add_widget(
                MDLabel(text=y[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card3.add_widget(
                MDLabel(text=y[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card3.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.english_section.add_widget(self.card3)

        for z in s4:
            self.card4 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))
            self.card4.add_widget(Image(source=z[3]))
            self.card4.add_widget(
                MDLabel(text=z[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card4.add_widget(
                MDLabel(text=z[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card4.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.hindi_section.add_widget(self.card4)

        for q in s5:
            self.card5 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))
            self.card5.add_widget(Image(source=q[3]))
            self.card5.add_widget(
                MDLabel(text=q[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card5.add_widget(
                MDLabel(text=q[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card5.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.tamil_section.add_widget(self.card5)

        self.layout = MDCard(size_hint=(1, 0.1), pos_hint={
            'center_x': 0.5, 'bottom': 1}, md_bg_color=(0, 0, 0, 1), elevation=3)
        self.add_widget(self.layout)
        self.sub_layout1 = MDBoxLayout(size_hint_x=None, width=self.height)
        self.layout.add_widget(self.sub_layout1)

        self.img = Image(source='images/black.jpg',
                         pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.75, 0.75))
        self.sub_layout1.add_widget(self.img)

        self.sub_layout2 = MDBoxLayout(orientation='horizontal')
        self.layout.add_widget(self.sub_layout2)

        self.sub_layout2_1 = MDBoxLayout(
            orientation='vertical', size_hint_x=0.2, spacing="0.5dp", padding="20dp")
        self.sub_layout2.add_widget(self.sub_layout2_1)

        self.song_n = MDLabel(text='', halign="left")
        self.sub_layout2_1.add_widget(self.song_n)
        self.song_auth = MDLabel(text='', halign="left")
        self.sub_layout2_1.add_widget(self.song_auth)

        self.sub_layout5 = MDBoxLayout(orientation='vertical', size_hint_x=0.8, spacing="1dp", padding="20dp", pos_hint={
            'center_x': 0.5, 'center_y': 0.5})
        self.sub_layout2.add_widget(self.sub_layout5)

        self.sub_layout2_1_1 = MDBoxLayout(orientation='horizontal', spacing="5dp", pos_hint={
            'center_x': 0.88, 'center_y': 0.3})
        self.sub_layout5.add_widget(self.sub_layout2_1_1)
        self.skip_prev = MDIconButton(
            icon='skip-previous', halign="center", disabled=True)
        self.skip_prev.bind(
            on_press=self.previous, on_enter=self.enter, on_leave=self.leave)
        self.sub_layout2_1_1.add_widget(self.skip_prev)
        self.play_pause = MDIconButton(icon='play', halign="center", icon_color=[
            0, 0, 0, 1], theme_icon_color="Custom", md_bg_color="white", disabled=True)
        self.sub_layout2_1_1.add_widget(self.play_pause)
        self.skip_next = MDIconButton(
            icon='skip-next', halign="center", disabled=True)
        self.skip_next.bind(on_press=self.next,
                            on_button_enter=self.enter, on_button_leave=self.leave)
        self.sub_layout2_1_1.add_widget(self.skip_next)

        self.sub_layout5_2 = MDBoxLayout(
            orientation='horizontal', spacing="0.1dp", size_hint_x=0.8, padding="5dp")
        self.sub_layout5.add_widget(self.sub_layout5_2)

        self.start = MDLabel(text="00:00", size_hint_x=0.2,
                             font_style="Subtitle2", halign="right")
        self.sub_layout5_2.add_widget(self.start)
        self.slider = MDSlider(
            size_hint_x=0.7, hint=False, disabled=True)
        self.sub_layout5_2.add_widget(self.slider)
        self.end = MDLabel(text="00:00", size_hint_x=0.1,
                           font_style="Subtitle2")
        self.sub_layout5_2.add_widget(self.end)

        self.sub_layout_3 = MDAnchorLayout(
            anchor_x='center', anchor_y='center', size_hint=(0.2, 1))
        self.sub_layout2.add_widget(self.sub_layout_3)

        self.sub_layout_3_1 = MDBoxLayout(orientation='horizontal', size_hint=(
            0.4, None), height=Window.minimum_height, spacing="3dp")
        self.sub_layout_3.add_widget(self.sub_layout_3_1)

        self.lyrics = MDIconButton(
            icon='microphone-variant', on_press=self.go_to_lyrics, disabled=True)
        self.sub_layout_3_1.add_widget(self.lyrics)
        self.switch = MDIconButton(icon='music-accidental-double-flat', on_press=lambda x: Thread(
            target=self.booster, name='Song Booster', daemon=True).start())
        self.sub_layout_3_1.add_widget(self.switch)
        self.repeat = MDIconButton(icon='repeat-off')
        self.sub_layout_3_1.add_widget(self.repeat)
        self.repeat.bind(on_release=self.song_repeat,
                         on_enter=self.enter, on_leave=self.leave)
        self.mute = MDIconButton(
            icon='volume-high', disabled=True, icon_color=[0, 0.5, 1, 1], theme_icon_color="Custom")
        self.mute.bind(on_press=self.mute_func,
                       on_enter=self.enter, on_leave=self.leave)
        self.sub_layout_3_1.add_widget(self.mute)

        self.top_bar = MDTopAppBar(left_action_items=[['menu', lambda x: self.nav_drawer.set_state('open'), "Menu"]],
                                   title="Chorduce",
                                   right_action_items=[
                                       ['magnify', lambda x: self.search(), "Search"]],
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0
                                   )
        self.add_widget(self.top_bar)

        self.nav_drawer = MDNavigationDrawer(
            enable_swiping=True, spacing=dp(25))
        self.nav_menu = MDNavigationDrawerMenu(spacing=dp(35))

        self.nav_header = MDNavigationDrawerHeader(
            title=account[0], text=account[1], title_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_header)

        self.nav_playlist = MDNavigationDrawerItem(
            text='Account', icon="account", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_profile)
        self.nav_menu.add_widget(self.nav_playlist)

        self.nav_playlist = MDNavigationDrawerItem(
            text='Playlist', icon="playlist-music", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)
        self.nav_playlist.bind(on_release=self.to_playlist,
                               on_enter=self.enter, on_leave=self.leave)

        self.nav_divider = MDNavigationDrawerDivider()
        self.nav_menu.add_widget(self.nav_divider)

        self.chatbot = MDNavigationDrawerItem(
            text='Euphonious', icon="robot", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.chatbot)
        self.chatbot.bind(on_release=self.to_chat,
                          on_enter=self.enter, on_leave=self.leave)

        self.nav_settings = MDNavigationDrawerItem(
            text='Settings', icon="tools", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_settings)
        self.nav_menu.add_widget(self.nav_settings)

        self.nav_logout = MDNavigationDrawerItem(
            text='Logout', icon="logout", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_logout.bind(on_release=self.logout,
                             on_enter=self.enter, on_leave=self.leave)
        self.nav_menu.add_widget(self.nav_logout)

        self.nav_layout = MDNavigationLayout()
        self.nav_drawer.add_widget(self.nav_menu)
        self.nav_layout.add_widget(self.nav_drawer)

        self.add_widget(
            MDNavigationRail(
                MDNavigationRailItem(
                    text="HOME",
                    icon="home",
                    on_press=self.to_main,
                ),
                MDNavigationRailItem(
                    text="MUSIC",
                    icon="music",
                    on_press=self.to_player,
                ),
                MDNavigationRailItem(
                    text="ASSISTANT",
                    icon="robot-happy-outline",
                    on_press=lambda x: Thread(
                        target=self.mic_ask, daemon=True).start()
                ),
                md_bg_color=(1, 0, 0, 0),
                pos_hint={'top': 0.92, 'center_x': 0.02},
                size_hint=(0.105, 5),
                padding=[0, 25, 0, 70],
                spacing="390dp"
            )
        )
        self.add_widget(self.nav_layout)

    def go_to_lyrics(self, dt):  # Function to change to lyrics screen
        self.manager.current = 'lyrics'
        self.manager.transition.direction = 'up'

    def to_main(self, dt):  # Function to change to main screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'left'

    def to_player(self, instance):  # Function to change to musicplayer screen
        try:
            self.manager.get_screen('musicplayer').music_icon_clicked = True
            self.manager.get_screen('musicplayer').prev_screen = 'main'
            self.manager.current = 'musicplayer'
            self.manager.transition.direction = 'left'
        except:
            pass

    def to_chat(self, dt):  # Function to change to chat screen
        self.nav_drawer.set_state("close")
        self.manager.current = 'chat'
        self.manager.transition.direction = 'left'

    def enter(self, instance):  # Function to change cursor icon when it is in focus with widget and increase its elevation
        Window.set_system_cursor(cursor_name='hand')
        instance.elevation = 3

    def leave(self, instance):  # Function to change cursor icon when it is out of focus with widget and increase its elevation
        Window.set_system_cursor(cursor_name='arrow')
        instance.elevation = 0

    # Function to resize bacgkround gradient colour w.r.t change in screen size
    def resize(self, window, width, height):
        self.rect.size = Window.size

    def logout(self, dt):  # Function to logout
        self.manager.remove_widget(MainScreen(name='main'))
        self.manager.current = 'login'
        self.manager.transition.direction = 'left'

    def to_playlist(self, dt):  # Functiom to change to playlist screen
        self.nav_drawer.set_state('close')
        self.manager.current = 'playlist'
        self.manager.transition.direction = 'left'

    def song(self, instance):  # Function to change to musicplayer screen
        self.song_name = instance.children[1].text
        self.manager.get_screen("musicplayer").playlist = False
        self.manager.get_screen('musicplayer').playlist_songs = None
        self.manager.get_screen('musicplayer').prev_screen = 'main'
        self.manager.get_screen("musicplayer").song_name = self.song_name
        self.manager.get_screen("musicplayer").clicked = True

        if self.manager.get_screen("musicplayer").sound and self.manager.get_screen("musicplayer").sn != self.song_name:
            self.manager.get_screen("musicplayer").sound.stop()

        self.manager.current = 'musicplayer'
        self.manager.transition.direction = 'left'

    def next(self, dt):  # Function to play next song
        self.manager.get_screen("musicplayer").prev_button.disabled = False
        self.skip_prev.disabled = False
        self.manager.get_screen("musicplayer").clicked = False
        self.manager.get_screen("musicplayer").new = True
        self.manager.get_screen("musicplayer").paused = False
        self.manager.get_screen("musicplayer").play_button.icon = 'play'
        self.manager.get_screen("musicplayer").slider.value = 0
        self.manager.get_screen("musicplayer").sound.stop()

    def previous(self, dt):  # Function to play previous song
        self.manager.get_screen("musicplayer").clicked = False
        self.manager.get_screen("musicplayer").prev = True
        self.manager.get_screen("musicplayer").new = True
        self.manager.get_screen("musicplayer").index -= 1
        if self.manager.get_screen("musicplayer").index == -(len(self.manager.get_screen("musicplayer").played_songs)):
            self.manager.get_screen("musicplayer").prev_button.disabled = True
            self.skip_prev.disabled = True
        else:
            self.manager.get_screen("musicplayer").prev_button.disabled = False
            self.skip_prev.disabled = False
        song = self.manager.get_screen(
            "musicplayer").played_songs[self.manager.get_screen("musicplayer").index]

        self.manager.get_screen("musicplayer").paused = False
        self.manager.get_screen("musicplayer").play_button.icon = 'play'
        self.manager.get_screen("musicplayer").sound.stop()
        self.manager.get_screen("musicplayer").slider.value = 0
        Clock.unschedule(self.manager.get_screen("musicplayer").update_slider)
        Clock.unschedule(self.manager.get_screen("musicplayer").update_time)

        self.manager.get_screen("musicplayer").sn = song[1]

        self.manager.get_screen("musicplayer").bg_image.source = song[3]
        self.manager.get_screen("musicplayer").song_title.text = song[1]
        self.manager.get_screen("musicplayer").song_author.text = song[2]
        self.manager.get_screen("musicplayer").song_image.source = song[3]

        self.manager.get_screen(
            "musicplayer").sound = SoundLoader.load(song[4])
        self.manager.get_screen("musicplayer").start_time.text = "00:00"
        self.manager.get_screen("musicplayer").end_time.text = self.convert_seconds_to_min(
            self.manager.get_screen("musicplayer").sound.length)
        self.manager.get_screen("musicplayer").sound.play()
        self.manager.get_screen("musicplayer").sound.bind(
            on_stop=self.manager.get_screen("musicplayer").on_stop)
        self.manager.get_screen("musicplayer").play_button.icon = 'pause'
        self.manager.get_screen("musicplayer").play_button.bind(
            on_press=self.manager.get_screen("musicplayer").play_pause)

        Clock.schedule_interval(self.manager.get_screen(
            "musicplayer").update_slider, 1)
        Clock.schedule_interval(
            self.manager.get_screen("musicplayer").update_time, 1)
        self.manager.get_screen("musicplayer").prev = False
        self.sound = self.manager.get_screen("musicplayer").sound
        self.is_playing = self.manager.get_screen("musicplayer").paused
        self.song_name = self.manager.get_screen("musicplayer").song_title.text
        self.song_n.text = self.manager.get_screen(
            "musicplayer").song_title.text
        self.song_author = self.manager.get_screen(
            "musicplayer").song_author.text
        self.song_auth.text = self.manager.get_screen(
            "musicplayer").song_author.text
        self.song_image = self.manager.get_screen(
            "musicplayer").song_image.source
        self.img.source = self.manager.get_screen(
            "musicplayer").song_image.source
        self.end.text = self.manager.get_screen("musicplayer").convert_seconds_to_min(
            self.manager.get_screen("musicplayer").sound.length)

    def search(self):  # Function to change to search screen
        self.manager.current = 'search'
        self.manager.transition.direction = 'left'

    def on_pre_enter(self):  # Function called just before entering the screen
        self.counter += 1
        l = [1, 15, 35, 50, 75, 100]
        self.account = Database.acc_details()
        try:
            with open("Settings/settings.json") as f:
                data = json.load(f)
                recs = data['Recommendations']
            if self.counter in l and recs == 'Enabled':
                Thread(target=self.ai_recommendation, daemon=True).start()
        except:
            pass
        for card in self.recommended_section.children:
            card.focus_color = (31, 31, 31, 0.15)

        for card in self.malayalam_section.children:
            card.focus_color = (31, 31, 31, 0.15)

        for card in self.english_section.children:
            card.focus_color = (31, 31, 31, 0.15)

        for card in self.hindi_section.children:
            card.focus_color = (31, 31, 31, 0.15)

        for card in self.tamil_section.children:
            card.focus_color = (31, 31, 31, 0.15)

        if self.counter == 0:
            self.counter += 1

        elif self.counter > 0 and self.sound != None:
            self.slider.disabled = False
            self.mute.disabled = False
            self.counter += 1
            self.img.source = self.song_image
            self.song_n.text = self.song_name
            self.song_auth.text = self.song_author
            self.end.text = self.convert_seconds_to_min(self.sound.length)
            self.slider.bind(on_touch_up=self.touch_up,
                             on_enter=self.enter, on_leave=self.leave)
            self.play_pause.icon = (
                'play' if self.sound.state == 'stop' else 'pause')
            self.play_pause.bind(on_press=self.playpause,
                                 on_enter=self.enter, on_leave=self.leave)
            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)

    def booster(self):  # Function to boost song base
        if self.sound and self.switch.theme_icon_color != "Custom":
            self.switch.icon_color = [0, 0.5, 1, 1]
            self.switch.theme_icon_color = "Custom"
            BassBoost.audio(path=self.sound.source)
            self.sound.source = self.sound.source.replace(
                '.mp3', '-boosted.mp3')
            self.sound.seek((self.slider.value/100)*self.sound.length)
            self.sound.play()
            self.bass = True
            self.bass_event()
        elif self.sound:
            self.sound.source = self.sound.source.replace(
                '-boosted.mp3', '.mp3')
            self.sound.seek((self.slider.value/100)*self.sound.length)
            self.sound.play()
            self.bass = False
            self.switch.theme_icon_color = "Primary"
            self.bass_event()

    # Function to confirm play of bass-boosted version of song
    def bass_confirmation(self, dt):
        if self.bass == True:
            toast(text="Bass enabled for the current song!", duration=5)
        else:
            toast(text="Bass disabled", duration=5)

    def update_slider(self, dt):  # Function to update slider position w.r.t song
        self.slider.value = (self.sound.get_pos() / self.sound.length) * 100

    def update_time(self, dt):  # Function to update time w.r.t song
        total_seconds = int(self.sound.get_pos())
        current_minute = total_seconds // 60
        current_seconds = total_seconds - current_minute * 60
        current_time = f"{current_minute:02}:{current_seconds:02}"
        self.start.text = current_time

    # Function to move slider position and seek song to the position of slider
    def touch_up(self, touch, widget):
        if widget.pos[1] < 50:
            if self.sound:
                self.sound.seek((self.slider.value/100)*self.sound.length)

    # Function to convert seconds to minute
    def convert_seconds_to_min(self, sec):
        val = str(datetime.timedelta(seconds=sec)).split(':')
        return f'{val[1]}:{val[2].split(".")[0]}'

    def playpause(self, dt):  # Function to play/pause song
        global current_pos
        if self.sound.state == 'play':
            self.paused = True
            self.manager.get_screen('musicplayer').paused = True
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
                    self.manager.get_screen('musicplayer').paused = False

    def song_repeat(self, dt):  # Function to enable song repeat mode
        if self.sound and self.repeat.icon == 'repeat-off':
            self.repeat.icon = 'repeat'
            self.repeat.icon_color = [0, 0.5, 1, 1]
            self.repeat.theme_icon_color = "Custom"
            self.sound.loop = True
            toast(text="Loop enabled for the current song", duration=5)
        elif self.sound:
            self.repeat.icon = 'repeat-off'
            self.repeat.theme_icon_color = "Primary"
            self.sound.loop = False
            toast(text="Loop disabled", duration=5)

    def mute_func(self, dt):  # Function to mute/Change volume of song
        if self.sound and self.mute.icon == 'volume-high':
            self.mute.icon = 'volume-variant-off'
            self.mute.theme_icon_color = "Primary"
            self.sound.volume = 0
            toast(text="Sound Muted", duration=5)
        elif self.sound and self.mute.icon == 'volume-variant-off':
            self.mute.icon = 'volume-low'
            self.mute.icon_color = [0, 0.5, 1, 1]
            self.mute.theme_icon_color = "Custom"
            self.sound.volume = 0.15
            toast(text="Sound Enabled", duration=5)
        elif self.sound and self.mute.icon == 'volume-low':
            self.mute.icon = 'volume-medium'
            self.mute.icon_color = [0, 0.5, 1, 1]
            self.mute.theme_icon_color = "Custom"
            self.sound.volume = 0.5
        elif self.sound and self.mute.icon == 'volume-medium':
            self.mute.icon = 'volume-high'
            self.mute.icon_color = [0, 0.5, 1, 1]
            self.mute.theme_icon_color = "Custom"
            self.sound.volume = 1

    def mic_ask(self):  # Function to enable the assistant speech engine
        self.recognizer = speech_recognition.Recognizer()
        try:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)

                audio = self.recognizer.listen(mic)
                text = self.recognizer.recognize_google(audio).lower()
                y = self.sound.volume
                self.sound.volume = 0.2

                x = AIChatBot.output(text)
                tts = gTTS(x, slow=False)
                tts.save('ai.mp3')
                playsound('ai.mp3')
                os.remove('ai.mp3')
                self.sound.volume = y

        except Exception as e:
            print(e)

    def to_profile(self, dt):  # Function to change to user account screen
        self.manager.get_screen('profile').acc_details = self.account
        self.manager.current = 'profile'
        self.manager.transition.direction = 'left'

    def to_settings(self, dt):  # Function to change to settings screen
        self.manager.current = 'settings'
        self.manager.transition.direction = 'left'

    # Function to get song recommendation based on user's listening history
    def ai_recommendation(self):
        self.recs_details = Database.recommendations(username=self.account[0])
        if self.recs_details != []:
            self.new_recs = True
            self.update_recs()

    # Function to update the recommended section with the new recommended songs
    def recommendation_updated(self, dt):
        self.recommended_section.clear_widgets()

        for i in self.recs_details:
            self.card1 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))
            self.card1.add_widget(Image(source=i[3]))
            self.card1.add_widget(
                MDLabel(text=i[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card1.add_widget(
                MDLabel(text=i[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card1.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.recommended_section.add_widget(self.card1)

        self.recs_details = []
        self.new_recs = False


class MusicPlayer(MDScreen):  # Initialising the music player screen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clicked = False
        self.prev = False
        self.stop = False
        self.next_song = []
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
        self.new = True
        self.counter2 = 0
        self.counter3 = 0
        self.played_songs = []
        self.index = -1
        self.sn = None
        self.already_started = False
        self.playlist_started = False
        self.queue_counter = 0
        self.music_icon_clicked = False

    def on_pre_enter(self, *args):  # Function called just before entering the screen
        self.song = Database.get_song_detail(name=self.song_name)

        if self.finished == True and self.counter == 0:
            Database.add_to_listening_history(
                song_id=self.song[0], username=self.manager.get_screen('main').account[0], author=self.song[2], language=self.song[5], genre=self.song[6])
            self.manager.get_screen("main").skip_next.disabled = False
            self.manager.get_screen("main").play_pause.disabled = False
            self.clicked = False

            self.stop = True
            self.counter += 1
            self.sn = self.song[1]

            self.sound = SoundLoader.load(self.song[4])
            self.sound.play()
            self.is_playing = True
            self.bg_image = FitImage(
                source=self.song[3]+'-bg.png', opacity='0.5')
            self.add_widget(self.bg_image)

            self.back = MDIconButton(
                icon='chevron-left', pos_hint={'top': 1, 'left': 0.85})
            self.back.bind(on_press=self.go_back)
            self.add_widget(self.back)

            self.song_image = Image(source=self.song[3], pos_hint={
                                    'left': 1.0, 'center_x': 0.1}, keep_ratio=True)
            self.add_widget(self.song_image)
            self.song_title = MDLabel(text=self.song[1], pos_hint={
                                      'left': 1.0, 'center_x': 0.7, 'center_y': 0.5}, bold=True, font_style="H2", size_hint=(1, 0.1), padding=(0, dp(4)))
            self.add_widget(self.song_title)
            self.song_author = MDLabel(text=self.song[2], pos_hint={
                                       'left': 1.0, 'center_x': 0.7, 'center_y': 0.45}, font_style="H6", size_hint=(1, 0.1), padding=(0, dp(4)))
            self.add_widget(self.song_author)

            self.slider = MDSlider(pos_hint={'center_x': 0.5, 'center_y': 0.2}, size_hint=(
                0.5, 0.1), hint=False, on_touch_up=self.touch_down)
            self.add_widget(self.slider)

            self.start_time = MDLabel(text="00:00", pos_hint={
                                      'center_x': 0.33, 'center_y': 0.2}, id='start_time', size_hint=(0.2, 0.1), font_style="Subtitle1")
            self.add_widget(self.start_time)
            self.end_time = MDLabel(text=self.convert_seconds_to_min(self.sound.length), pos_hint={
                                    'center_x': 0.85, 'center_y': 0.2}, id='end_time', size_hint=(0.2, 0.1), font_style="Subtitle1")
            self.add_widget(self.end_time)

            self.play_button = MDIconButton(icon='pause', pos_hint={'center_x': 0.5, 'center_y': 0.1}, icon_color=[
                                            0, 0, 0, 1], theme_icon_color="Custom", md_bg_color="white")
            self.add_widget(self.play_button)
            self.play_button.bind(on_press=self.play_pause)

            self.next_button = MDIconButton(
                icon='skip-next', pos_hint={'center_x': 0.55, 'center_y': 0.1})
            self.add_widget(self.next_button)
            self.next_button.bind(on_press=self.next)

            self.prev_button = MDIconButton(
                icon='skip-previous', pos_hint={'center_x': 0.45, 'center_y': 0.1})
            self.add_widget(self.prev_button)
            self.prev_button.bind(on_press=self.previous)
            self.prev_button.disabled = True

            self.sound.bind(on_stop=self.on_stop)
            self.play_button.icon = (
                'play' if self.sound.state == 'stop' else 'pause')
            self.sound.play()
            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)
            self.finished = False
            self.paused = False
            if self.playlist_started == False:
                self.played_songs.append(self.song)

            Window.set_title(f"Chorduce - {self.song_title.text}")

            Thread(
                name='lyrics', target=self.get_lyrics, daemon=True).start()

        elif self.music_icon_clicked == True:
            self.play_button.icon = (
                'play' if self.sound.state == 'stop' else 'pause')
            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)

            self.music_icon_clicked = False

        elif self.song[1] != self.sn and self.counter > 0:
            Database.add_to_listening_history(
                song_id=self.song[0], username=self.manager.get_screen('main').account[0], author=self.song[2], language=self.song[5], genre=self.song[6])
            if self.playlist_started == False:
                self.played_songs.append(self.song)
                self.index = -1
            self.prev_button.disabled = False
            self.manager.get_screen('main').skip_prev.disabled = False
            self.screen_switched = False
            self.already_started = True
            self.sn = self.song[1]
            self.new = True
            self.sound.stop()
            self.bg_image.source = self.song[3]+'-bg.png'
            self.song_title.text = self.song[1]
            self.song_author.text = self.song[2]
            self.song_image.source = self.song[3]

            self.sound = SoundLoader.load(self.song[4])
            self.start_time.text = "00:00"
            self.end_time.text = self.convert_seconds_to_min(
                sec=self.sound.length)
            self.sound.play()
            self.sound.bind(on_stop=self.on_stop)
            self.play_button.icon = (
                'play' if self.sound.state == 'stop' else 'pause')
            self.play_button.bind(on_press=self.play_pause)
            self.paused = False
            self.finished = False
            self.playlist_started = False

            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)
            self.clicked = False
            self.manager.get_screen('main').lyrics.disabled = True
            Window.set_title(f"Chorduce - {self.song_title.text}")
            Thread(
                name='lyrics', target=self.get_lyrics, daemon=True).start()

        else:
            self.play_button.icon = (
                'play' if self.sound.state == 'stop' else 'pause')
            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)

    # Function to convert seconds to minute
    def convert_seconds_to_min(self, sec):
        val = str(datetime.timedelta(seconds=sec)).split(':')
        return f'{val[1]}:{val[2].split(".")[0]}'

    def play_pause(self, dt):  # Function to play/pause song
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

    def next(self, dt):  # Function to play next song
        self.prev_button.disabled = False
        self.manager.get_screen("main").skip_prev.disabled = False
        self.clicked = False
        self.new = True
        self.paused = False
        self.play_button.icon = 'play'
        self.slider.value = 0
        self.sound.stop()

    def previous(self, dt):  # Function to play previous song
        self.clicked = False
        self.prev = True
        self.new = True
        self.index -= 1
        if self.index == -(len(self.played_songs)):
            self.prev_button.disabled = True
        else:
            self.prev_button.disabled = False
        song = self.played_songs[self.index]

        self.paused = False
        self.play_button.icon = 'play'
        self.sound.stop()
        self.slider.value = 0
        Clock.unschedule(self.update_slider)
        Clock.unschedule(self.update_time)
        self.sn = song[1]

        self.bg_image.source = song[3]+'-bg.png'
        self.song_title.text = song[1]
        self.song_author.text = song[2]
        self.song_image.source = song[3]

        self.sound = SoundLoader.load(song[4])
        self.start_time.text = "00:00"
        self.end_time.text = self.convert_seconds_to_min(self.sound.length)
        self.sound.play()
        self.sound.bind(on_stop=self.on_stop)
        self.play_button.icon = 'pause'
        self.play_button.bind(on_press=self.play_pause)

        Clock.schedule_interval(self.update_slider, 1)
        Clock.schedule_interval(self.update_time, 1)
        self.prev = False
        self.manager.get_screen("main").sound = self.sound
        self.manager.get_screen("main").is_playing = self.paused
        self.manager.get_screen("main").song_name = self.song_title.text
        self.manager.get_screen("main").song_n.text = self.song_title.text
        self.manager.get_screen("main").song_author = self.song_author.text
        self.manager.get_screen("main").song_auth.text = self.song_author.text
        self.manager.get_screen("main").song_image = self.song_image.source
        self.manager.get_screen("main").img.source = self.song_image.source
        self.manager.get_screen(
            "main").end.text = self.convert_seconds_to_min(self.sound.length)
        MainScreen.on_pre_enter

        Window.set_title(f"Chorduce - {self.song_title.text}")

    def on_stop(self, dt):  # Function called when the song stops
        if self.manager.get_screen("main").bass == True:
            self.manager.get_screen(
                "main").switch.theme_icon_color = "Primary"

        if self.manager.get_screen("main").repeat.icon == 'repeat':
            self.manager.get_screen("main").repeat.icon = 'repeat-off'
            self.manager.get_screen("main").repeat.theme_icon_color = "Primary"

        if self.index != -1 and self.prev == False and self.paused == False and self.playlist == False and self.queue == False and self.playlist_started == False:
            Clock.unschedule(self.update_slider)
            Clock.unschedule(self.update_time)
            self.new = False
            self.index += 1
            song = self.played_songs[self.index]
            self.sn = song[1]
            Database.add_to_listening_history(
                song_id=song[0], username=self.manager.get_screen('main').account[0], author=song[2], language=song[5], genre=song[6])

            self.bg_image.source = song[3]+'-bg.png'
            self.song_title.text = song[1]
            self.song_author.text = song[2]
            self.song_image.source = song[3]

            self.sound = SoundLoader.load(song[4])
            self.start_time.text = "00:00"
            self.end_time.text = self.convert_seconds_to_min(self.sound.length)
            self.sound.play()
            self.sound.bind(on_stop=self.on_stop)
            self.play_button.icon = 'pause'
            self.play_button.bind(on_press=self.play_pause)

            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)
            self.manager.get_screen("main").sound = self.sound
            self.manager.get_screen("main").is_playing = self.paused
            self.manager.get_screen("main").song_name = self.song_title.text
            self.manager.get_screen("main").song_n.text = self.song_title.text
            self.manager.get_screen("main").song_author = self.song_author.text
            self.manager.get_screen(
                "main").song_auth.text = self.song_author.text
            self.manager.get_screen("main").song_image = self.song_image.source
            self.manager.get_screen("main").img.source = self.song_image.source
            self.manager.get_screen(
                "main").end.text = self.convert_seconds_to_min(self.sound.length)
            self.manager.get_screen('main').lyrics.disabled = True
            Thread(
                name='lyrics', target=self.get_lyrics, daemon=True).start()
            MainScreen.on_pre_enter

        elif self.paused == False and (self.slider.value > 98.5 or self.new == True) and self.prev == False and self.clicked == False:

            self.clicked = False
            self.paused = False
            self.play_button.icon = 'play'
            self.manager.get_screen('main').skip_prev.disabled = False
            self.prev_button.disabled = False
            Clock.unschedule(self.update_slider)
            Clock.unschedule(self.update_time)
            self.new = False

            if self.queue != False:
                if len(self.queue_songs) != 0:

                    if self.index != -1 and self.queue_counter == 0:
                        self.played_songs.insert(
                            self.index+1, self.queue_songs[0])
                    elif self.index == -1 and self.queue_counter == 0:
                        self.played_songs.append(self.queue_songs[0])

                    elif self.queue_counter > 0:
                        n = self.played_songs.index(self.reference)
                        self.played_songs.insert(n+1, self.queue_songs[0])

                    self.queue_counter += 1
                    self.sn = self.queue_songs[0][1]
                    Database.add_to_listening_history(
                        song_id=self.queue_songs[0][0], username=self.manager.get_screen('main').account[0], author=self.queue_songs[0][2], language=self.queue_songs[0][5], genre=self.queue_songs[0][6])

                    self.bg_image.source = self.queue_songs[0][3]+'-bg.png'
                    self.song_title.text = self.queue_songs[0][1]
                    self.song_author.text = self.queue_songs[0][2]
                    self.song_image.source = self.queue_songs[0][3]

                    self.sound = SoundLoader.load(self.queue_songs[0][4])
                    self.start_time.text = "00:00"
                    self.end_time.text = self.convert_seconds_to_min(
                        self.sound.length)
                    self.sound.play()
                    self.sound.bind(on_stop=self.on_stop)
                    self.play_button.icon = 'pause'
                    self.play_button.bind(on_press=self.play_pause)

                    Clock.schedule_interval(self.update_slider, 1)
                    Clock.schedule_interval(self.update_time, 1)
                    self.reference = self.queue_songs[0]
                    self.queue_songs.pop(0)
                    if len(self.queue_songs) == 0:
                        self.queue_songs = []
                        self.queue = False
                        self.queue_counter = 0
                        self.index = -(len(self.played_songs) -
                                       self.played_songs.index(self.reference)) + 1
                        if self.index == 0:
                            self.index = -1

            elif self.already_started != True:
                song = Database.music(
                    limit=1, lang=self.song[5], genre=self.song[6])
                Database.add_to_listening_history(
                    song_id=song[0][0], username=self.manager.get_screen('main').account[0], author=song[0][2], language=song[0][5], genre=song[0][6])
                self.played_songs.append(
                    Database.get_song_detail(name=song[0][1]))
                self.sn = song[0][1]

                self.bg_image.source = song[0][3]+'-bg.png'
                self.song_title.text = song[0][1]
                self.song_author.text = song[0][2]
                self.song_image.source = song[0][3]

                self.sound = SoundLoader.load(song[0][4])
                self.start_time.text = "00:00"
                self.end_time.text = self.convert_seconds_to_min(
                    self.sound.length)
                self.sound.play()
                self.sound.bind(on_stop=self.on_stop)
                self.play_button.icon = 'pause'
                self.play_button.bind(on_press=self.play_pause)

                Clock.schedule_interval(self.update_slider, 1)
                Clock.schedule_interval(self.update_time, 1)

            self.manager.get_screen("main").sound = self.sound
            self.manager.get_screen("main").is_playing = self.paused
            self.manager.get_screen("main").song_name = self.song_title.text
            self.manager.get_screen("main").song_n.text = self.song_title.text
            self.manager.get_screen("main").song_author = self.song_author.text
            self.manager.get_screen(
                "main").song_auth.text = self.song_author.text
            self.manager.get_screen("main").song_image = self.song_image.source
            self.manager.get_screen("main").img.source = self.song_image.source
            self.manager.get_screen(
                "main").end.text = self.convert_seconds_to_min(self.sound.length)
            self.manager.get_screen('main').lyrics.disabled = True
            Thread(
                name='lyrics', target=self.get_lyrics, daemon=True).start()
            MainScreen.on_pre_enter

            self.stop = True
        self.already_started = False

        '''with open("Settings/settings.json") as f:
            data = json.load(f)
            notifs = data['Notifications']
        if Window.focus == False and notifs == 'Enabled':
            notify(BodyText=self.song_author.text, TitleText=self.song_title.text,
                   AppName='Chorduce', ImagePath=self.song_image.source)'''
        Window.set_title(f'Chorduce - {self.song_title.text}')

        if self.manager.get_screen('main').sound != None:
            vol = {'volume-high': 1, 'volume-variant-off': 0,
                   'volume-low': 0.15, 'volume-medium': 0.5}
            self.m_icon = self.manager.get_screen(
                'main').mute.icon
            self.manager.get_screen('main').sound.volume = vol[self.m_icon]

    def update_slider(self, dt):  # Function to update slider position w.r.t song
        self.slider.value = (self.sound.get_pos() / self.sound.length) * 100

    def update_time(self, dt):  # Function to Update time w.r.t to song
        total_seconds = int(self.sound.get_pos())
        current_minute = total_seconds // 60
        current_seconds = total_seconds - (current_minute * 60)
        current_time = f"{current_minute:02}:{current_seconds:02}"
        self.start_time.text = current_time

    def touch_down(self, *args):  # Function to seek song based on slider position
        if self.sound:
            self.sound.seek((self.slider.value/100)*self.sound.length)

    def get_lyrics(self):  # Function to get lyrics of current song ( if available )
        if self.sound:
            genius = lyricsgenius.Genius('',
                                         skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"],
                                         remove_section_headers=True)

            try:
                API = azapi.AZlyrics('google', accuracy=0.8)

                API.artist = self.song_author.text
                API.title = self.song_title.text

                API.getLyrics(save=False)

                lyrics = API.lyrics
                if lyrics != '':
                    self.not_found = False
                else:
                    error = 1/0
            except:
                try:
                    extract_lyrics = SongLyrics(
                        '', '')

                    data = extract_lyrics.get_lyrics(
                        f"{self.song_title.text} By {self.song_author.text} Lyrics")
                    lyrics = data['lyrics']
                    self.not_found = False
                except:
                    try:
                        song = genius.search_song(
                            self.song_title.text, self.song_author.text)
                        genius.response_format = 'markdown'
                        lyrics = song.lyrics
                        self.not_found = False
                    except:
                        self.not_found = True

            if self.not_found != True:
                self.manager.get_screen('main').lyrics.disabled = False
                self.manager.get_screen('lyrics').label.text = lyrics
                Clock.schedule_once(self.set_lyrics_height)
            else:
                self.manager.get_screen(
                    'lyrics').label.text = "We Do Not Have The Lyrics For This Song!"
                Clock.schedule_once(self.set_lyrics_height)
                self.manager.get_screen('main').lyrics.disabled = True

    # Function to set the height of label widget in lyrics screen
    def set_lyrics_height(self, dt):
        self.manager.get_screen('lyrics').label.height = self.manager.get_screen(
            'lyrics').label.texture_size[1]

    def go_back(self, dt):  # Function to go back to the previous screen
        self.manager.get_screen("main").sound = self.sound
        self.manager.get_screen("main").paused = self.paused
        self.manager.get_screen("main").song_name = self.song_title.text
        self.manager.get_screen("main").song_author = self.song_author.text
        self.manager.get_screen("main").song_image = self.song_image.source
        self.manager.current = self.prev_screen
        self.manager.transition.direction = 'right'


class BassBoost():  # Initializing bassboost class
    global attenuate_db
    global accentuate_db
    attenuate_db = -10
    accentuate_db = 10

    def bass_line_freq(track):  # Function to find the bass factor
        sample_track = list(track)

        est_mean = np.mean(sample_track)

        est_std = 3 * np.std(sample_track) / (math.sqrt(2))

        bass_factor = int(round((est_std - est_mean) * 0.005))

        return bass_factor

    def audio(path):  # Function to apply bass to the song
        sample = AudioSegment.from_mp3(path)
        filtered = sample.low_pass_filter(
            BassBoost.bass_line_freq(sample.get_array_of_samples()))

        combined = (sample - attenuate_db).overlay(filtered + accentuate_db)
        combined.export("D:\\Music Player App\\" +
                        path[20:].replace(".mp3", "") + "-boosted.mp3", format="mp3")


class SearchScreen(MDScreen):  # Initialising the SearchScreen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.song_id = None

        self.new_songs = Clock.create_trigger(self.new)

        self.back = MDIconButton(
            icon='chevron-left', pos_hint={'top': 1, 'left': 0.7})

        self.search_bar = MDTextField(mode='fill', hint_text='Search', icon_left='magnify',
                                      pos_hint={'top': 0.92, 'center_x': 0.53}, size_hint=(0.9, 0.2),
                                      background_color="yellow", fill_color_focus="white", fill_color_normal="grey",
                                      hint_text_color_normal="white", icon_left_color_normal="white", text_validate_unfocus=False)
        self.add_widget(self.search_bar)
        self.search_bar.bind(text=self.updating)

        self.scroll = MDScrollView(pos_hint={'top': 0.87, 'center_x': 0.58}, do_scroll_x=False, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=20,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)

        self.list = MDList(size_hint_x=0.9)
        self.scroll.add_widget(self.list)

        self.top_bar = MDTopAppBar(left_action_items=[['chevron-left', lambda x: self.go_back()],],
                                   title="Music Player",
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0
                                   )
        self.add_widget(self.top_bar)

        self.nav_drawer = MDNavigationDrawer(
            enable_swiping=True, spacing=dp(25))
        self.nav_menu = MDNavigationDrawerMenu(spacing=dp(35))

        self.nav_account = MDNavigationDrawerItem(
            text='Account', icon="account", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_profile)
        self.nav_menu.add_widget(self.nav_account)

        self.nav_playlist = MDNavigationDrawerItem(
            text='Playlist', icon="playlist-music", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)
        self.nav_playlist.bind(on_release=self.to_playlist)

        self.nav_divider = MDNavigationDrawerDivider()
        self.nav_menu.add_widget(self.nav_divider)

        self.chatbot = MDNavigationDrawerItem(
            text='Euphonious', icon="robot", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.chatbot)
        self.chatbot.bind(on_release=self.to_chat)

        self.nav_settings = MDNavigationDrawerItem(
            text='Settings', icon="tools", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_settings)
        self.nav_menu.add_widget(self.nav_settings)

        self.nav_logout = MDNavigationDrawerItem(
            text='Logout', icon="logout", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_logout.bind(on_release=self.logout)
        self.nav_menu.add_widget(self.nav_logout)

        self.nav_layout = MDNavigationLayout()
        self.nav_drawer.add_widget(self.nav_menu)
        self.nav_layout.add_widget(self.nav_drawer)

        self.add_widget(
            MDNavigationRail(
                MDNavigationRailMenuButton(
                    icon='menu',
                    on_press=lambda x: self.nav_drawer.set_state('open')
                ),
                MDNavigationRailItem(
                    text="HOME",
                    icon="home",
                    on_press=self.to_main,
                ),
                MDNavigationRailItem(
                    text="MUSIC",
                    icon="music",
                    on_press=self.to_player,
                ),
                MDNavigationRailItem(
                    text="ASSISTANT",
                    icon="robot-happy-outline",
                    on_press=lambda x: Thread(
                        target=self.manager.get_screen('main').mic_ask, daemon=True).start()
                ),
                md_bg_color=(1, 0, 0, 0),
                pos_hint={'top': 0.97, 'center_x': 0.02},
                size_hint=(0.105, 5),
                padding=[0, 25, 0, 70],
                spacing="390dp"
            )
        )
        self.add_widget(self.nav_layout)

    def to_main(self, dt):  # Function to go to main screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'

    def to_player(self, instance):  # Function to go to musicplayer
        try:
            self.manager.get_screen('musicplayer').music_icon_clicked = True
            self.manager.get_screen('musicplayer').prev_screen = 'search'
            self.manager.current = 'musicplayer'
            self.manager.transition.direction = 'left'
        except:
            pass

    def to_profile(self, dt):  # Function to go to user account screen
        self.manager.current = 'profile'
        self.manager.transition.direction = 'left'

    def to_settings(self, dt):  # Function to go to settings screen
        self.manager.current = 'settings'
        self.manager.transition.direction = 'left'

    def logout(self, dt):  # Function to logout
        pass

    def to_playlist(self, dt):  # Function to change to playlist screen
        self.manager.current = 'playlist'
        self.manager.transition.direction = 'left'

    def to_chat(self, dt):  # Function to change to chat screen
        self.manager.current = 'chat'
        self.manager.transition.direction = 'left'

    def on_pre_enter(self):  # Function called just before entering the screen
        self.account = Database.acc_details()[0]
        self.plays = Database.playlists_info(username=self.account)
        self.songs = Database.music(limit=15)
        for i in self.songs:
            self.sugg_songs = TwoLineAvatarIconListItem(IconRightWidget(
                id=f"{i[0]},{i[1]}", icon='dots-vertical', on_press=self.dropdown), ImageLeftWidget(source=i[3]), text=i[1], secondary_text=i[2])
            self.list.add_widget(self.sugg_songs)
            self.sugg_songs.bind(on_release=self.musicplayer)

    def updating(self, instance, value):  # Function called when the text in search bar is changed
        self.search_text = self.search_bar.text
        Thread(target=self.update_list(), name='search', daemon=True).start()

    # Function to find the matching song and to update the filtered_items list
    def update_list(self):

        if self.search_text != '':
            text = self.search_text

            self.filtered_items = Database.song_match(text)
            self.new_songs()
        else:
            self.filtered_items = []
            self.new_songs()

    def new(self, dt):  # Function to update the widgets based on search result
        try:
            if len(self.filtered_items) > 0:
                self.list.clear_widgets()
                for it in self.filtered_items:
                    self.sugg_songs = TwoLineAvatarIconListItem(IconRightWidget(
                        id=f"{it[0]},{it[1]}", icon='dots-vertical', on_press=self.dropdown), ImageLeftWidget(source=it[3]), text=it[1], secondary_text=it[2])
                    self.list.add_widget(self.sugg_songs)
                    self.sugg_songs.bind(on_release=self.musicplayer)
            else:
                self.list.clear_widgets()
        except:
            pass

    def go_back(self):  # Function to return to previous screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'

    def musicplayer(self, instance):  # Function to change to musicplayer
        self.song_name = instance.text
        self.manager.get_screen("musicplayer").song_name = self.song_name
        self.manager.get_screen('musicplayer').playlist = False
        self.manager.get_screen('musicplayer').playlist_songs = None
        self.manager.get_screen('musicplayer').prev_screen = 'search'
        self.manager.get_screen("musicplayer").clicked = False
        self.manager.get_screen('musicplayer').new = True

        if self.manager.get_screen("musicplayer").sound and self.manager.get_screen("musicplayer").sn != self.song_name:
            self.manager.get_screen("musicplayer").sound.stop()

        self.manager.current = 'musicplayer'
        self.manager.transition.direction = 'left'

    # Function which shows a dropdown menu of options ('Add to queue', 'Add to playlist')
    def dropdown(self, instance):
        detail = instance.id.split(',')
        self.name_of_song = detail[1]
        self.song_id = int(detail[0])
        self.menu_items = [
            {
                'text': 'Add to Queue',
                'viewclass': 'OneLineListItem',
                'on_release':  self.queue
            },
            {
                'text': 'Add to Playlist',
                'viewclass': 'OneLineListItem',
                'on_release':  self.playlists
            }
        ]
        self.menu = MDDropdownMenu(
            caller=instance,
            items=self.menu_items,
            width_mult=4)
        self.menu.open()

    def playlists(self):  # Function to open a dialog box containing a list of playlists of the user
        self.box = MDBoxLayout(
            size_hint_y=None, orientation='vertical', adaptive_height=True)
        for k in self.plays:
            self.play_name = OneLineListItem(id=str(k[0]), text=k[1])
            self.play_name.bind(on_press=self.select_playlist)
            self.box.add_widget(self.play_name)

        self.dialog = MDDialog(
            title="Select Playlist",
            type="custom",
            auto_dismiss=True,
            content_cls=self.box
        )
        self.dialog.open()

    def queue(self):  # Function to add song to the queue
        self.song_info = Database.get_song_detail(id=int(self.song_id))
        self.manager.get_screen('musicplayer').queue = True
        self.manager.get_screen(
            'musicplayer').queue_songs.append(self.song_info)
        toast(text="Song Added To Queue")

    def select_playlist(self, instance):  # Function to add song to the playlist
        Database.add_playlist_song(playlist_id=int(
            instance.id), song_id=int(self.song_id), song_name=self.name_of_song)
        self.dialog.dismiss()
        toast(text="Song Added To Playlist")


class Playlist(MDScreen):  # Initialising the Playlist screen
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.prev_len = 0
        self.deleted = False

        self.head = MDLabel(text="Playlists", pos_hint={
                            'top': 0.95, 'right': 0.56}, bold=True, font_style="H3", size_hint=(0.5, 0.1))
        self.add_widget(self.head)

        self.scroll = MDScrollView(size_hint=(0.9, 0.87), pos_hint={'top': 0.87, 'right': 0.97}, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)

        self.sub_layout = MDStackLayout(
            spacing="30dp", adaptive_height=True, width=dp(1000), padding="20dp")
        self.scroll.add_widget(self.sub_layout)

        self.create_play = MDFloatingActionButton(
            icon='plus', pos_hint={'top': 0.1, 'right': 0.95}, elevation=5, icon_size="35dp")
        self.add_widget(self.create_play)
        self.create_play.bind(on_release=self.play_details)

        self.top_bar = MDTopAppBar(left_action_items=[['chevron-left', lambda x: self.go_to_main()]],
                                   title="Music Player",
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0
                                   )
        self.add_widget(self.top_bar)

        self.nav_drawer = MDNavigationDrawer(
            enable_swiping=True, spacing=dp(25))
        self.nav_menu = MDNavigationDrawerMenu(spacing=dp(35))

        self.nav_account = MDNavigationDrawerItem(
            text='Account', icon="account", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_profile)
        self.nav_menu.add_widget(self.nav_account)

        self.nav_playlist = MDNavigationDrawerItem(
            text='Playlist', icon="playlist-music", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)
        self.nav_playlist.bind(on_release=self.to_playlist)

        self.nav_divider = MDNavigationDrawerDivider()
        self.nav_menu.add_widget(self.nav_divider)

        self.chatbot = MDNavigationDrawerItem(
            text='Euphonious', icon="robot", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.chatbot)
        self.chatbot.bind(on_release=self.to_chat)

        self.nav_settings = MDNavigationDrawerItem(
            text='Settings', icon="tools", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_settings)
        self.nav_menu.add_widget(self.nav_settings)

        self.nav_logout = MDNavigationDrawerItem(
            text='Logout', icon="logout", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_logout.bind(on_release=self.logout)
        self.nav_menu.add_widget(self.nav_logout)

        self.nav_layout = MDNavigationLayout()
        self.nav_drawer.add_widget(self.nav_menu)
        self.nav_layout.add_widget(self.nav_drawer)

        self.add_widget(
            MDNavigationRail(
                MDNavigationRailMenuButton(
                    icon='menu',
                    on_press=lambda x: self.nav_drawer.set_state('open')
                ),
                MDNavigationRailItem(
                    text="HOME",
                    icon="home",
                    on_press=self.to_main,
                ),
                MDNavigationRailItem(
                    text="MUSIC",
                    icon="music",
                    on_press=self.to_player,
                ),
                MDNavigationRailItem(
                    text="ASSISTANT",
                    icon="robot-happy-outline",
                    on_press=lambda x: Thread(
                        target=self.manager.get_screen('main').mic_ask, daemon=True).start()
                ),
                md_bg_color=(1, 0, 0, 0),
                pos_hint={'top': 0.97, 'center_x': 0.02},
                size_hint=(0.105, 5),
                padding=[0, 25, 0, 70],
                spacing="390dp"
            )
        )
        self.add_widget(self.nav_layout)

    def to_main(self, dt):  # Function to change to main screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'

    def to_player(self, instance):  # Function to change to musicplayer
        try:
            self.manager.get_screen('musicplayer').music_icon_clicked = True
            self.manager.get_screen('musicplayer').prev_screen = 'playlist'
            self.manager.current = 'musicplayer'
            self.manager.transition.direction = 'left'
        except:
            pass

    def to_profile(self, dt):  # Function to change to user account screen
        self.manager.current = 'profile'
        self.manager.transition.direction = 'left'

    def to_settings(self, dt):  # Function to change to settings screen
        self.manager.current = 'settings'
        self.manager.transition.direction = 'left'

    def logout(self, dt):  # Function to logout
        pass

    def to_playlist(self, dt):  # Function to change to playlist screen
        self.manager.current = 'playlist'
        self.manager.transition.direction = 'left'

    def to_chat(self, dt):  # Function to change to chat screen
        self.manager.current = 'chat'
        self.manager.transition.direction = 'left'

    def go_to_main(self):  # Function to change to main screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'

    # Function to extract colour from the image of playlist
    def colour_extractor(self, path):
        try:
            color_thief = ColorThief(path)
            palette = color_thief.get_palette(color_count=2)
            l = []

            for i in palette:
                l.append('#%02x%02x%02x' % i)

        except:
            l = ["#000000", "#00007c"]

        return l

    # Function to show dialog box and fetch the name and image of playlist
    def play_details(self, dt):
        self.main = MDBoxLayout(orientation="horizontal",
                                spacing="12dp",
                                size_hint_y=None,
                                height="200dp")
        self.upload = Button(background_normal='images/upload.png', on_press=self.choose,
                             size_hint_x=0.7, background_down='images/loading.png')
        self.main.add_widget(self.upload)

        self.play_n = MDTextField(
            hint_text="Playlist Name",
            pos_hint={'center_y': 0.5},
            max_text_length=30,
            helper_text_mode='on_error'
        )

        self.main.add_widget(self.play_n)
        self.dialog = MDDialog(
            title="Create Playlist",
            type="custom",
            auto_dismiss=False,
            content_cls=self.main,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.cancel
                ),
                MDFlatButton(
                    text="CREATE",
                    on_release=self.create
                ),
            ],
        )

        self.dialog.open()

    def choose(self, dt):  # Function to choose image
        self.play_img = filechooser.open_file()
        try:
            self.upload.background_normal = self.play_img[0]
        except:
            toast(text="Unable to load image")

    def cancel(self, dt):  # Function to dismiss the dialog box
        self.dialog.dismiss()

    def create(self, dt):  # Function to create a new playlist
        if self.play_n.text != '' and self.upload.state == 'normal' and len(self.play_n.text) <= 30:
            today = date.today()
            t = today.strftime("%d/%m/%Y")
            colours = self.colour_extractor(path=self.upload.background_normal)
            Database.create_playlist(
                name=self.play_n.text, image=(
                    self.upload.background_normal if self.upload.background_normal != 'images/upload.png' else 'images/no img.png'),
                user=self.username, date=t,  colours=str(colours)
            )

            self.playlists = Database.playlists_info(username=self.username)

            self.card_new = MDCard(id=str(self.playlists[-1][0]), orientation='vertical', md_bg_color=(
                1, 1, 1, 1), height="350dp", width="300dp", size_hint=(None, None), spacing="10dp", padding="20dp")
            self.sub_layout.add_widget(self.card_new)
            self.card_new.bind(on_press=self.playlist_songs)

            self.img_new = Image(source=self.playlists[-1][2],
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint_y=1, keep_ratio=False, allow_stretch=True)
            self.card_new.add_widget(self.img_new)

            self.play_name_new = MDLabel(
                text=self.playlists[-1][1], bold=True, font_style='H5', size_hint_y=0.2)
            self.card_new.add_widget(self.play_name_new)

            self.play_date_new = MDLabel(
                text=self.playlists[-1][4], font_style="Subtitle2", size_hint_y=0.1)
            self.card_new.add_widget(self.play_date_new)
            self.dialog.dismiss()
            toast(text="Playlist Created")

    def on_pre_enter(self):  # Function called just before entering the screen
        self.account = Database.acc_details()
        self.username = self.account[0]
        self.playlists = Database.playlists_info(username=self.username)
        self.prev_len = len(self.playlists)

        if self.counter == 0 or self.deleted == True:
            self.counter += 1
            if self.deleted:
                self.sub_layout.clear_widgets()

            for i in range(len(self.playlists)):
                self.card = MDCard(id=str(self.playlists[i][0]), orientation='vertical', md_bg_color=(
                    1, 1, 1, 1), height="350dp", width="300dp", size_hint=(None, None), spacing="10dp", padding="20dp")
                self.sub_layout.add_widget(self.card)
                self.card.bind(on_press=self.playlist_songs)

                self.img = Image(source=self.playlists[i][2], pos_hint={
                                 'center_x': 0.5, 'center_y': 0.5}, size_hint_y=1, keep_ratio=False, allow_stretch=True)
                self.card.add_widget(self.img)

                self.play_name = MDLabel(
                    text=self.playlists[i][1], bold=True, font_style='H5', size_hint_y=0.2)
                self.card.add_widget(self.play_name)

                self.play_date = MDLabel(
                    text=self.playlists[i][4], font_style="Subtitle2", size_hint_y=0.1)
                self.card.add_widget(self.play_date)

            self.deleted = False

        elif self.counter > 0 and self.prev_len < len(self.playlists):

            for y in range(self.prev_len, len(self.playlists)):
                self.new_card = MDCard(orientation='vertical', md_bg_color=(
                    1, 1, 1, 1), height="350dp", width="300dp", size_hint=(None, None), spacing="10dp", padding="20dp")
                self.sub_layout.add_widget(self.new_card)

                self.new_img = Image(source=self.playlists[y][2], pos_hint={
                                     'center_x': 0.5, 'center_y': 0.5}, size_hint_y=1, keep_ratio=False, allow_stretch=True)
                self.new_card.add_widget(self.img_new)

                self.new_play_name = MDLabel(
                    text=self.playlists[y][1], bold=True, font_style='H5', size_hint_y=0.2)
                self.new_card.add_widget(self.play_name_new)

                self.new_play_date = MDLabel(
                    text=self.playlists[y][4], font_style="Subtitle2", size_hint_y=0.1)
                self.new_card.add_widget(self.play_date_new)
            self.prev_len = len(self.playlists)

        elif self.counter > 0:
            self.sub_layout.clear_widgets()

            for i in range(len(self.playlists)):
                self.card = MDCard(id=str(self.playlists[i][0]), orientation='vertical', md_bg_color=(
                    1, 1, 1, 1), height="350dp", width="300dp", size_hint=(None, None), spacing="10dp", padding="20dp")
                self.sub_layout.add_widget(self.card)
                self.card.bind(on_press=self.playlist_songs)

                self.img = Image(source=self.playlists[i][2], pos_hint={
                                 'center_x': 0.5, 'center_y': 0.5}, size_hint_y=1, keep_ratio=False, allow_stretch=True)
                self.card.add_widget(self.img)

                self.play_name = MDLabel(
                    text=self.playlists[i][1], bold=True, font_style='H5', size_hint_y=0.2)
                self.card.add_widget(self.play_name)

                self.play_date = MDLabel(
                    text=self.playlists[i][4], font_style="Subtitle2", size_hint_y=0.1)
                self.card.add_widget(self.play_date)

    def playlist_songs(self, instance):  # Function to change to playlist_songs screen
        try:
            self.manager.get_screen(
                "playlist_songs").playlist_id = int(instance.id)
            self.manager.get_screen(
                "playlist_songs").bg_img = instance.children[2].source
            self.manager.get_screen(
                "playlist_songs").play_name = instance.children[1].text
            self.manager.get_screen(
                "playlist_songs").play_date = instance.children[0].text
            self.manager.current = 'playlist_songs'
            self.manager.transition.direction = 'left'
        except:
            self.manager.get_screen(
                "playlist_songs").playlist_id = int(self.card_new.id)
            self.manager.get_screen(
                "playlist_songs").bg_img = self.img_new.source
            self.manager.get_screen(
                "playlist_songs").play_name = self.play_name_new.text
            self.manager.get_screen(
                "playlist_songs").play_date = self.play_date_new.text
            self.manager.current = 'playlist_songs'
            self.manager.transition.direction = 'left'


class Playlist_Songs(MDScreen):  # Initialising the Playlist Songs screen
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlist_id = None
        self.bg_img = None
        self.play_name = None
        self.play_date = None

    def on_pre_enter(self):  # Function called just before entering the screen
        self.clear_widgets()
        self.colours = Database.playlists_info(id=self.playlist_id)[5]
        self.hex = ast.literal_eval(self.colours)
        self.songs = Database.playlist_songs(
            id=self.playlist_id, order_by="created")

        self.song_infos = []
        for i in self.songs:
            self.song_info = Database.get_song_detail(id=i[1])
            self.song_infos.append(self.song_info)

        with self.canvas:
            Color(0.5, 0.5, 0.5,
                  mode='hex')
            self.bg_grad = Rectangle(texture=Gradient.vertical(get_color_from_hex(self.hex[1]), get_color_from_hex(self.hex[0])),
                                     pos=[0, -8], size=[1920, 1080])

        self.scroll = MDScrollView(pos_hint={'top': 0.93}, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)

        self.main = MDBoxLayout(orientation='vertical', spacing="1dp",
                                size_hint_y=None, adaptive_height=True, padding=[0, 0, 0, 100])
        self.scroll.add_widget(self.main)

        self.layout = MDBoxLayout(orientation='horizontal', pos_hint={
                                  'top': 0.95, 'center_x': 0.23}, size_hint_y=None, height="300dp", size_hint_x=0.4, spacing="2dp")
        self.main.add_widget(self.layout)
        self.layout_sub = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="100dp", size_hint_x=0.33, padding=[
                                      0, 0, 200, 0], pos_hint={'center_x': 0.23}, spacing="20dp")
        self.main.add_widget(self.layout_sub)

        self.bg = Image(source=self.bg_img, pos_hint={
                        'right': 0.7, 'center_y': 0.5}, size_hint_x=0.5)
        if self.bg.texture.size != (248, 248):
            image = Im.open(self.bg_img)
            new = image.resize((248, 248))
            new.save('-new.'.join(self.bg_img.rsplit('.', 1)))
            self.bg.source = '-new.'.join(self.bg_img.rsplit('.', 1))
        self.layout.add_widget(self.bg)

        self.sub_layout1 = MDBoxLayout(orientation='vertical', size_hint=(
            0.5, 0.2), pos_hint={'right': 0.6, 'center_y': 0.5}, spacing="50dp")
        self.layout.add_widget(self.sub_layout1)

        self.song_name = MDLabel(
            text=self.play_name, font_style="H4", bold=True)
        self.sub_layout1.add_widget(self.song_name)

        self.song_author = MDLabel(text=self.play_date, font_style="Subtitle1")
        self.sub_layout1.add_widget(self.song_author)

        self.icon1 = MDIconButton(icon='delete', pos_hint={
                                  'top': 1}, icon_size="35dp", md_bg_color=[1, 0, 0, 0.5])
        self.icon1.bind(on_press=self.confirm_playlist_deletion)
        self.layout_sub.add_widget(self.icon1)
        self.icon2 = MDIconButton(icon='sort-alphabetical-ascending', pos_hint={
                                  'top': 1}, icon_size="35dp", md_bg_color=[0, 1, 1, 0.5])
        self.icon2.bind(on_press=self.sort_on_name)
        self.layout_sub.add_widget(self.icon2)
        self.icon3 = MDIconButton(icon='sort-calendar-ascending', pos_hint={
                                  'top': 1}, icon_size="35dp", md_bg_color=[0, 1, 1, 0.5])
        self.icon3.bind(on_press=self.sort_on_date)
        self.layout_sub.add_widget(self.icon3)
        self.icon4 = MDIconButton(icon='playlist-edit', pos_hint={
                                  'top': 1}, icon_size="35dp", md_bg_color=[0, 1, 1, 0.5])
        self.icon4.bind(on_press=self.confirm_playlist_rename)
        self.layout_sub.add_widget(self.icon4)

        self.icon5 = MDIconButton(icon='image-edit', pos_hint={
                                  'top': 1}, icon_size="35dp", md_bg_color=[0, 1, 1, 0.5])
        self.icon5.bind(on_press=self.confirm_playlist_image)
        self.layout_sub.add_widget(self.icon5)

        self.layout2 = MDBoxLayout(orientation='vertical', spacing="20dp",
                                   padding="20dp", size_hint_y=None, adaptive_height=True)
        self.main.add_widget(self.layout2)

        self.number = MDLabel(text='')

        for i in range(len(self.song_infos)):
            self.card = MDCard(size_hint_y=None, orientation='horizontal', padding=[
                               50, 10, 50, 10], height="150dp", radius=20, size_hint_x=0.85, pos_hint={'center_x': 0.52})
            self.card.bind(on_release=self.musicplayer)
            self.layout2.add_widget(self.card)
            self.card.add_widget(
                MDLabel(text=f"{i+1}", size_hint_x=0.1, font_style="H5"))
            self.card.add_widget(Image(source=self.song_infos[i][3]))
            self.card.add_widget(
                MDLabel(text=self.song_infos[i][1], font_style='H5'))
            self.card.add_widget(
                MDLabel(text=self.song_infos[i][2], font_style="H5"))
            self.card.add_widget(MDLabel(text='', size_hint_x=0.4))
            self.card.add_widget(MDLabel(text=datetime.datetime.strptime(f"{self.songs[i][3]}", rf"%Y-%m-%d").strftime(rf"%d/%m/%Y"), pos_hint={
                                 'center_x': 0.5}, font_style="H5", size_hint_x=0.7))
            self.delete_song = MDIconButton(id=f"{self.song_infos[i][0]}",
                                            icon='delete', pos_hint={'center_y': 0.5}, size_hint_x=0.2)
            self.delete_song.bind(on_press=self.confirm_playlist_song_deletion)
            self.card.add_widget(self.delete_song)

        self.top_bar = MDTopAppBar(left_action_items=[['chevron-left', lambda x: self.go_back()]],
                                   title="Music Player",
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0
                                   )
        self.add_widget(self.top_bar)

        self.nav_drawer = MDNavigationDrawer(
            enable_swiping=True, spacing=dp(25))
        self.nav_menu = MDNavigationDrawerMenu(spacing=dp(35))

        self.nav_account = MDNavigationDrawerItem(
            text='Account', icon="account", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_profile)
        self.nav_menu.add_widget(self.nav_account)

        self.nav_playlist = MDNavigationDrawerItem(
            text='Playlist', icon="playlist-music", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)
        self.nav_playlist.bind(on_release=self.to_playlist)

        self.nav_divider = MDNavigationDrawerDivider()
        self.nav_menu.add_widget(self.nav_divider)

        self.chatbot = MDNavigationDrawerItem(
            text='Euphonious', icon="robot", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.chatbot)
        self.chatbot.bind(on_release=self.to_chat)

        self.nav_settings = MDNavigationDrawerItem(
            text='Settings', icon="tools", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_settings)
        self.nav_menu.add_widget(self.nav_settings)

        self.nav_logout = MDNavigationDrawerItem(
            text='Logout', icon="logout", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_logout.bind(on_release=self.logout)
        self.nav_menu.add_widget(self.nav_logout)

        self.nav_layout = MDNavigationLayout()
        self.nav_drawer.add_widget(self.nav_menu)
        self.nav_layout.add_widget(self.nav_drawer)

        self.add_widget(
            MDNavigationRail(
                MDNavigationRailMenuButton(
                    icon='menu',
                    on_press=lambda x: self.nav_drawer.set_state('open')
                ),
                MDNavigationRailItem(
                    text="HOME",
                    icon="home",
                    on_press=lambda x: self.to_main,
                ),
                MDNavigationRailItem(
                    text="MUSIC",
                    icon="music",
                    on_press=self.to_player,
                ),
                MDNavigationRailItem(
                    text="ASSISTANT",
                    icon="robot-happy-outline",
                    on_press=lambda x: Thread(
                        target=self.manager.get_screen('main').mic_ask, daemon=True).start()
                ),
                md_bg_color=(1, 0, 0, 0),
                pos_hint={'top': 0.97, 'center_x': 0.02},
                size_hint=(0.105, 5),
                padding=[0, 25, 0, 70],
                spacing="390dp"
            )
        )
        self.add_widget(self.nav_layout)

    def to_main(self, dt):  # Function to change to the main screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'

    def to_player(self, instance):  # Function to change to the musicplayer
        try:
            self.manager.get_screen('musicplayer').music_icon_clicked = True
            self.manager.get_screen(
                'musicplayer').prev_screen = 'playlist_songs'
            self.manager.current = 'musicplayer'
            self.manager.transition.direction = 'left'
        except:
            pass

    def to_profile(self, dt):  # Function to change to the user account screen
        self.manager.current = 'profile'
        self.manager.transition.direction = 'left'

    def to_settings(self, dt):  # Function to change to the settings screen
        self.manager.current = 'settings'
        self.manager.transition.direction = 'left'

    def logout(self, dt):  # Function to logout
        pass

    def to_playlist(self, dt):  # Function to change to playlist screen
        self.manager.current = 'playlist'
        self.manager.transition.direction = 'left'

    def to_chat(self, dt):  # Function to change to chat screen
        self.manager.current = 'chat'
        self.manager.transition.direction = 'left'

    def musicplayer(self, instance):  # Function to change to musicplayer
        self.index = int(instance.children[6].text)
        self.manager.get_screen('musicplayer').playlist = False
        self.new_index = self.manager.get_screen('musicplayer').index
        try:
            if self.new_index != -1:
                for i in self.song_infos:
                    self.manager.get_screen(
                        'musicplayer').played_songs.insert(self.new_index+1, i)
            else:
                for i in self.song_infos:
                    self.manager.get_screen(
                        'musicplayer').played_songs.append(i)
            self.new_index = 0
            try:
                self.manager.get_screen('musicplayer').index = -(self.manager.get_screen(
                    'musicplayer').played_songs.index(self.song_infos[self.index]))
            except:
                self.manager.get_screen('musicplayer').index = -(self.manager.get_screen(
                    'musicplayer').played_songs.index(self.song_infos[-1]))
            self.manager.get_screen('musicplayer').playlist_started = True
        except:
            self.manager.get_screen('musicplayer').playlist_songs = None
        self.manager.get_screen('musicplayer').new = True
        self.manager.get_screen('musicplayer').prev_screen = 'playlist_songs'
        self.manager.get_screen(
            "musicplayer").song_name = instance.children[4].text
        self.manager.get_screen("musicplayer").clicked = False
        if self.manager.get_screen("musicplayer").sound and self.manager.get_screen("musicplayer").sn != self.song_name:
            self.manager.get_screen("musicplayer").sound.stop()
        self.manager.current = 'musicplayer'
        self.manager.transition.direction = 'left'

    def colour_extractor(self, path):
        try:
            color_thief = ColorThief(path)
            palette = color_thief.get_palette(color_count=2)
            l = []

            for i in palette:
                l.append('#%02x%02x%02x' % i)

        except:
            l = ["#000000", "#00007c"]

        return l

    # Function to show dialog box to confirm playlist deletion
    def confirm_playlist_deletion(self, dt):
        self.main = MDBoxLayout(orientation="vertical",
                                spacing="5dp",
                                size_hint_y=None,
                                size_hint_x=None,
                                width="300dp",
                                height="50dp")
        self.confirm = MDLabel(text="Are You Sure?",
                               size_hint_x=2, bold=True, font_style="H5")
        self.main.add_widget(self.confirm)

        self.note = MDLabel(text="Note: This will delete the whole playlist")
        self.main.add_widget(self.note)

        self.dialog = MDDialog(
            type="custom",
            auto_dismiss=False,
            content_cls=self.main,
            buttons=[
                MDFlatButton(
                    text="Yes",
                    md_bg_color=[0, 1, 0, 0.5],
                    on_release=self.delete_playlist
                ),
                MDFlatButton(
                    text="Not Now",
                    md_bg_color=[1, 0, 0, 0.5],
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )

        self.dialog.open()

    # Function to show dialoh box for playlist song deletion
    def confirm_playlist_song_deletion(self, instance):
        self.main = MDBoxLayout(orientation="vertical",
                                spacing="5dp",
                                size_hint_y=None,
                                size_hint_x=None,
                                width="300dp",
                                height="50dp")
        self.confirm = MDLabel(text="Are You Sure?",
                               size_hint_x=2, bold=True, font_style="H5")
        self.main.add_widget(self.confirm)

        self.dialog = MDDialog(
            type="custom",
            auto_dismiss=False,
            content_cls=self.main,
            buttons=[
                MDFlatButton(
                    id=instance.id,
                    text="Yes",
                    md_bg_color=[0, 1, 0, 0.5],
                    on_release=self.song_delete
                ),
                MDFlatButton(
                    text="Not Now",
                    md_bg_color=[1, 0, 0, 0.5],
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )

        self.dialog.open()

    def delete_playlist(self, dt):  # Function to delete playlist
        Database.delete_playlist(self.playlist_id)
        self.dialog.dismiss()
        self.manager.get_screen('playlist').deleted = True
        self.manager.current = 'playlist'
        toast(text="Playlist Deleted")

    def song_delete(self, instance):  # Function to delete playlist song
        Database.delete_playlist_song(self.playlist_id, int(instance.id))
        self.layout2.clear_widgets()
        self.songs = Database.playlist_songs(id=self.playlist_id)

        self.song_infos = []
        for i in self.songs:
            self.song_info = Database.get_song_detail(id=i[1])
            self.song_infos.append(self.song_info)

        self.number = MDLabel(text='')

        for i in range(len(self.song_infos)):
            self.card = MDCard(size_hint_y=None, orientation='horizontal', padding=[
                               50, 10, 50, 10], height="150dp", radius=20, size_hint_x=0.85, pos_hint={'center_x': 0.5})
            self.card.bind(on_release=self.musicplayer)
            self.layout2.add_widget(self.card)
            self.number.text = f"{i}"
            self.card.add_widget(
                MDLabel(text=f"{i+1}", size_hint_x=0.1, font_style="H5"))
            self.card.add_widget(Image(source=self.song_infos[i][3]))
            self.card.add_widget(
                MDLabel(text=self.song_infos[i][1], font_style='H5'))
            self.card.add_widget(
                MDLabel(text=self.song_infos[i][2], font_style="H5"))
            self.card.add_widget(MDLabel(text='', size_hint_x=0.4))
            self.card.add_widget(MDLabel(text=datetime.datetime.strptime(f"{self.songs[i][3]}", rf"%Y-%m-%d").strftime(rf"%d/%m/%Y"), pos_hint={
                                 'center_x': 0.5}, font_style="H5", size_hint_x=0.7))
            self.delete_song = MDIconButton(id=f"{self.song_infos[i][0]}",
                                            icon='delete', pos_hint={'center_y': 0.5}, size_hint_x=0.2)
            self.delete_song.bind(on_press=self.song_delete)
            self.card.add_widget(self.delete_song)

        self.dialog.dismiss()

    def sort_on_name(self, dt):  # Function to sort playlist songs in order of their name
        self.layout2.clear_widgets()
        if self.icon2.icon == 'sort-alphabetical-ascending':
            sort = 'song_name DESC'
            self.icon2.icon = 'sort-alphabetical-descending'
        else:
            sort = 'song_name ASC'
            self.icon2.icon = 'sort-alphabetical-ascending'
        self.songs = Database.playlist_songs(
            id=self.playlist_id, order_by=sort)

        self.song_infos = []
        for i in self.songs:
            self.song_info = Database.get_song_detail(id=i[1])
            self.song_infos.append(self.song_info)

        self.number = MDLabel(text='')

        for i in range(len(self.song_infos)):
            self.card = MDCard(size_hint_y=None, orientation='horizontal', padding=[
                               50, 10, 50, 10], height="150dp", radius=20, size_hint_x=0.85, pos_hint={'center_x': 0.5})
            self.card.bind(on_release=self.musicplayer)
            self.layout2.add_widget(self.card)
            self.number.text = f"{i}"
            self.card.add_widget(
                MDLabel(text=f"{i+1}", size_hint_x=0.1, font_style="H5"))
            self.card.add_widget(Image(source=self.song_infos[i][3]))
            self.card.add_widget(
                MDLabel(text=self.song_infos[i][1], font_style='H5'))
            self.card.add_widget(
                MDLabel(text=self.song_infos[i][2], font_style="H5"))
            self.card.add_widget(MDLabel(text='', size_hint_x=0.4))
            self.card.add_widget(MDLabel(text=datetime.datetime.strptime(f"{self.songs[i][3]}", rf"%Y-%m-%d").strftime(rf"%d/%m/%Y"), pos_hint={
                                 'center_x': 0.5}, font_style="H5", size_hint_x=0.7))
            self.delete_song = MDIconButton(id=f"{self.song_infos[i][0]}",
                                            icon='delete', pos_hint={'center_y': 0.5}, size_hint_x=0.2)
            self.delete_song.bind(on_press=self.song_delete)
            self.card.add_widget(self.delete_song)

    # Function to sort playlist songs in order of their date of creation
    def sort_on_date(self, dt):
        self.layout2.clear_widgets()
        if self.icon3.icon == 'sort-calendar-ascending':
            sort = 'created DESC'
            self.icon3.icon = 'sort-calendar-descending'
        else:
            sort = 'created ASC'
            self.icon3.icon = 'sort-calendar-ascending'
        self.songs = Database.playlist_songs(
            id=self.playlist_id, order_by=sort)

        self.song_infos = []
        for i in self.songs:
            self.song_info = Database.get_song_detail(id=i[1])
            self.song_infos.append(self.song_info)

        self.number = MDLabel(text='')

        for i in range(len(self.song_infos)):
            self.card = MDCard(size_hint_y=None, orientation='horizontal', padding=[
                               50, 10, 50, 10], height="150dp", radius=20, size_hint_x=0.85, pos_hint={'center_x': 0.5})
            self.card.bind(on_release=self.musicplayer)
            self.layout2.add_widget(self.card)
            self.number.text = f"{i}"
            self.card.add_widget(
                MDLabel(text=f"{i+1}", size_hint_x=0.1, font_style="H5"))
            self.card.add_widget(Image(source=self.song_infos[i][3]))
            self.card.add_widget(
                MDLabel(text=self.song_infos[i][1], font_style='H5'))
            self.card.add_widget(
                MDLabel(text=self.song_infos[i][2], font_style="H5"))
            self.card.add_widget(MDLabel(text='', size_hint_x=0.4))
            self.card.add_widget(MDLabel(text=datetime.datetime.strptime(f"{self.songs[i][3]}", rf"%Y-%m-%d").strftime(rf"%d/%m/%Y"), pos_hint={
                                 'center_x': 0.5}, font_style="H5", size_hint_x=0.7))
            self.delete_song = MDIconButton(id=f"{self.song_infos[i][0]}",
                                            icon='delete', pos_hint={'center_y': 0.5}, size_hint_x=0.2)
            self.delete_song.bind(on_press=self.song_delete)
            self.card.add_widget(self.delete_song)

    # Function to show dialog box for confirming playlist rename
    def confirm_playlist_rename(self, dt):
        self.rename_layout = MDTextField(
            hint_text="New Playlist Name",
            pos_hint={'center_y': 0.5, },
            max_text_length=30,
            helper_text_mode='on_error'
        )

        self.dialog = MDDialog(
            title="Rename Playlist",
            type="custom",
            auto_dismiss=False,
            content_cls=self.rename_layout,
            buttons=[
                MDFlatButton(
                    text="CONFRIM",
                    on_release=self.rename_playlist
                ),
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )

        self.dialog.open()

    def rename_playlist(self, dt):  # Function to rename playlist
        if self.rename_layout.text != '' and len(self.rename_layout.text) <= 30:
            Database.playlist_edit(
                playlist_id=self.playlist_id, rename=self.rename_layout.text)
            self.song_name.text = self.rename_layout.text
            self.play_name = self.rename_layout.text
            self.dialog.dismiss()

    # Function to show dialog box for confirming playlist image edit
    def confirm_playlist_image(self, dt):

        self.upload = Button(background_normal='images/upload.png',
                             on_press=self.choose, background_down='images/loading.png', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint_y=None, height="300dp")

        self.dialog = MDDialog(
            title="Create Playlist",
            type="custom",
            auto_dismiss=False,
            content_cls=self.upload,
            buttons=[
                MDFlatButton(
                    text="CONFIRM",
                    on_release=self.image_edit_playlist
                ),
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )

        self.dialog.open()

    def choose(self, dt):  # Function to choose image
        self.play_img = filechooser.open_file()
        try:
            self.upload.background_normal = self.play_img[0]
        except:
            toast(text="Unable to load image")

    def image_edit_playlist(self, dt):  # Function to edit image of the playlist
        if self.upload.background_normal != 'images/upload.png':

            Database.playlist_edit(
                playlist_id=self.playlist_id, image=self.upload.background_normal)
            self.bg.source = self.upload.background_normal
            self.bg_img = self.upload.background_normal
            self.hex = self.colour_extractor(self.bg_img)
            if self.bg.texture.size != (248, 248):
                image = Im.open(self.bg_img)
                new = image.resize((248, 248))
                new.save('-new.'.join(self.bg_img.rsplit('.', 1)))
                self.bg.source = '-new.'.join(self.bg_img.rsplit('.', 1))

            self.bg_grad.texture = Gradient.vertical(
                get_color_from_hex(self.hex[1]), get_color_from_hex(self.hex[0]))

            self.dialog.dismiss()

    def go_back(self):  # Function to go back to previous screen
        self.manager.current = 'playlist'
        self.manager.transition.direction = 'right'


class ChatUI(MDScreen):  # Initialising the Chat Screen
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 1
        self.list = []
        self.change = False

        with self.canvas.before:
            self.rect = Rectangle(texture=Gradient.vertical(get_color_from_hex('#1d2671'),
                                                            get_color_from_hex(
                                                                '#c33764')), size=Window.size)
            Window.bind(on_resize=self.resize)

        self.back_button = MDIconButton(
            icon='chevron-left', pos_hint={'top': 1, 'left': 1})
        self.back_button.bind(on_press=self.go_back)
        self.add_widget(self.back_button)

        self.layout = MDCard(size_hint=(1, 0.1), pos_hint={
            'center_x': 0.5, 'bottom': 1}, md_bg_color=get_color_from_hex('#a5d7e8'), elevation=3)

        self.sub_layout2 = MDBoxLayout(
            size_hint=(None, None),
            adaptive_size=True,
            padding=[500, 30, 10, 50],
            spacing="20px", pos_hint={
                'center_x': 0.5, 'bottom': 1}
        )

        self.scroll = MDScrollView(do_scroll_x=False, pos_hint={'top': 0.95}, size_hint_y=0.85, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0], background_hue='100', effect_cls=OpacityScrollEffect)
        self.add_widget(self.scroll)

        self.sub_layout = MDStackLayout(size_hint=(None, None),
                                        spacing="30dp", adaptive_height=True, width="1920dp", padding=[135, 20, 20, 30])
        self.scroll.add_widget(self.sub_layout)

        self.sub_layout3 = MDBoxLayout(
            padding=[8, 3, 2, 2],
            orientation='horizontal', size_hint=(None, None), adaptive_height=True, spacing="50px", width="1800dp"
        )
        self.sub_layout.add_widget(self.sub_layout3)

        self.upload = Button(background_normal='images/ai.jpg',
                             size_hint=(None, None), background_down='images/loading.png', valign='center', border=(0, 0, 0, 0))

        self.sub_layout3.add_widget(self.upload)
        self.card = MDCard(size_hint=(None, None), style='outlined',
                           height="100dp", width="1500dp", radius=20, elevation=0, md_bg_color=get_color_from_hex('#00FFFFFF'))
        self.sub_layout3.add_widget(self.card)

        self.text = MDLabel(text="Heya my friend, I am Euphonious. How can I help you today?", size_hint=(
            1, 1), bold=True, font_style="H4", italic=True, valign='top', padding=[15, 0], height="100dp", halign='left', markup=True)
        self.card.add_widget(self.text)

        if len(self.text.text) > 178:
            if '\n' in self.text.text:
                count = self.text.text.count('\n')
                self.card.height = f"{(len(self.text.text)/178)*110 * count/count-1.5}dp"
            else:
                self.card.height = f"{(len(self.text.text)/178)*110}dp"

        self.text_input = MDTextField(
            mode='fill', hint_text="Send a message", pos_hint={
                'center_x': 0.5, 'top': 0.1}, size_hint=(None, None), size=(1550, 400), multiline=True, radius=(30, 30, 30, 30), max_height='500dp')
        self.add_widget(self.text_input)
        self.list.append(self.text_input.pos)

        self.send_button = MDIconButton(icon='send', md_bg_color="blue", pos_hint={
            'center_x': 0.93, 'top': 0.10})
        self.send_button.bind(on_press=self.send_user_message)
        self.add_widget(self.send_button)

    def on_pre_enter(self):  # Function called just before entering the screen
        self.account = Database.acc_details()

    def go_back(self, dt):  # Function called to go back to the previous screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'

    def send_user_message(self, dt):  # Function to send the user's message
        self.counter += 1
        self.text = self.text_input.text
        self.text_input.text = ''
        self.text_input.disabled = True
        self.send_button.disabled = True

        self.sub_layout4 = MDBoxLayout(
            padding=[8, 3, 3, 2],
            orientation='horizontal', size_hint=(None, None), adaptive_height=True, spacing="50px", width="1800dp"
        )
        self.sub_layout.add_widget(self.sub_layout4)
        self.upload2 = Button(background_normal=self.account[4],
                              size_hint=(None, None), background_down='images/loading.png', valign='top', border=(0, 0, 0, 0), pos_hint={'top': 0.7})
        self.sub_layout4.add_widget(self.upload2)

        self.card2 = MDCard(size_hint=(None, None),
                            height="100dp", width="1500dp", radius=20, elevation=0, md_bg_color=[0, 0, 0, 0], pos_hint={'top': 0.7})
        self.sub_layout4.add_widget(self.card2)

        self.text2 = MDLabel(text=self.text, size_hint=(
            1, 1), bold=True, font_style="H4", halign='left', padding=[15, 3], italic=True, valign='top')
        self.card2.add_widget(self.text2)
        Clock.schedule_once(self.get_texture_size, 0)

        if self.counter != 2:
            self.scroll.scroll_to(widget=self.text2, animate={
                                  'transition': 'in_out_sine'})

        Thread(target=self.get_ai_message,
               name='AI_Message', daemon=True).start()

    def get_texture_size(self, dt):  # Function to set the height of user's message card
        self.card2.height = self.text2.texture_size[1] + \
            2*self.text2.padding[1]

    def move(self, dt):  # Function to change cursor icon when on focus
        Window.set_system_cursor(cursor_name='hand')

    def leave(self, dt):  # Function to change cursor icon when out of focus
        Window.set_system_cursor(cursor_name='arrow')

    def get_ai_message(self):  # Function to get response from AI
        try:
            AIChatBot.counter = 1
            self.ai_text = AIChatBot.output(text=self.text2.text).strip()
            Clock.schedule_once(self.send_ai_message)
        except:
            self.ai_text = random.choice([
                'Oops!!! There seems to be an unknown issue please try again.',
                'Mhmm... Maybe somethings not going well. Try Again!',
                'I dont know what happened there could you please tell me once more',
                'I think im becoming deaf. Cant hear what you say'
            ])
            Clock.schedule_once(self.send_ai_message)

    def send_ai_message(self, dt):  # Function to send the response from AI
        self.counter += 1
        self.sub_layout5 = MDBoxLayout(
            padding=[8, 3, 2, 3],
            orientation='horizontal', size_hint=(None, None), adaptive_height=True, spacing="50px", width="1800dp"
        )
        self.sub_layout.add_widget(self.sub_layout5)

        self.upload = Button(background_normal='images/ai.jpg',
                             size_hint=(None, None), background_down='images/loading.png', valign='center', border=(0, 0, 0, 0), pos_hint={'top': 0.9})

        self.sub_layout5.add_widget(self.upload)
        self.card = MDCard(size_hint=(None, None),
                           height="100dp", width="1500dp", radius=20, elevation=0, md_bg_color="#00FFFFFF", pos_hint={'top': 0.9})
        self.sub_layout5.add_widget(self.card)

        self.text = MDLabel(text=self.ai_text, size_hint=(
            1, 1), bold=True, font_style="H4", italic=True, valign='top', padding=[15, 0], height="100dp", halign='left')
        self.card.add_widget(self.text)

        Clock.schedule_once(self.ai_texture_size, 0)

        self.scroll.scroll_to(widget=self.text, animate={
            'transition': 'in_out_sine'})

        self.text_input.disabled = False
        self.send_button.disabled = False

        self.value = AIChatBot.output3()

        if self.value[0] == True:
            Clock.schedule_once(self.musicplayer)

    def ai_texture_size(self, dt):  # Function to set the height of AI's response card
        if '\n' in self.text.text:
            self.card.height = self.text.texture_size[1] + \
                2*self.text.padding[1]
        else:
            if len(self.text.text) > 178:
                self.card.height = f"{(len(self.text.text)/178)*110}dp"

    # Function to resize the background gradient colour w.r.t screen size
    def resize(self, window, width, height):
        self.rect.size = Window.size

    def Window_Size(self):  # Function to get the current window size
        return Window.size

    def musicplayer(self, dt):  # Function to change to musicplayer
        self.manager.get_screen('musicplayer').new = True
        self.manager.get_screen('musicplayer').prev_screen = 'chat'
        self.manager.get_screen(
            "musicplayer").song_name = self.value[1]
        self.manager.get_screen("musicplayer").clicked = True
        if self.manager.get_screen("musicplayer").sound and self.manager.get_screen("musicplayer").sn != self.value[1]:
            self.manager.get_screen("musicplayer").sound.stop()
        self.manager.current = 'musicplayer'
        self.manager.transition.direction = 'left'


class AIChatBot():  # Initialising the AIChatBot Class
    global agent_chain
    global new_memory
    global conversation
    global memory_list
    global memory
    global screen_change
    global song_name
    global author
    global sql_agent
    memory_list = []
    counter = 0
    screen_change = False
    song_name = None
    author = None

    dburl = ''
    db = SQLDatabase.from_uri(dburl)

    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
        ),
        Tool(
            name="play song",
            func=lambda text: AIChatBot.sqloutput(text),
            description="strictly use it when user wants to listen to a song. As soon as you get a positive observation display the success message 'playing song song_name'"
        ),
        Tool(
            name="create playlist",
            func=lambda string: AIChatBot.playlist_parser(string),
            description="""strictly use it only when user wants to create a playlist. The input to this should be in the format 'name, image', name is name of playlist and image is path of image. 
            If no name is given set name as per your wish, if no image is given set image to 'images/upload.png'. Do not add songs to playlist unless/until user has specifically mentioned about it.
            The final output should 'Successfuly created the playlist playlist_name' only"""
        ),
        Tool(
            name="add new song to playlist",
            func=lambda string: AIChatBot.playlist_song_parser(string),
            description="""strictly use it only when user wants to add song to playlist. The input format must be 'playlist_name, the type/name of song user wants to listen'. 
            if no playlist_name given ask the user to specify a playlist, if no name/type of song given then 'playlist_name, a random song from playlist' should be the input. Answer based on observation
            Remember to not to use this command unless/until user has asked to add a song to the playlist."""
        ),
        WriteFileTool(),
        ReadFileTool(),
        MoveFileTool()
    ]

    prefix = "You are Euphonius, A multifunctional chatbot that tends to user's queries. Perform the actions correctly"

    llm = ChatOpenAI(temperature=0,
                     model="gpt-3.5-turbo-0613", max_tokens=3000)
    agent_chain = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, early_stopping_method='generate',
                                   verbose=True, agent_kwargs={'prefix': prefix}, max_iterations=5)

    db = SQLDatabase.from_uri(
        '', sample_rows_in_table_info=10)
    sql_llm = ChatOpenAI(temperature=0.1, model='gpt-3.5-turbo-0613',
                         openai_api_key='')
    sql_agent = SQLDatabaseSequentialChain.from_llm(llm=sql_llm,
                                                    database=db, return_direct=True)

    def output(text):
        global screen_change  # Function to return AI Response
        screen_change = False
        output = agent_chain.run(input=text)

        return output

    def output3():  # Function which checks if the screen is to be changed to musicplayer
        return (screen_change, song_name, author)

    def output4(value: bool):  # Function which shows the value of screen_change variable
        global screen_change
        screen_change = value
        return screen_change

    def sqloutput(text):  # Function to get output by querying database using AI
        agent_chain.max_iterations = 2
        out = sql_agent.run(
            f"Fetch a song according to the following request (always use order by rand() along with user's request): {text}")
        print(out)
        y = ast.literal_eval(out)
        if len(y) == 0 or len(y[0]) == 0:
            return "Couldnt fetch the required song"
        elif len(y[0]) == 7:
            x = y[0][1]
            AIChatBot.song_infos(y[0][1], y[0][2])
        else:
            x = y[0][0]
            AIChatBot.song_infos(y[0][0], y[0][1])
        agent_chain.max_iterations = 5

        return f"Song {x} being played successfully"

    # Function to get song info collected from database
    def song_infos(name_of_song: str, author_of_song: str):
        global song_name
        global author
        global screen_change
        song_name = name_of_song
        author = author_of_song
        screen_change = True

    def playlist_parser(string: str):  # Function to parse input for creating playlist
        if ',' in string:
            a, b = string.split(',')
            return AIChatBot.create_playlist(a.strip(), b.strip())
        else:
            return AIChatBot.create_playlist(string, None)

    # Function to create playlist using AI
    def create_playlist(name: str, image: str = None):
        if image == None or os.path.isfile(image) == False:
            image = 'images/upload.png'
        try:
            color_thief = ColorThief(image)
            palette = color_thief.get_palette(color_count=2)
            l = []

            for i in palette:
                l.append('#%02x%02x%02x' % i)
            colour = str(l)
        except:
            colour = str(["#000000", "#00007c"])
        today = date.today()
        t = today.strftime("%d/%m/%Y")
        user = Database.acc_details()[0]
        try:
            Database.create_playlist(
                name=name, image=image, user=user, date=t, colours=colour)
            return f"Playlist {name} created successfully"
        except Exception as e:
            return "Unable to create playlist"

    # Function to parse input for adding song to playlist
    def playlist_song_parser(string: str):
        if ',' in string:
            a, b = string.split(',')
            return AIChatBot.add_playlist_song(a.strip(), b.strip())
        else:
            a, b = string, 'a random song'
            return AIChatBot.add_playlist_song(a.strip(), b)

    # Function to add song to playlist using AI
    def add_playlist_song(name: str, text: str):
        user = Database.acc_details()[0]
        try:
            playlist_id = Database.playlists_info(
                username=user, play_name=name)[0]
        except:
            return "Playlist {name} Not Found"

        db = SQLDatabase.from_uri(
            '', sample_rows_in_table_info=10)
        llm = ChatOpenAI(temperature=0.1, model='gpt-3.5-turbo-0613')
        agent = SQLDatabaseSequentialChain.from_llm(llm=llm,
                                                    database=db, return_direct=True)
        out = agent.run(
            f"Fetch the id and name of the song as per the following request: {text}")
        y = ast.literal_eval(out)
        if len(y) == 0 or len(y[0]) == 0:
            return "Couldnt add the required song"
        else:
            song_id = y[0][0]
            song_name = y[0][1]
            Database.add_playlist_song(
                playlist_id=playlist_id, song_id=song_id, song_name=song_name)
            return f"Song {song_name} added to playlist {name}"


class UserProfile(MDScreen):  # Initialising UserProfile screen
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account = None

        self.acc_details = None

        self.sub_layout1 = MDBoxLayout(
            orientation='vertical', pos_hint={'center_x': 0.73, 'top': 0.9}, size_hint_y=0.15)
        self.add_widget(self.sub_layout1)

        self.username = MDLabel(
            text='', font_style="H3", bold=True)
        self.sub_layout1.add_widget(self.username)

        self.email = MDLabel(
            text='', font_style="H6", bold=True)
        self.sub_layout1.add_widget(self.email)

        self.infos = MDLabel(
            text="", font_style="Subtitle1", bold=True)
        self.sub_layout1.add_widget(self.infos)

        self.scroll = MDScrollView(do_scroll_x=False, pos_hint={'top': 0.65}, size_hint_y=0.9, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)

        self.sub_layout3 = MDBoxLayout(
            orientation='horizontal', size_hint_x=1, spacing="20dp")
        self.sub_layout1.add_widget(self.sub_layout3)

        self.icon1 = MDIconButton(icon='rename-outline', pos_hint={
                                  'top': 1}, icon_size='23sp', md_bg_color=[0, 1, 1, 0.5], on_press=self.account_edit_confirmation)
        self.sub_layout3.add_widget(self.icon1)
        self.icon2 = MDIconButton(icon='image-edit-outline', pos_hint={
                                  'top': 1}, icon_size='23sp', md_bg_color=[0, 1, 1, 0.5], on_press=self.confirm_user_image)
        self.sub_layout3.add_widget(self.icon2)

        self.main_layout = MDBoxLayout(
            orientation='vertical', size_hint_y=None, height="700dp", spacing="10dp", padding=[0, 10, 0, 0])
        self.scroll.add_widget(self.main_layout)

        self.top_bar = MDTopAppBar(left_action_items=[['chevron-left', lambda x: self.go_back()],],
                                   title="Music Player",
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0
                                   )
        self.add_widget(self.top_bar)

        self.nav_drawer = MDNavigationDrawer(
            enable_swiping=True, spacing=dp(25))
        self.nav_menu = MDNavigationDrawerMenu(spacing=dp(35))

        self.nav_account = MDNavigationDrawerItem(
            text='Account', icon="account", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_profile)
        self.nav_menu.add_widget(self.nav_account)

        self.nav_playlist = MDNavigationDrawerItem(
            text='Playlist', icon="playlist-music", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)
        self.nav_playlist.bind(on_release=self.to_playlist)

        self.nav_divider = MDNavigationDrawerDivider()
        self.nav_menu.add_widget(self.nav_divider)

        self.chatbot = MDNavigationDrawerItem(
            text='Euphonious', icon="robot", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.chatbot)
        self.chatbot.bind(on_release=self.to_chat)

        self.nav_settings = MDNavigationDrawerItem(
            text='Settings', icon="tools", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_settings)
        self.nav_menu.add_widget(self.nav_settings)

        self.nav_logout = MDNavigationDrawerItem(
            text='Logout', icon="logout", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_logout.bind(on_release=self.logout)
        self.nav_menu.add_widget(self.nav_logout)

        self.nav_layout = MDNavigationLayout()
        self.nav_drawer.add_widget(self.nav_menu)
        self.nav_layout.add_widget(self.nav_drawer)
        self.add_widget(
            MDNavigationRail(
                MDNavigationRailMenuButton(
                    icon='menu',
                    on_press=lambda x: self.nav_drawer.set_state('open')
                ),
                MDNavigationRailItem(
                    text="HOME",
                    icon="home",
                    on_press=self.to_main,
                ),
                MDNavigationRailItem(
                    text="MUSIC",
                    icon="music",
                    on_press=self.to_player,
                ),
                MDNavigationRailItem(
                    text="ASSISTANT",
                    icon="robot-happy-outline",
                    on_press=lambda x: Thread(
                        target=self.manager.get_screen('main').mic_ask, daemon=True).start()
                ),
                md_bg_color=(1, 0, 0, 0),
                pos_hint={'top': 0.97, 'center_x': 0.02},
                size_hint=(0.105, 5),
                padding=[0, 25, 0, 70],
                spacing="390dp"
            )
        )
        self.add_widget(self.nav_layout)

    def to_main(self, dt):  # Function to change to main screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'

    def to_player(self, instance):  # Function to change to musicplayer
        try:
            self.manager.get_screen('musicplayer').music_icon_clicked = True
            self.manager.get_screen('musicplayer').prev_screen = 'profile'
            self.manager.current = 'musicplayer'
            self.manager.transition.direction = 'left'
        except:
            pass

    def to_profile(self, dt):  # Function to change to user account screen
        self.manager.current = 'profile'
        self.manager.transition.direction = 'left'

    def to_settings(self, dt):  # Function to change to settings screen
        self.manager.current = 'settings'
        self.manager.transition.direction = 'left'

    def logout(self, dt):  # Function to logout
        pass

    def to_playlist(self, dt):  # Function to change to playlist screen
        self.manager.current = 'playlist'
        self.manager.transition.direction = 'left'

    def to_chat(self, dt):  # Function to change to chat screen
        self.manager.current = 'chat'
        self.manager.transition.direction = 'left'

    def on_pre_enter(self):  # Function called just before entering the screen

        self.account = self.manager.get_screen('main').account

        self.playlist_count = Database.playlist_count(
            username=self.account[0])[0]
        self.top_songs = Database.top_played(
            username=self.account[0])

        with self.canvas.before:
            Color(1, 1, 1, mode='rgb')
            self.user_image = Ellipse(
                source=self.account[4], size=(248, 248), pos=(130, 750))

        self.username.text = self.account[0]
        self.email.text = self.account[1]

        self.infos.text = f'{self.playlist_count} Playlists | Joined On {datetime.datetime.strptime(f"{self.account[5]}", rf"%Y-%m-%d").strftime(rf"%d/%m/%Y")}'

        if len(self.top_songs) == 3:
            self.main_layout.clear_widgets()
            self.sub_layout2 = MDGridLayout(
                size_hint_y=5, size_hint_x=0.4, cols=3, spacing="35dp", padding="25dp", pos_hint={'center_x': 0.25, 'top': 0.7})
            self.song_details = []
            for i in self.top_songs:
                self.song_details.append(Database.get_song_detail(id=i[0]))
            self.label1 = MDLabel(
                text='Most Played Songs', font_style='H3', size_hint_y=None, height="25dp", bold=True, pos_hint={'center_x': 0.545, 'top': 1})
            self.main_layout.add_widget(self.label1)
            self.main_layout.add_widget(self.sub_layout2)

            l = [[214/255, 175/255, 54/255, 0.75], [167/255, 167 /
                                                    255, 173/255, 0.75], [167/255, 112/255, 68/255, 0.75]]
            for i in range(3):

                self.card = MDSmartTile(radius=30, box_radius=[0, 0, 30, 30], size_hint_x=None, width="420dp", box_color=l[i],
                                        lines=2, height="375dp", size_hint_y=None, source=self.song_details[i][3])
                self.songs_authors = TwoLineListItem(_no_ripple_effect=True, pos_hint={'center_y': 0.5},
                                                     text=f'[size=25][b]{self.song_details[i][1]}[/b][/size]', secondary_text=f'[b]{self.song_details[i][2]}[/b]')
                self.card.add_widget(self.songs_authors)
                self.card.bind(on_press=self.musicplayer)
                self.sub_layout2.add_widget(self.card)

    def musicplayer(self, instance):  # Function to change to musicplayer screen
        s = instance.children[0].children[0].text
        song_name = s.split('[b]')[1].split('[/b]')[0]
        self.manager.get_screen('musicplayer').new = True
        self.manager.get_screen('musicplayer').prev_screen = 'profile'
        self.manager.get_screen(
            "musicplayer").song_name = song_name
        self.manager.get_screen("musicplayer").clicked = True
        if self.manager.get_screen("musicplayer").sound and self.manager.get_screen("musicplayer").sn != song_name:
            self.manager.get_screen("musicplayer").sound.stop()
        self.manager.current = 'musicplayer'

    # Function to show dialog box to change account details
    def account_edit_confirmation(self, dt):

        self.dialog_layout = MDBoxLayout(orientation='vertical', pos_hint={
                                         'center_x': 0.5, 'center_y': 0.5}, height='200dp', spacing="10dp", size_hint_y=None)

        self.username_edit = MDTextField(hint_text="username", mode='rectangle', size_hint_x=0.65, pos_hint={
                                         'center_x': 0.5, 'center_y': 0.5}, icon_left='account')
        self.email_edit = MDTextField(hint_text='email', mode='rectangle', size_hint_x=0.65, pos_hint={
            'center_x': 0.5, 'center_y': 0.5}, icon_left='email')
        self.password_edit = MDTextField(hint_text='password', mode='rectangle', size_hint_x=0.65, pos_hint={
                                         'center_x': 0.5, 'center_y': 0.5}, icon_left='key')

        self.dialog_layout.add_widget(self.username_edit)
        self.dialog_layout.add_widget(self.email_edit)
        self.dialog_layout.add_widget(self.password_edit)

        self.dialog = MDDialog(
            title="Edit Account Details",
            text='Change only the details you wish to be changed',
            type="custom",
            auto_dismiss=False,
            content_cls=self.dialog_layout,
            buttons=[
                MDFlatButton(
                    text="CONFRIM",
                    on_release=self.edit_account
                ),
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )

        self.dialog.open()

    def edit_account(self, dt):  # Function to edit account details
        if self.username_edit.text != '' or self.email_edit.text != '' or self.password_edit.text != '':
            Database.account_edit(acc=self.account, username=(self.username_edit.text if self.username_edit.text != '' else None),
                                  email=(self.email_edit.text if self.email_edit.text != '' else None), password=(self.password_edit.text if self.password_edit.text != '' else None))
            self.account = Database.acc_details()
            self.username.text = self.account[0]
            self.email.text = self.account[1]
            self.dialog.dismiss()

            self.manager.get_screen(
                'main').nav_header.title = self.username.text
            self.manager.get_screen('main').nav_header.text = self.email.text

    # Function to show dialog box to change user image
    def confirm_user_image(self, dt):
        self.upload = Button(background_normal=self.account[4],
                             on_press=self.choose, background_down='images/loading.png', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint_y=None, height="300dp")

        self.dialog = MDDialog(
            title="Edit Profile Picture",
            type="custom",
            auto_dismiss=False,
            content_cls=self.upload,
            buttons=[
                MDFlatButton(
                    text="CONFIRM",
                    on_release=self.image_edit_user
                ),
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )

        self.dialog.open()

    def choose(self, dt):  # Function to choose image
        try:
            self.play_img = filechooser.open_file()
            self.upload.background_normal = self.play_img[0]
        except:
            toast(text="Unable to load image")

    def image_edit_user(self, dt):  # Function to edit user image
        if self.upload.background_normal != 'images/account.png':

            Database.account_edit(
                acc=self.account, image=self.upload.background_normal)
            self.user_image.source = self.upload.background_normal

            self.dialog.dismiss()

    def go_back(self):  # Function to go back to the previous screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'


class Settings(MDScreen):  # Initialising Settings screen
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.prev_screen = None

        with self.canvas.before:
            Color(0, 0, 0.3, mode='hex', group=u'color')
            self.rect = Rectangle(texture=Gradient.vertical([0, 0, 0.3, 0.3], [0, 0, 0.5, 0.5], [0, 0, 1, 0.5]),
                                  size=(1920, 1080), group=u"rect")

        self.sleep_time = None

        self.scroll = MDScrollView(do_scroll_x=False, pos_hint={'top': 0.93}, size_hint_y=0.9, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)

        self.main_layout = MDBoxLayout(
            orientation='vertical', size_hint_y=None, adaptive_height=True, spacing="10dp", padding="20dp")
        self.scroll.add_widget(self.main_layout)

        self.sub_layout2 = MDBoxLayout(
            orientation='vertical', size_hint_y=None, adaptive_height=True, spacing="10dp", padding="20dp")
        self.main_layout.add_widget(self.sub_layout2)

        self.label2 = MDLabel(text="Accessibility Features",
                              font_style='H4', bold=True, pos_hint={'center_x': 0.545})
        self.sub_layout2.add_widget(self.label2)

        self.list2 = MDList(pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        self.sub_layout2.add_widget(self.list2)

        self.listitem3 = TwoLineRightIconListItem(
            text='Set Sleep Time', secondary_text="Set sleep time so that the app closes automatically after the selected time")
        self.list2.add_widget(self.listitem3)

        self.listitem3icon = IconRightWidget(
            icon='timer-off', on_press=self.time_pick)
        self.listitem3.add_widget(self.listitem3icon)

        self.listitem8 = TwoLineRightIconListItem(
            text='Notifications', secondary_text='Enable/Disable notification when new song is played'
        )
        self.listitem8icon = IconRightWidget(icon='toggle-switch-off', on_press=self.notif_config, icon_size='40sp'
                                             )
        self.list2.add_widget(self.listitem8)
        self.listitem8.add_widget(self.listitem8icon)

        self.sub_layout3 = MDBoxLayout(
            orientation='vertical', size_hint_y=None, adaptive_height=True, spacing="10dp", padding="20dp")
        self.main_layout.add_widget(self.sub_layout3)

        self.label3 = MDLabel(text="Privacy",
                              font_style='H4', bold=True, pos_hint={'center_x': 0.545})
        self.sub_layout3.add_widget(self.label3)

        self.list3 = MDList(pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        self.sub_layout3.add_widget(self.list3)

        self.listitem6 = TwoLineRightIconListItem(
            text='AI Recommendations', secondary_text='Enable/Disable Song Recommendations based on your listening history')
        self.list3.add_widget(self.listitem6)

        self.listitem6icon = IconRightWidget(icon_size='43sp',
                                             icon='toggle-switch', on_press=self.ai_recommendations)
        self.listitem6.add_widget(self.listitem6icon)

        self.listitem9 = TwoLineRightIconListItem(
            text='Download User Data', secondary_text='Downloads your data stored in the database and saves it in the desktop as a text file named "EuphoniusUserData"'
        )
        self.listitem9icon = IconRightWidget(
            icon='download', on_press=self.user_data
        )
        self.list3.add_widget(self.listitem9)
        self.listitem9.add_widget(self.listitem9icon)

        self.top_bar = MDTopAppBar(left_action_items=[['chevron-left', lambda x: self.go_back()],],
                                   title="Music Player",
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0
                                   )
        self.add_widget(self.top_bar)

        self.nav_drawer = MDNavigationDrawer(
            enable_swiping=True, spacing=dp(25))
        self.nav_menu = MDNavigationDrawerMenu(spacing=dp(35))

        self.nav_account = MDNavigationDrawerItem(
            text='Account', icon="account", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_profile)
        self.nav_menu.add_widget(self.nav_account)

        self.nav_playlist = MDNavigationDrawerItem(
            text='Playlist', icon="playlist-music", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)
        self.nav_playlist.bind(on_release=self.to_playlist)

        self.nav_divider = MDNavigationDrawerDivider()
        self.nav_menu.add_widget(self.nav_divider)

        self.chatbot = MDNavigationDrawerItem(
            text='Euphonious', icon="robot", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.chatbot)
        self.chatbot.bind(on_release=self.to_chat)

        self.nav_settings = MDNavigationDrawerItem(
            text='Settings', icon="tools", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF", on_release=self.to_settings)
        self.nav_menu.add_widget(self.nav_settings)

        self.nav_logout = MDNavigationDrawerItem(
            text='Logout', icon="logout", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_logout.bind(on_release=self.logout)
        self.nav_menu.add_widget(self.nav_logout)

        self.nav_layout = MDNavigationLayout()
        self.nav_drawer.add_widget(self.nav_menu)
        self.nav_layout.add_widget(self.nav_drawer)

        self.add_widget(
            MDNavigationRail(
                MDNavigationRailMenuButton(
                    icon='menu',
                    on_press=lambda x: self.nav_drawer.set_state('open')
                ),
                MDNavigationRailItem(
                    text="Home",
                    icon="home",
                    on_press=self.to_main,
                ),
                MDNavigationRailItem(
                    text="Music",
                    icon="music",
                    on_press=self.to_player,
                ),
                MDNavigationRailItem(
                    text="Assistant",
                    icon="robot-happy-outline",
                    on_press=lambda x: Thread(
                        target=self.manager.get_screen('main').mic_ask, daemon=True).start()
                ),
                md_bg_color=(1, 0, 0, 0),
                pos_hint={'top': 0.97, 'center_x': 0.02},
                size_hint=(0.105, 5),
                padding=[0, 25, 0, 70],
                spacing="390dp"
            )
        )
        self.add_widget(self.nav_layout)

    def to_main(self, dt):  # Function to change to main screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'

    def to_player(self, instance):  # Function to change to musicplayer
        try:
            self.manager.get_screen('musicplayer').music_icon_clicked = True
            self.manager.get_screen('musicplayer').prev_screen = 'settings'
            self.manager.current = 'musicplayer'
            self.manager.transition.direction = 'left'
        except:
            pass

    def to_profile(self, dt):  # Function to change to user account screen
        self.manager.current = 'profile'
        self.manager.transition.direction = 'left'

    def to_settings(self, dt):  # Function to change to settings screen
        self.manager.current = 'settings'
        self.manager.transition.direction = 'left'

    def logout(self, dt):  # Function to logout
        pass

    def to_playlist(self, dt):  # Function to change to playlist screen
        self.manager.current = 'playlist'
        self.manager.transition.direction = 'left'

    def to_chat(self, dt):  # Function to change to chat screen
        self.manager.current = 'chat'
        self.manager.transition.direction = 'left'

    # Function to enable/disable recommendation button
    def ai_recommendations(self, dt):
        if self.listitem6icon.icon == 'toggle-switch':
            self.listitem6icon.icon = 'toggle-switch-off'
            with open("Settings/settings.json") as f:
                data = json.load(f)

                data["Recommendations"] = "Disabled"

            with open("Settings/settings.json", "w") as f:
                json.dump(data, f)

            toast("Turned off Assistant Recommendations")
        else:
            self.listitem6icon.icon = 'toggle-switch'
            with open("Settings/settings.json") as f:
                data = json.load(f)

                data["Recommendations"] = "Enabled"

            with open("Settings/settings.json", "w") as f:
                json.dump(data, f)
            toast("Turned On Assistant Recommendations")

    def time_pick(self, dt):  # Function to pick time for sleep mode
        if self.listitem3icon.icon == 'timer-off':
            self.picker = MDTimePicker(size_hint=(0.5, 0.5), pos_hint={
                'center_x': 0.5, 'center_y': 0.5})
            self.picker.open()
            self.picker.bind(time=self.get_time)

            self.listitem3icon.icon = 'timer'
            Clock.schedule_interval(self.check_time, 1)
        else:
            toast('Sleep Mode Off')
            self.listitem3icon.icon = 'timer-off'

    def get_time(self, instance, time):  # Function to get the time picked
        self.sleep_time = time

    def check_time(self, dt):  # Function to check the time until app is closed
        c = datetime.datetime.now()
        current_time = c.strftime('%H:%M:%S')

        if str(self.sleep_time) != current_time:
            return
        else:
            Clock.unschedule(self.check_time)
            self.listitem3icon.icon = 'timer-off'
            toast("App Will Close in 10 seconds")
            Clock.schedule_once(lambda x: MDApp.get_running_app().stop(), 10)

    def notif_config(self, dt):  # Function to enable/disable notifications
        if self.listitem8icon.icon == 'toggle-switch-off':
            with open("Settings/settings.json") as f:
                data = json.load(f)

                data["Notifications"] = "Enabled"

            with open("Settings/settings.json", "w") as f:
                json.dump(data, f)
            self.listitem8icon.icon = 'toggle-switch'
            toast("Notifications Enabled")
        else:
            with open("Settings/settings.json") as f:
                data = json.load(f)

                data["Notifications"] = "Disabled"

            with open("Settings/settings.json", "w") as f:
                json.dump(data, f)
            self.listitem8icon.icon = 'toggle-switch-off'
            toast("Notifications Disabled")

    def user_data(self, dt):  # Function to get user account data stored in database
        with open(rf'C:\Users\pc\Desktop\ChorduceUserData.txt', 'a') as f:
            data = Database.acc_details()
            for i in data:
                f.write(str(i)+"\n")
            toast("User Data Saved To Desktop")

    def go_back(self):  # Function to go back to previous screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'


class Lyrics(MDScreen):  # Initialising Lyrics screen
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.not_found = False
        self.lyrics = 'Not Found'
        LabelBase.register(
            name='arial', fn_regular='fonts/ArialUnicodeMS.ttf')

        self.scroll_view = MDScrollView(do_scroll_x=False, pos_hint={'top': 0.93, 'center_x': 0.4}, size_hint_y=0.9, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                        always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll_view)

        self.label = MDLabel(text=f"[font=arial]{self.lyrics}[/font]", font_style='H3', padding=(400, 0, 0, 0), bold=True, font_family='fonts/ArialUnicodeMS.ttf',
                             size_hint=(None, None), width="1600dp", halign='left', pos_hint={'right': 0.4}, markup=True, allow_copy=True, allow_selection=True)
        self.scroll_view.add_widget(self.label)

        self.top_bar = MDTopAppBar(left_action_items=[['chevron-down', lambda x: self.go_back()],],
                                   title="Music Player",
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0
                                   )
        self.add_widget(self.top_bar)

    def on_pre_enter(self):  # Function called just before entering the screen
        Clock.schedule_once(self.lyric_height)

    def lyric_height(self, dt):  # Function to set the lyrics label height
        self.label.height = self.label.texture_size[1]

    def go_back(self):  # Function to go back to the previous screen
        self.manager.current = 'main'
        self.manager.transition.direction = 'down'


class Chorduce(MDApp):  # Initialising the Main Chorduce App
    def build(self):  # Function to build the app

        Database.connect()  # Connecting to the database
        self.icon = 'images/Chorduce icon.png'  # Setting app icon
        self.title = "Chorduce"  # Setting app title
        self.theme_cls.theme_style = "Dark"  # Setting Dark Theme
        sm = MDScreenManager()

        # Adding different screens to the app on startup
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(MusicPlayer(name='musicplayer'))
        sm.add_widget(Lyrics(name='lyrics'))
        sm.add_widget(ChatUI(name='chat'))
        return sm


if __name__ == '__main__':
    Chorduce().run()  # Run the App
