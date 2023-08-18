from kivy.core.text import LabelBase
import random
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, HuggingFaceHub
from langchain.utilities import SerpAPIWrapper
from kivy_garden.frostedglass import FrostedGlass
from kivy.core.window import WindowBase
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.memory import ConversationEntityMemory
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains import SQLDatabaseSequentialChain
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.agents.agent_toolkits import GmailToolkit
from datetime import datetime
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import faiss
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS
from langchain import LLMChain
from langchain.agents import LLMSingleActionAgent
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, StructuredChatAgent
from langchain.prompts.base import BasePromptTemplate
from langchain.prompts.chat import BaseMessagePromptTemplate
from langchain.memory.chat_message_histories import RedisChatMessageHistory
import pyjokes
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.tools import StructuredTool
import ast
from langchain import HuggingFaceHub
import speech_recognition
import pyttsx3
from io import BytesIO
from kivy.cache import Cache
import os
# os.environ["KIVY_VIDEO"] = "python-vlc"
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
from kivymd.uix.toolbar import MDTopAppBar
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
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.navigationrail import (
    MDNavigationRail,
    MDNavigationRailMenuButton,
    MDNavigationRailFabButton,
    MDNavigationRailItem,
)
import requests
# Window.fullscreen = 'auto'
# Window.borderless = True

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', -1500)
Config.set('graphics', 'top',  1000)
Config.set('graphics', 'resizable', 'False')
Config.set('graphics', 'borderless',  1)
Config.set('graphics', 'width', 0)
Config.set('graphics', 'height', 0)


account = ("", "", "")
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
        cursor.execute('INSERT INTO users (username, email, phone, password) VALUES (%s, %s, %s, %s)',
                       (username, email, phone, password))
        cnx.commit()
        global account
        global logged_in
        cursor.execute(
            'SELECT username, email, password FROM users WHERE email=%s AND password = %s', (email, password))
        account = cursor.fetchone()
        logged_in = True
        return True, account

    def login(email, password):
        cursor.execute(
            'SELECT username, email, password FROM users WHERE email=%s AND password = %s', (email, password))
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

    def get_song_detail(name=None, id=None):
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
            cursor.execute(
                f"SELECT * FROM songs WHERE title LIKE '{text}%' OR author LIKE '%{text}%' OR image LIKE '%{text}%' OR language LIKE '%{text}%' OR genre LIKE '%{text}%' GROUP BY title LIMIT 20")
            result = cursor.fetchall()
            return result
        except:
            return None

    def playlists_info(username):
        try:
            cursor.execute(
                "SELECT * FROM playlists WHERE user = %s", (username, ))
            result = cursor.fetchall()
            return result
        except:
            return 0

    def create_playlist(name, image, user, date):
        try:
            cursor.execute(
                "INSERT INTO playlists (name, image, user, created) VALUES (%s, %s, %s, %s)", (name, image, user, date))
            cnx.commit()
        except:
            raise Exception

    def playlist_songs(id, order_by=None):
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

    def add_playlist_song(playlist_id, song_id, song_name):
        today = date.today().strftime("%Y/%m/%d")

        try:
            cursor.execute(
                "INSERT INTO playlist_songs (playlist_id, song_id, song_name, created) VALUES (%s, %s, %s, %s)", (playlist_id, song_id, song_name, today))
            cnx.commit()
        except Exception:
            raise Exception

    def delete_playlist(playlist_id):
        print("Entered")
        print(playlist_id)
        try:

            cursor.execute(
                f"DELETE FROM playlist_songs WHERE playlist_id = {playlist_id}")
            cnx.commit()
            print("Deleted playlist songs")

            cursor.execute(f"DELETE FROM playlists WHERE id = {playlist_id}")
            cnx.commit()
            print("Deleted playlist")

        except Exception:
            raise Exception

    def delete_playlist_song(playlist_id, song_id):
        try:
            cursor.execute(
                f'DELETE FROM playlist_songs WHERE playlist_id = {playlist_id} AND song_id = {song_id}')
            cnx.commit()
        except Exception:
            raise Exception

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

    def jsondata(email, password):
        store = JsonStore('app_details.json')
        store.put('login_details', email=email, password=password)

    def get_jsondata():
        store = JsonStore('app_details.json')
        username = store.get('login_details')['email']
        password = store.get('login_details')['password']
        if username:
            return username, password
        else:
            return None


'''Window.borderless = True
Window.fullscreen = 'auto'''


class WelcomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.video = Video(source="D:\\Music Player App\\login.mp4", options={
        #                   'eos': 'loop', 'allow_stretch': True, 'keep_ratio': True})
        # self.video.state = 'play'
        # self.add_widget(self.video)

        self.welc = MDBoxLayout(orientation='vertical',
                                size_hint=(0.37, 0.37),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=20, padding=20)

        self.img = Image(source="D:/Chapt 5 Python/Aeris1.png",
                         pos_hint={'center_x': 0.5, 'center_y': 0.8}, size_hint=(1, 1.5))
        self.welc.add_widget(self.img)
        self.per = MDLabel(text="Perilla", font_size='300sp',
                           halign='center', size_hint=(1, 0.4))
        self.welc.add_widget(self.per)

        self.welc_button = MDRectangleFlatButton(
            text="Welcome", pos_hint={'center_x': 0.5}, size_hint=(.5, .5))
        self.welc_button.bind(on_release=lambda p: self.next())
        self.welc.add_widget(self.welc_button)

        self.add_widget(self.welc)

    def next(self):
        # self.video.state = 'stop'

        self.manager.current = 'login'


class LoginScreen(MDScreen, MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        LabelBase.register(
            name='cracky', fn_regular='fonts/CurlzMT.ttf', fn_bold='fonts/CURLZ.ttf')

        self.login_form = MDCard(orientation='vertical',
                                 size_hint=(0.3, 0.5),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 elevation=5, spacing="10dp", padding="40dp")  # , md_bg_color=[1, 0, 0, 0])

        self.label = MDLabel(text='[font=cracky]Music Player App[/font]', pos_hint={'top': 1}, markup=True, font_family="fonts/CurlzMT.ttf",  # , theme_text_color='Custom',
                             halign='center', size_hint=(1, 0.0005), valign='top', font_style="H2", bold=True)
        self.login_form.add_widget(self.label)
        self.add_widget(FitImage(source='images/login.jpg'))

        self.email = MDTextField(mode='rectangle',
                                 hint_text="Email", helper_text="Invalid Email", helper_text_mode='on_error', line_anim=True, size_hint=(0.8, 0.5), pos_hint={'center_x': 0.5, 'top': 1})
        self.password = MDTextField(hint_text="Password", password=True, mode='rectangle',
                                    helper_text="Invalid Password", helper_text_mode='on_error', line_anim=True, size_hint=(0.8, 0.5), pos_hint={'center_x': 0.5, 'top': 1}, icon_right='eye-off')
        # self.password.bind(on_icon_right=self.icon)

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
        # self.icon_button = MDIconButton(
        #    icon='eye-off', theme_text_color="Hint", pos_hint={'center_x': 0.8, 'center_y': 0.8})
        # self.login_form.add_widget(self.icon_button)
        # self.icon_button.pos_hint = {'center_x': 0.5, 'top': 1}

        self.add_widget(self.login_form)

    '''def on_pre_enter(self, *args):
        data = Database.get_jsondata()

        if data != None:

            username = data[0]
            password = data[1]

            check = Database.login(email=username,
                                   password=password)

            if check:
                self.manager.add_widget(MainScreen(name='main'))
                self.manager.current = 'main'''

    def icon(self, instance):
        if instance.icon_right == 'eye-off':
            instance.icon_right = 'eye-on'
            instance.password = False
        else:
            instance.icon_right = 'eye-off'
            instance.password = True

    def login(self):
        status = Database.login(email=self.email.text,
                                password=self.password.text)
        print(status)
        if status:
            print('Logged in')
            Database.jsondata(email=self.email.text,
                              password=self.password.text)
            self.manager.add_widget(MainScreen(name='main'))
            self.manager.current = 'main'
        else:
            self.email.error = True
            self.password.error = True
            print('Incorrect Email or password')

    def reg(self):
        self.manager.current = 'registration'


os.environ['OPENAI_API_KEY'] = "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"
os.environ['SERPAPI_API_KEY'] = "edad3081de97572290efcd436f7b82de90f0bef23ccf17de73a283d9d77d1bce"

repo_id = "google/flan-t5-xl"
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bass = False

        self.bass_event = Clock.create_trigger(self.bass_confirmation)

        with self.canvas.before:
            print(self.pos, self.size, Window.size)
            Color(0, 0, 0.3, mode='hex')
            self.rect = Rectangle(texture=Gradient.vertical([0, 0, 0.3, 0.3], [0, 0, 0.5, 0.5], [0, 0, 1, 0.5]),
                                  size=Window.size)
        Window.bind(on_resize=self.resize)
        # global logged_in
        # if logged_in:

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

        # Add cards to card layout
        # self.songs = get_songs_from_database() # Function to get songs from database
        # for song in self.songs:
        # l = ['Jeevamshamayi', 'Chundari Penne', 'Kaliyuga', 'Nangeli Poove', 'Harivarasanam', 'Gulumaal', 'Etho Nidrathan', 'Paathiramazhayetho', 'Thee Minnal', 'Onnam Padimele']
        songs = Database.music(limit=40)
        s1 = songs[:8]
        print(s1)
        s2 = songs[8:16]
        s3 = songs[16:24]
        s4 = songs[24:32]
        s5 = songs[32:]
        for i in s1:
            # songs = Database.music(limit=1)
            # print(songs)
            # if song.section == 'recommended':
            self.card1 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))  # , unfocus_color = (40,40,40,0.1), md_bg_color = (0,0,0,0))
            self.card1.add_widget(Image(source=i[3]))
            self.card1.add_widget(
                MDLabel(text=i[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card1.add_widget(
                MDLabel(text=i[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card1.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.recommended_section.add_widget(self.card1)

        for x in s2:

            # songs = Database.music(limit=1)
            self.card2 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))  # ,  unfocus_color = (40,40,40,0.1))
            self.card2.add_widget(Image(source=x[3]))
            self.card2.add_widget(
                MDLabel(text=x[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card2.add_widget(
                MDLabel(text=x[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card2.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.malayalam_section.add_widget(self.card2)

        for y in s3:

            # songs = Database.music(limit=1)
            self.card3 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))  # ,  unfocus_color = (40,40,40,0.1))
            self.card3.add_widget(Image(source=y[3]))
            self.card3.add_widget(
                MDLabel(text=y[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card3.add_widget(
                MDLabel(text=y[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card3.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.english_section.add_widget(self.card3)

        for z in s4:

            # songs = Database.music(limit=1)
            self.card4 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))  # ,  unfocus_color = (40,40,40,0.1))
            self.card4.add_widget(Image(source=z[3]))
            self.card4.add_widget(
                MDLabel(text=z[1], font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card4.add_widget(
                MDLabel(text=z[2], size_hint=(1, 0.2), font_style='Subtitle2'))
            self.card4.bind(on_release=self.song,
                            on_enter=self.enter, on_leave=self.leave)
            self.hindi_section.add_widget(self.card4)

        for q in s5:

            # songs = Database.music(limit=1)
            self.card5 = MDCard(orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, size_hint_x=1, spacing=dp(5),
                                ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))  # ,  unfocus_color = (40,40,40,0.1))
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
        # self.layout.bind(on_press=self.se)
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

        # self.sub_layout2_1_1.add_widget(MDLabel(text = "Song Name", halign = "left"))
        self.skip_prev = MDIconButton(
            icon='skip-previous', halign="center", disabled=True)
        self.skip_prev.bind(
            on_press=self.previous, on_breh=self.enter, on_leave=self.leave)
        self.sub_layout2_1_1.add_widget(self.skip_prev)
        self.play_pause = MDIconButton(icon='play', halign="center", icon_color=[
            0, 0, 0, 1], theme_icon_color="Custom", md_bg_color="white", disabled=True)
        self.sub_layout2_1_1.add_widget(self.play_pause)
        self.skip_next = MDIconButton(
            icon='skip-next', halign="center", disabled=True)
        self.skip_next.bind(on_press=self.next,
                            on_button_enter=self.enter, on_button_leave=self.leave)
        self.sub_layout2_1_1.add_widget(self.skip_next)
        # self.sub_layout2_1_1.add_widget(MDLabel(text = "Author Name", halign = "left"))

        self.sub_layout5_2 = MDBoxLayout(
            orientation='horizontal', spacing="0.1dp", size_hint_x=0.8, padding="5dp")
        self.sub_layout5.add_widget(self.sub_layout5_2)

        self.start = MDLabel(text="00:00", size_hint_x=0.2,
                             font_style="Subtitle2", halign="right")
        self.sub_layout5_2.add_widget(self.start)
        self.slider = MDSlider(
            size_hint_x=0.7, hint=False)
        # self.slider.set_thumb_icon(path='images/test.png')
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

        self.switch = MDIconButton(icon='music-accidental-double-flat', on_press=lambda x: Thread(
            target=self.booster, name='Song Booster', daemon=True).start())
        # self.switch.bind(on_press = lambda x: Thread(target ))
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
                                   title="Music Player",
                                   right_action_items=[['magnify', lambda x: self.search(), "Search"], ['microphone', lambda x: Thread(target=self.mic_ask(), name='vc_assistant').start()]], pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0
                                   )
        print("Colour:", self.top_bar.md_bg_color)
        self.add_widget(self.top_bar)

        self.nav_drawer = MDNavigationDrawer(
            enable_swiping=True, spacing=dp(25))
        self.nav_menu = MDNavigationDrawerMenu(spacing=dp(35))

        self.nav_header = MDNavigationDrawerHeader(
            title=account[0], text=account[1], title_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_header)

        self.nav_playlist = MDNavigationDrawerItem(
            text='Account', icon="account", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)

        self.nav_playlist = MDNavigationDrawerItem(
            text='Playlist', icon="playlist-music", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_playlist)
        self.nav_playlist.bind(on_release=self.to_playlist,
                               on_enter=self.enter, on_leave=self.leave)

        self.nav_text_art = MDNavigationDrawerItem(
            text='AI Text Art', icon="image-text", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_text_art.bind(on_release=self.to_textart,
                               on_enter=self.enter, on_leave=self.leave)
        self.nav_menu.add_widget(self.nav_text_art)

        self.chatbot = MDNavigationDrawerItem(
            text='Jaadhu', icon="robot", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.chatbot)
        self.chatbot.bind(on_release=self.to_chat,
                          on_enter=self.enter, on_leave=self.leave)

        self.nav_divider = MDNavigationDrawerDivider()
        self.nav_menu.add_widget(self.nav_divider)

        self.nav_settings = MDNavigationDrawerItem(
            text='Enikkariyilla', icon="incognito", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_settings)

        self.nav_settings = MDNavigationDrawerItem(
            text='Settings', icon="tools", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_menu.add_widget(self.nav_settings)

        self.nav_logout = MDNavigationDrawerItem(
            text='Logout', icon="logout", text_color="#FFFFFF", icon_color="#FFFFFF", selected_color="#FFFFFF")
        self.nav_logout.bind(on_release=self.logout,
                             on_enter=self.enter, on_leave=self.leave)
        self.nav_menu.add_widget(self.nav_logout)

        self.nav_rail = MDNavigationRail()
        self.nav_rail.add_widget(MDNavigationRailItem(
            text='python', icon='language-python'))

        self.nav_layout = MDNavigationLayout()
        # self.nav_layout.add_widget(self.nav_rail)
        self.nav_drawer.add_widget(self.nav_menu)
        self.nav_layout.add_widget(self.nav_drawer)
        self.add_widget(
            MDNavigationRail(
                MDNavigationRailItem(
                    text="Python",
                    icon="language-python",
                    # size_hint=(1.2, 1.2)
                ),
                MDNavigationRailItem(
                    text="JavaScript",
                    icon="language-javascript",
                    # size_hint=(1.2, 1.2)
                ),
                MDNavigationRailItem(
                    text="CPP",
                    icon="language-cpp",
                    # size_hint=(1.2, 1.2)
                ),
                MDNavigationRailItem(
                    text="Git",
                    icon="git",
                    # size_hint=(1.2, 1.2)
                ),
                md_bg_color=(1, 0, 0, 0),
                pos_hint={'top': 0.9},
                # size_hint=(0.03, 3),
                # spacing="30dp"
            )
        )
        self.add_widget(self.nav_layout)

    def to_chat(self, dt):
        self.nav_drawer.set_state("close")
        self.manager.current = 'chat'

    def enter(self, instance):
        Window.set_system_cursor(cursor_name='hand')
        instance.elevation = 3

    def leave(self, instance):
        Window.set_system_cursor(cursor_name='arrow')
        instance.elevation = 0

    def resize(self, window, width, height):
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
        # self.manager.get_screen("musicplayer").played_songs.append(
        #    Database.get_song_detail(name=self.song_name))
        self.manager.get_screen("musicplayer").clicked = True

        if self.manager.get_screen("musicplayer").sound and self.manager.get_screen("musicplayer").sn != self.song_name:
            self.manager.get_screen("musicplayer").sound.stop()
        # print(self.play_pause.icon)
       # if self.play_pause and self.counter > 1:
            # print("yes")
            # self.manager.get_screen("musicplayer").play_button.icon == self.play_pause.icon
        self.manager.current = 'musicplayer'

    def next(self, dt):
        self.manager.get_screen("musicplayer").prev_button.disabled = False
        self.skip_prev.disabled = False
        self.manager.get_screen("musicplayer").clicked = False
        self.manager.get_screen("musicplayer").new = True
        self.manager.get_screen("musicplayer").paused = False
        self.manager.get_screen("musicplayer").play_button.icon = 'play'
        self.manager.get_screen("musicplayer").slider.value = 0
        self.manager.get_screen("musicplayer").sound.stop()

    def previous(self, dt):
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
            "musicplayer").played_songs[self.manager.get_screen("musicplayer").index]  # self.played_songs[self.index]

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

    def search(self):
        print(1339013190)
        # self.manager.add_widget(SearchScreen(name='search'))
        self.manager.current = 'search'

    def se(self, instance):
        pass

    def on_pre_enter(self):
        print(Window.size)
        print("Entered Main")
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
            self.mute.disabled = False
            print("Entered Counter")
            self.counter += 1
            print(self.img.source, self.song_image)
            self.img.source = self.song_image
            print("Changed Image")
            self.song_n.text = self.song_name
            self.song_auth.text = self.song_author
            self.end.text = self.convert_seconds_to_min(self.sound.length)
            self.slider.bind(on_touch_up=self.touch_up,
                             on_enter=self.enter, on_leave=self.leave)
            print(self.sound.state)
            self.play_pause.icon = (
                'play' if self.sound.state == 'stop' else 'pause')
            self.play_pause.bind(on_press=self.playpause,
                                 on_enter=self.enter, on_leave=self.leave)
            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)
        # Clock.schedule_once(self.bass == True, 1)

    def booster(self):
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

    def bass_confirmation(self, dt):
        if self.bass == True:
            toast(text="Bass enabled for the current song!", duration=5)
        else:
            toast(text="Bass disabled", duration=5)
        # self.bass = False

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
        val = str(datetime.timedelta(seconds=sec)).split(':')
        return f'{val[1]}:{val[2].split(".")[0]}'

    def playpause(self, dt):
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

    def song_repeat(self, dt):
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

    def mute_func(self, dt):
        if self.sound and self.mute.icon == 'volume-high':
            self.mute.icon = 'volume-variant-off'
            self.mute.theme_icon_color = "Primary"
            # self.mute.icon_color = [0, 0.5, 1, 1]
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
            # toast(text="Sound Enabled", duration=5)
        elif self.sound and self.mute.icon == 'volume-medium':
            self.mute.icon = 'volume-high'
            self.mute.icon_color = [0, 0.5, 1, 1]
            self.mute.theme_icon_color = "Custom"
            self.sound.volume = 1
            # toast(text="Sound Enabled", duration=5)

    def check(self):
        print("Entered")
        if self.song_name != self.prev_sn:
            Clock.schedule_once(self.on_pre_enter)

    def mic_ask(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = pyttsx3.init()
        self.speaker.setProperty("rate", 150)
        # self.speaker.say("Hey what's up")
        # self.speaker.runAndWait()
        try:
            print(0)
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)

                audio = self.recognizer.listen(mic)
                text = self.recognizer.recognize_google(audio).lower()
                print(1, text)

                x = AIChatBot.output(text)
                self.speaker.say(x)
                self.speaker.runAndWait()
        except Exception as e:
            print(e)


class RegistrationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.go_back = MDAnchorLayout(anchor_x="left", anchor_y="top")

        self.back_button = MDRaisedButton(text="Back")
        self.back_button.bind(on_release=lambda x: self.back())
        self.go_back.add_widget(self.back_button)

        self.add_widget(self.go_back)

        self.registration_form = MDBoxLayout(orientation='vertical', size_hint=(
            0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.username = MDTextField(hint_text="Username")
        self.email = MDTextField(hint_text='Email')
        self.phone = MDTextField(hint_text='Phone')
        self.password = MDTextField(hint_text='Password', password=True,
                                    helper_text="Passwords doesnt match", helper_text_mode="on_error")
        self.conf_pass = MDTextField(hint_text='Confirm Password', password=True,
                                     helper_text="Passwords doesnt match", helper_text_mode="on_error")
        self.registration_form.add_widget(self.username)
        self.registration_form.add_widget(self.email)
        self.registration_form.add_widget(self.phone)
        self.registration_form.add_widget(self.password)
        self.registration_form.add_widget(self.conf_pass)

        # Create a register button
        self.register_button = MDRectangleFlatButton(
            text='Register', pos_hint={'center_x': 0.5})
        self.register_button.bind(on_release=self.register)
        self.registration_form.add_widget(self.register_button)

        # Add the registration form to the screen
        self.add_widget(self.registration_form)

    def back(self):
        self.manager.current = 'login'

    def register(self, dt):
        if self.password.text == self.conf_pass.text:
            Database.create_account(
                self.username.text, self.email.text, self.phone.text, self.password.text)
            # Cache.append(category='login_details',
            #             key='username', obj=self.email)
            # Cache.append(category='login_details',
            #             key='password', obj=self.password)
            self.manager.add_widget(MainScreen(name='main'))
            self.manager.current = 'main'
        else:
            self.password.error = True
            self.conf_pass.error = True


class AITextArtScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = False
        self.back_button = MDIconButton(
            icon='chevron-left', pos_hint={'top': 1, 'left': 1})
        self.back_button.bind(on_press=self.go_back)
        self.add_widget(self.back_button)
        self.layout = MDBoxLayout(orientation='vertical')
        self.text_input = MDTextField(mode='round',
                                      multiline=False, size_hint_y=None, height=50, hint_text='Enter text here')
        self.submit_button = MDRectangleFlatButton(
            text='Submit', size_hint_y=None, height=50)
        if self.running == False:
            self.submit_button.bind(on_press=self.generate_image)
        else:
            return
        self.image_space = AsyncImage(
            source="images/gm.png", opacity=0.5, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(self.image_space)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.submit_button)
        self.add_widget(self.layout)

    def generate_image(self, instance):
        API_TOKEN = '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'
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        self.running = True
        text = self.text_input.text
        if not text:
            return
        self.image_space.source = 'images/gi.png'

        response = requests.post(API_URL, headers=headers, json={
            "inputs": text,
        })

        image = Im.open(BytesIO(response.content))
        image.save('generated_image.png')

        self.image_space.source = 'generated_image.png'
        self.image_space.size_hint = (0.3, 0.3)
        self.image_space.opacity = 1
        self.running = False

    def go_back(self, dt):
        self.manager.current = 'main'


class MusicPlayer(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clicked = False
        self.prev = False
        self.stop = False
        self.next_song = []
        # self.previous_song = []
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

    def on_pre_enter(self, *args):
        self.song = Database.get_song_detail(name=self.song_name)
        '''new = Database.music(limit=1)  # [(''Parudeesa', 'author')]
        self.upcoming = new[0]
        print(self.upcoming)'''
        if self.finished == True and self.counter == 0:
            self.manager.get_screen("main").skip_next.disabled = False
            self.manager.get_screen("main").play_pause.disabled = False
            self.clicked = False
            print(1)
            # self.previous_song.append(self.song)
            self.stop = True
            self.counter += 1
            self.sn = self.song[1]
            # print(self.song)
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
            # self.slider.bind(self.set_pos)
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
            # self.layout = MDAnchorLayout(anchor_x = "left", anchor_y = "bottom", md_bg_color = "red", size_hint = (0.1,0.1))
            # self.up = MDLabel(text = f"UPCOMING:\n{self.upcoming[1]}\n{self.upcoming[2]}")
            # self.layout.add_widget(self.up)
            # self.add_widget(self.layout)
            # print(self.up)

        if self.song[1] != self.sn and self.counter > 0:
            print(100)
            self.prev_button.disabled = False
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
            if self.playlist_started == False:
                self.played_songs.append(self.song)
            self.playlist_started = False
            # self.played_songs.append(self.song)

            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)
            self.clicked = False

        else:
            self.play_button.icon = (
                'play' if self.sound.state == 'stop' else 'pause')
            print(self.sn, self.song[1])
            Clock.schedule_interval(self.update_slider, 1)
            Clock.schedule_interval(self.update_time, 1)

    def convert_seconds_to_min(self, sec):
        val = str(datetime.timedelta(seconds=sec)).split(':')
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
        self.prev_button.disabled = False
        self.manager.get_screen("main").skip_prev.disabled = False
        self.clicked = False
        self.new = True
        self.paused = False
        self.play_button.icon = 'play'
        self.slider.value = 0
        self.sound.stop()

    def previous(self, dt):
        self.clicked = False
        self.prev = True
        self.new = True
        self.index -= 1
        print("#######################", self.index, -(len(self.played_songs)))
        if self.index == -(len(self.played_songs)):
            print("OKKK")
            self.prev_button.disabled = True
        else:
            self.prev_button.disabled = False
        print(self.prev_button.disabled)
        print(self.played_songs)
        print("Index:", self.index)
        song = self.played_songs[self.index]

        # self.new = True
        # self.next_song.insert(0, Database.get_song_detail(name = self.sn))
        self.paused = False
        self.play_button.icon = 'play'
        self.sound.stop()
        self.slider.value = 0
        Clock.unschedule(self.update_slider)
        Clock.unschedule(self.update_time)
        # print("On previous:", self.previous_song)
        # self.previous_song = Database.get_song_detail(name = self.sn)
        print(self.sn)
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

        # notification.notify(app_icon = None, title = self.song_title.text, app_name = "Music Player",
        # message = self.song_author.text, timeout = 10, toast = False)

    def on_stop(self, dt):
        if self.manager.get_screen("main").bass == True:
            self.manager.get_screen(
                "main").switch.theme_icon_color = "Primary"

        if self.manager.get_screen("main").repeat.icon == 'repeat':
            self.manager.get_screen("main").repeat.icon = 'repeat-off'
            self.manager.get_screen("main").repeat.theme_icon_color = "Primary"

        print("PAUSED", self.paused)
        print("SLIDER VALUE", self.slider.value)
        print("PREV", self.prev)
        print("CLICKED", self.clicked)
        print("NEW", self.new)
        print("INDEX", self.index)
        print("ALREADY STARTED", self.already_started)
        print(self.played_songs)
        print("QUEUED SONGS", self.queue_songs)
        print("PLAYLIST", self.playlist)
        print("QUEUE", self.queue)

        if self.index != -1 and self.prev == False and self.paused == False and self.playlist == False and self.queue == False and self.playlist_started == False:
            print(
                1000000000000000000000000000000000000000000000000000000000000000000000000000000)
            Clock.unschedule(self.update_slider)
            Clock.unschedule(self.update_time)
            self.new = False
            self.index += 1
            song = self.played_songs[self.index]
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
            MainScreen.on_pre_enter

        elif self.paused == False and (self.slider.value > 98.5 or self.new == True) and self.prev == False and self.clicked == False:
            # True and (False or True) and True and True
            # True and True and True and True
            # True
            print(
                1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111)
            self.clicked = False
            self.paused = False
            self.play_button.icon = 'play'
            self.manager.get_screen('main').skip_prev.disabled = False
            self.prev_button.disabled = False
            Clock.unschedule(self.update_slider)
            Clock.unschedule(self.update_time)
            self.new = False

            if self.already_started != True:
                print(1111111111111111111111111155555555555555555555555555)
                song = Database.music(limit=1)
                print("On stop:", song)
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

            '''if self.queue != False:
                print(
                    1111111112222222222222222222222222222222222222222222222222222222222222222222)
                if len(self.queue_songs) != 0:
                    self.played_songs.append(self.queue_songs[0])
                    # if len(self.queue_songs) != 1:
                    #    self.previous_song = self.queue_songs[0]
                    self.sn = self.queue_songs[0][1]

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
                    self.queue_songs.pop(0)
                    if len(self.queue_songs) == 0:
                        self.queue_songs = []
                        self.queue = False

            elif self.playlist:
                print(self.playlist_songs)
                if self.playlist_songs != None and len(self.playlist_songs) != 0 and self.already_started == False:
                    print(
                        1111111111111111111333333333333333333333333333333333333333333333333)
                    # if len(self.playlist_songs) != 1:
                    self.played_songs.append(self.playlist_songs[0])
                    self.sn = self.playlist_songs[0][1]

                    self.bg_image.source = self.playlist_songs[0][3]+'-bg.png'
                    self.song_title.text = self.playlist_songs[0][1]
                    self.song_author.text = self.playlist_songs[0][2]
                    self.song_image.source = self.playlist_songs[0][3]

                    self.sound = SoundLoader.load(self.playlist_songs[0][4])
                    self.start_time.text = "00:00"
                    self.end_time.text = self.convert_seconds_to_min(
                        self.sound.length)
                    self.sound.play()
                    self.sound.bind(on_stop=self.on_stop)
                    self.play_button.icon = 'pause'
                    self.play_button.bind(on_press=self.play_pause)

                    Clock.schedule_interval(self.update_slider, 1)
                    Clock.schedule_interval(self.update_time, 1)
                    self.playlist_songs.pop(0)
                    if len(self.playlist_songs) == 0:
                        self.playlist_songs = None
                        self.playlist = False
                else:
                    print(111111111111111111444444444444444444444444444444444)
                    song = Database.music(limit=1)
                    print("On stop:", song)
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
                    Clock.schedule_interval(self.update_time, 1)'''

            self.manager.get_screen("main").sound = self.sound
            self.manager.get_screen("main").is_playing = self.paused
            self.manager.get_screen("main").song_name = self.song_title.text
            self.manager.get_screen("main").song_n.text = self.song_title.text
            print(self.manager.get_screen(
                "main").song_n.text, self.song_title.text)
            self.manager.get_screen("main").song_author = self.song_author.text
            self.manager.get_screen(
                "main").song_auth.text = self.song_author.text
            self.manager.get_screen("main").song_image = self.song_image.source
            self.manager.get_screen("main").img.source = self.song_image.source
            print(self.manager.get_screen(
                "main").song_image, self.song_image.source)
            self.manager.get_screen(
                "main").end.text = self.convert_seconds_to_min(self.sound.length)
            MainScreen.on_pre_enter

            self.stop = True
        self.already_started = False

        if self.manager.get_screen('main').sound != None:
            vol = {'volume-high': 1, 'volume-variant-off': 0,
                   'volume-low': 0.15, 'volume-medium': 0.5}
            self.m_icon = self.manager.get_screen(
                'main').mute.icon  # volume-variant-off
            self.manager.get_screen('main').sound.volume = vol[self.m_icon]

        # notification.notify(app_icon = None, title = self.song_title.text, app_name = "Music Player",
        #                    message = self.song_author.text, timeout = 10, toast = False)

        # elif self.new == True:
        #    self.new = False
        #    self.stop = True

    def update_slider(self, dt):
        self.slider.value = (self.sound.get_pos() / self.sound.length) * 100

    def update_time(self, dt):
        total_seconds = int(self.sound.get_pos())
        current_minute = total_seconds // 60
        current_seconds = total_seconds - (current_minute * 60)
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
        self.manager.current = self.prev_screen  # 'main'


class BassBoost():
    global attenuate_db
    global accentuate_db
    attenuate_db = -10
    accentuate_db = 10

    def bass_line_freq(track):
        sample_track = list(track)

        est_mean = np.mean(sample_track)

        est_std = 3 * np.std(sample_track) / (math.sqrt(2))

        bass_factor = int(round((est_std - est_mean) * 0.005))

        return bass_factor

    def audio(path):
        sample = AudioSegment.from_mp3(path)
        filtered = sample.low_pass_filter(
            BassBoost.bass_line_freq(sample.get_array_of_samples()))

        combined = (sample - attenuate_db).overlay(filtered + accentuate_db)
        combined.export("D:\\Music Player App\\" +
                        path[20:].replace(".mp3", "") + "-boosted.mp3", format="mp3")

        print("Done")


class SearchScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.song_id = None

        self.new_songs = Clock.create_trigger(self.new)  # self.new_songs()

        self.songs = Database.music(limit=27)

        self.back = MDIconButton(
            icon='chevron-left', pos_hint={'top': 1, 'left': 0.85})
        self.add_widget(self.back)
        self.back.bind(on_press=self.go_back)

        self.search_bar = MDTextField(mode='fill', hint_text='Search', icon_left='magnify',
                                      pos_hint={'top': 0.95, 'center_x': 0.5}, size_hint=(0.9, 0.2),
                                      background_color="yellow", fill_color_focus="white", fill_color_normal="grey",
                                      hint_text_color_normal="white", icon_left_color_normal="white", text_validate_unfocus=False)
        self.add_widget(self.search_bar)
        self.search_bar.bind(text=self.updating)
        # self.search_bar.bind(on_text_validate=self.update_suggestion)

        self.scroll = MDScrollView(pos_hint={'top': 0.9}, do_scroll_x=False, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=20,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)

        self.list = MDList()
        self.scroll.add_widget(self.list)

        for i in self.songs:
            self.sugg_songs = TwoLineAvatarIconListItem(IconRightWidget(
                id=f"{i[0]},{i[1]}", icon='dots-vertical', on_press=self.dropdown), ImageLeftWidget(source=i[3]), text=i[1], secondary_text=i[2])
            self.list.add_widget(self.sugg_songs)
            self.sugg_songs.bind(on_release=self.musicplayer)

       # self.menu.open()

        # self.list.add_widget(MDLabel(text='gaga\ngagaga\ngagagag\nagagagagaga', size_hint = (2,2)))

    def on_pre_enter(self):
        self.account = Database.acc_details()[0]
        self.plays = Database.playlists_info(username=self.account)
        print(self.plays)

    def updating(self, instance, value):
        print('ho')
        self.search_text = self.search_bar.text
        Thread(target=self.update_list, name='search', daemon=True).start()

    def update_list(self):
        print("Entering update list")
        print(self.search_text)

        if self.search_text != '':
            # t1 = time.time()
            print(1111111111)
            text = self.search_text
            # print(time.time()-t1)
            print(66666)

            self.filtered_items = Database.song_match(text)
            print(9999999999999)
            # print(time.time()-t1)
            self.new_songs()

            '''if len(self.filtered_items) > 0:
                for it in self.filtered_items:
                    self.sugg_songs = TwoLineAvatarIconListItem(IconRightWidget(
                        id=f"{it[0]},{it[1]}", icon='dots-vertical', on_press=self.dropdown), ImageLeftWidget(source=it[3]), text=it[1], secondary_text=it[2])
                    self.list.add_widget(self.sugg_songs)
                    self.sugg_songs.bind(on_release=self.musicplayer)
            print(891243)'''
        else:
            self.filtered_items = []
            self.new_songs()

        # if len(filtered_items) > 0 and len(self.search_bar.text) > 0:
        #    self.search_bar.hint_text = filtered_items[0][1]
        # if len(self.search_bar.text) == 0:
        #    self.search_bar.hint_text = "Search"

    def new(self, dt):
        # print(len(self.filtered_items))
        try:
            if len(self.filtered_items) > 0:
                self.list.clear_widgets()
                for it in self.filtered_items:
                    self.sugg_songs = TwoLineAvatarIconListItem(IconRightWidget(
                        id=f"{it[0]},{it[1]}", icon='dots-vertical', on_press=self.dropdown), ImageLeftWidget(source=it[3]), text=it[1], secondary_text=it[2])
                    self.list.add_widget(self.sugg_songs)
                    self.sugg_songs.bind(on_release=self.musicplayer)
            else:
                print("Clearing")
                self.list.clear_widgets()
        except:
            self.list.clear_widgets()

    '''def update_suggestion(self, instance):
        if len(self.search_bar.text) != 0 and self.search_bar.hint_text != "Search":
            self.search_bar.text = self.search_bar.hint_text
            self.search_bar.hint_text = "Search"'''

    def go_back(self, dt):
        self.manager.current = 'main'

    def musicplayer(self, instance):
        self.song_name = instance.text
        print(self.song_name)
        self.manager.get_screen("musicplayer").song_name = self.song_name
        self.manager.get_screen('musicplayer').playlist = False
        self.manager.get_screen('musicplayer').playlist_songs = None
        self.manager.get_screen('musicplayer').prev_screen = 'search'
        self.manager.get_screen("musicplayer").clicked = False
        self.manager.get_screen('musicplayer').new = True

        if self.manager.get_screen("musicplayer").sound and self.manager.get_screen("musicplayer").sn != self.song_name:
            self.manager.get_screen("musicplayer").sound.stop()

        self.manager.current = 'musicplayer'

    def dropdown(self, instance):
        detail = instance.id.split(',')
        print(detail, detail[1])
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
        # print(self.sugg_songs.children)
        self.menu = MDDropdownMenu(
            caller=instance,
            items=self.menu_items,
            width_mult=4)
        self.menu.open()
        print("opened")

    def playlists(self):
        # self.scroll2 = MDScrollView(pos_hint = {'top':0.95}, height = "200dp")
        self.box = MDBoxLayout(
            size_hint_y=None, orientation='vertical', adaptive_height=True)
        # self.scroll2.add_widget(self.box)
        print(self.plays)
        for k in self.plays:
            # print(k)
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

    def queue(self):
        self.song_info = Database.get_song_detail(id=int(self.song_id))
        self.manager.get_screen('musicplayer').queue = True
        self.manager.get_screen(
            'musicplayer').queue_songs.append(self.song_info)
        toast(text="Song Added To Queue")

    def select_playlist(self, instance):
        Database.add_playlist_song(playlist_id=int(
            instance.id), song_id=int(self.song_id), song_name=self.name_of_song)
        self.dialog.dismiss()
        toast(text="Song Added To Playlist")


class Playlist(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.prev_len = 0
        self.deleted = False

    def go_to_main(self, dt):
        self.manager.current = 'main'

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

    def choose(self, dt):
        self.play_img = filechooser.open_file()
        # print(self.play_img, self.play_img[0])
        try:
            self.upload.background_normal = self.play_img[0]
            print(self.play_img[0], self.upload.background_normal)
        except:
            toast(text="Unable to load image")

    def cancel(self, dt):
        self.dialog.dismiss()

    def create(self, dt):
        print(self.upload.state)
        if self.play_n.text != '' and self.upload.state == 'normal' and len(self.play_n.text) <= 30:
            today = date.today()
            t = today.strftime("%d/%m/%Y")
            Database.create_playlist(
                name=self.play_n.text, image=(
                    self.upload.background_normal if self.upload.background_normal != 'images/upload.png' else 'images/no img.png'),
                user=self.username, date=t
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
            print(self.play_name_new.text, self.img_new.source,
                  self.username, self.play_date_new.text)
            # Database.create_playlist(
            #    name=self.play_name_new.text, image=self.play_img[0], user=self.username, date=self.play_date_new.text)
            self.dialog.dismiss()
            toast(text="Playlist Created")

    def on_pre_enter(self):
        self.account = Database.acc_details()
        self.username = self.account[0]
        self.playlists = Database.playlists_info(username=self.username)
        print(self.playlists)
        self.prev_len = len(self.playlists)  # 3
        print(self.deleted)

        if self.counter == 0 or self.deleted == True:  # True or False -> True
            print("OKAKAKAKAKAAAAAA", self.deleted)
            self.counter += 1
            if self.deleted:
                self.clear_widgets()
            self.back = MDIconButton(
                icon='chevron-left', pos_hint={'top': 1, 'left': 0.95})
            self.back.bind(on_press=self.go_to_main)
            self.add_widget(self.back)

            self.head = MDLabel(text="Playlists", pos_hint={
                                'top': 0.95, 'right': 0.53}, bold=True, font_style="H3", size_hint=(0.5, 0.1))
            self.add_widget(self.head)

            self.scroll = MDScrollView(size_hint=(0.9, 0.87), pos_hint={'top': 0.87, 'right': 0.95}, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                       always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
            self.add_widget(self.scroll)

            self.sub_layout = MDStackLayout(
                spacing="30dp", adaptive_height=True, width=dp(1000), padding="20dp")
            self.scroll.add_widget(self.sub_layout)

            for i in range(len(self.playlists)):
                self.card = MDCard(id=str(self.playlists[i][0]), orientation='vertical', md_bg_color=(
                    1, 1, 1, 1), height="350dp", width="300dp", size_hint=(None, None), spacing="10dp", padding="20dp")
                self.sub_layout.add_widget(self.card)
                # print(self.card.id)
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

            self.create_play = MDFloatingActionButton(
                icon='plus', pos_hint={'top': 0.1, 'right': 0.95}, elevation=5, icon_size="35dp")
            self.add_widget(self.create_play)
            self.create_play.bind(on_release=self.play_details)
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
            self.clear_widgets()
            self.back = MDIconButton(
                icon='chevron-left', pos_hint={'top': 1, 'left': 0.95})
            self.back.bind(on_press=self.go_to_main)
            self.add_widget(self.back)

            self.head = MDLabel(text="Playlists", pos_hint={
                                'top': 0.95, 'right': 0.53}, bold=True, font_style="H3", size_hint=(0.5, 0.1))
            self.add_widget(self.head)

            self.scroll = MDScrollView(size_hint=(0.9, 0.87), pos_hint={'top': 0.87, 'right': 0.95}, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                       always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
            self.add_widget(self.scroll)

            self.sub_layout = MDStackLayout(
                spacing="30dp", adaptive_height=True, width=dp(1000), padding="20dp")
            self.scroll.add_widget(self.sub_layout)

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

            self.create_play = MDFloatingActionButton(
                icon='plus', pos_hint={'top': 0.1, 'right': 0.95}, elevation=5, icon_size="35dp")
            self.add_widget(self.create_play)
            self.create_play.bind(on_release=self.play_details)

    def playlist_songs(self, instance):
        try:
            print("TRYING", instance.id)
            self.manager.get_screen(
                "playlist_songs").playlist_id = int(instance.id)
            print(1)
            self.manager.get_screen(
                "playlist_songs").bg_img = instance.children[2].source
            self.manager.get_screen(
                "playlist_songs").play_name = instance.children[1].text
            print(2)
            self.manager.get_screen(
                "playlist_songs").play_date = instance.children[0].text
            self.manager.current = 'playlist_songs'
        except:
            print("EXCEPTION", self.card_new.id)
            self.manager.get_screen(
                "playlist_songs").playlist_id = int(self.card_new.id)
            self.manager.get_screen(
                "playlist_songs").bg_img = self.img_new.source
            self.manager.get_screen(
                "playlist_songs").play_name = self.play_name_new.text
            self.manager.get_screen(
                "playlist_songs").play_date = self.play_date_new.text
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
        self.clear_widgets()
        self.songs = Database.playlist_songs(
            id=self.playlist_id, order_by="created")

        self.song_infos = []
        for i in self.songs:
            self.song_info = Database.get_song_detail(id=i[1])
            self.song_infos.append(self.song_info)

        self.hex = self.colour_extractor(self.bg_img)

        '''x = add(1,2)
        print(x)'''

        with self.canvas:
            Color(0.5, 0.5, 0.5,
                  mode='hex')
            print(self.hex)
            self.bg_grad = Rectangle(texture=Gradient.vertical(get_color_from_hex(self.hex[1]), get_color_from_hex(self.hex[0])),
                                     pos=[0, -8], size=[1920, 1080])

        self.bar = MDTopAppBar(title=self.play_name, md_bg_color=(1, 0, 0, 0), left_action_items=[
                               ["arrow-left", lambda x: self.go_back(), 'back']], pos_hint={'top': 1}, elevation=0, anchor_title="left")
        self.add_widget(self.bar)

        self.scroll = MDScrollView(pos_hint={'top': 0.93}, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)

        self.main = MDBoxLayout(orientation='vertical', spacing="1dp",
                                size_hint_y=None, adaptive_height=True, padding=[0, 0, 0, 100])
        self.scroll.add_widget(self.main)

        self.layout = MDBoxLayout(orientation='horizontal', pos_hint={
                                  'top': 0.95}, size_hint_y=None, height="300dp", size_hint_x=0.4, spacing="2dp")
        self.main.add_widget(self.layout)
        self.layout_sub = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="100dp", size_hint_x=0.33, padding=[
                                      0, 0, 200, 0], pos_hint={'center_x': 0.2}, spacing="20dp")
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
            self.delete_song.bind(on_press=self.confirm_playlist_song_deletion)
            self.card.add_widget(self.delete_song)

    def musicplayer(self, instance):
        self.index = int(instance.children[6].text)
        self.manager.get_screen('musicplayer').playlist = False  # True
        print("PLAYLIST INDEX", self.index)
        print("PLAYLIST SONGS:", self.song_infos)
        self.new_index = self.manager.get_screen('musicplayer').index

        try:
            self.manager.get_screen(
                'musicplayer').playlist_songs = self.song_infos[self.index::]
            for i in self.song_infos:
                self.manager.get_screen(
                    'musicplayer').played_songs.insert(self.new_index+1, i)
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

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def colour_extractor(self, path):
        color_thief = ColorThief(path)
        palette = color_thief.get_palette(color_count=2)
        l = []

        for i in palette:
            l.append(self.rgb_to_hex(i))

        return l

    def confirm_playlist_deletion(self, dt):
        self.main = MDBoxLayout(orientation="vertical",
                                spacing="5dp",
                                size_hint_y=None,
                                size_hint_x=None,
                                width="300dp",
                                height="50dp")
        # self.upload = Button(background_normal='images/upload.png', on_press=self.choose,
        #                     size_hint_x=0.7, background_down='images/loading.png')
        # self.main.add_widget(self.upload)

        # self.play_n = MDTextField(
        #    hint_text="Playlist Name",
        #    pos_hint={'center_y': 0.5},
        #    max_text_length=30,
        #    helper_text_mode='on_error'
        # )
        self.confirm = MDLabel(text="Are You Sure?",
                               size_hint_x=2, bold=True, font_style="H5")
        self.main.add_widget(self.confirm)

        self.note = MDLabel(text="Note: This will delete the whole playlist")
        self.main.add_widget(self.note)

        # self.main.add_widget(self.play_n)
        self.dialog = MDDialog(
            # title="Are You Sure?",
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

    def confirm_playlist_song_deletion(self, instance):
        self.main = MDBoxLayout(orientation="vertical",
                                spacing="5dp",
                                size_hint_y=None,
                                size_hint_x=None,
                                width="300dp",
                                height="50dp")
        # self.upload = Button(background_normal='images/upload.png', on_press=self.choose,
        #                     size_hint_x=0.7, background_down='images/loading.png')
        # self.main.add_widget(self.upload)

        # self.play_n = MDTextField(
        #    hint_text="Playlist Name",
        #    pos_hint={'center_y': 0.5},
        #    max_text_length=30,
        #    helper_text_mode='on_error'
        # )
        self.confirm = MDLabel(text="Are You Sure?",
                               size_hint_x=2, bold=True, font_style="H5")
        self.main.add_widget(self.confirm)

        # self.note = MDLabel(text="Note: This will delete the whole playlist")
        # self.main.add_widget(self.note)

        # self.main.add_widget(self.play_n)
        self.dialog = MDDialog(
            # title="Are You Sure?",
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

    def delete_playlist(self, dt):
        Database.delete_playlist(self.playlist_id)
        self.dialog.dismiss()
        self.manager.get_screen('playlist').deleted = True
        self.manager.current = 'playlist'
        toast(text="Playlist Deleted")

    def song_delete(self, instance):
        Database.delete_playlist_song(self.playlist_id, int(instance.id))
        self.layout2.clear_widgets()
        self.songs = Database.playlist_songs(id=self.playlist_id)

        self.song_infos = []
        for i in self.songs:
            self.song_info = Database.get_song_detail(id=i[1])
            print(self.song_info)
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

    def sort_on_name(self, dt):
        self.layout2.clear_widgets()
        if self.icon2.icon == 'sort-alphabetical-ascending':
            sort = 'song_name DESC'
            self.icon2.icon = 'sort-alphabetical-descending'
        else:
            sort = 'song_name ASC'
            self.icon2.icon = 'sort-alphabetical-ascending'
        self.songs = Database.playlist_songs(
            id=self.playlist_id, order_by=sort)
        print(self.songs)

        self.song_infos = []
        for i in self.songs:
            self.song_info = Database.get_song_detail(id=i[1])
            print(self.song_info)
            self.song_infos.append(self.song_info)
        print(self.song_infos)

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
        print(self.songs)

        self.song_infos = []
        for i in self.songs:
            self.song_info = Database.get_song_detail(id=i[1])
            print(self.song_info)
            self.song_infos.append(self.song_info)
        print(self.song_infos)

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

    def confirm_playlist_rename(self, dt):

        # self.rename_layout = MDBoxLayout(orientation="horizontal",
        #                                 spacing="12dp",
        #                                 size_hint_y=None,
        #                                 height="200dp")

        self.rename_layout = MDTextField(
            hint_text="New Playlist Name",
            pos_hint={'center_y': 0.5, },
            max_text_length=30,
            helper_text_mode='on_error'
        )

        # self.main.add_widget(self.play_n)
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

    def rename_playlist(self, dt):
        if self.rename_layout.text != '' and len(self.rename_layout.text) <= 30:
            Database.playlist_edit(
                playlist_id=self.playlist_id, rename=self.rename_layout.text)
            self.song_name.text = self.rename_layout.text
            self.bar.title = self.rename_layout.text
            self.play_name = self.rename_layout.text
            self.dialog.dismiss()

    def confirm_playlist_image(self, dt):

        self.upload_layout = MDBoxLayout(
            orientation='vertical', size_hint_y=None, height="200dp", width="25dp")

        self.upload = Button(background_normal='images/upload.png',
                             on_press=self.choose, background_down='images/loading.png')
        self.upload_layout.add_widget(self.upload)

        self.dialog = MDDialog(
            title="Create Playlist",
            type="custom",
            auto_dismiss=False,
            content_cls=self.upload_layout,
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

    def choose(self, dt):
        self.play_img = filechooser.open_file()
        # print(self.play_img, self.play_img[0])
        try:
            self.upload.background_normal = self.play_img[0]
            print(self.play_img[0], self.upload.background_normal)
        except:
            toast(text="Unable to load image")

    def image_edit_playlist(self, dt):
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

    def go_back(self):
        print(self.manager.transition.direction)
        self.manager.transition.direction = 'right'
        self.manager.current = 'playlist'
        self.manager.transition.direction = 'left'


class ChatUI(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 1
        self.list = []
        self.change = False

        with self.canvas.before:
            self.rect = Rectangle(texture=Gradient.vertical(get_color_from_hex('#EBC7E6'),
                                                            get_color_from_hex(
                                                                '#BFACE2'),
                                                            get_color_from_hex(
                                                                '#A084DC'),
                                                            get_color_from_hex('#645CBB')), size=Window.size)
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
        print(1)

        print(2)

        self.text = MDLabel(text="Heya my friend welcome to the nameless Music Player App. How can I help you today?", size_hint=(
            1, 1), bold=True, font_style="H4", italic=True, valign='top', padding=[15, 0], height="100dp", halign='left', markup=True)
        # self.text.add_widget(ImageLeftWidget(source='images/test.png'))
        self.card.add_widget(self.text)

        if len(self.text.text) > 178:
            if '\n' in self.text.text:
                count = self.text.text.count('\n')
                self.card.height = f"{(len(self.text.text)/178)*110 * count/count-1.5}dp"
            else:
                self.card.height = f"{(len(self.text.text)/178)*110}dp"

        self.text_input = MDTextField(
            mode='fill', hint_text="Send a message", pos_hint={
                'center_x': 0.5, 'top': 0.1}, size_hint=(None, None), size=(1700, 400), multiline=True, radius=(30, 30, 30, 30))  # fill_color_normal=[192, 192, 192, 0.5])
        self.add_widget(self.text_input)
        self.text_input.add_widget(ScrollView())
        self.list.append(self.text_input.pos)

        self.send_button = MDIconButton(icon='send', md_bg_color="blue", pos_hint={
            'center_x': 0.93, 'top': 0.10})
        self.send_button.bind(on_press=self.send_user_message)
        self.add_widget(self.send_button)

    def go_back(self, dt):
        self.manager.current = 'main'

    def send_user_message(self, dt):
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
        self.upload2 = Button(background_normal='images/no img.png',
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

    def get_texture_size(self, dt):
        print(self.text2.padding)
        self.card2.height = self.text2.texture_size[1] + \
            2*self.text2.padding[1]

    def move(self, dt):
        Window.set_system_cursor(cursor_name='hand')

    def leave(self, dt):
        Window.set_system_cursor(cursor_name='arrow')

    def get_ai_message(self):
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

    def send_ai_message(self, dt):

        self.counter += 1
        self.sub_layout5 = MDBoxLayout(
            padding=[8, 3, 2, 3],
            orientation='horizontal', size_hint=(None, None), adaptive_height=True, spacing="50px", width="1800dp"
        )
        self.sub_layout.add_widget(self.sub_layout5)

        self.upload = Button(background_normal='images/ai.jpg',
                             size_hint=(None, None), background_down='images/loading.png', valign='center', border=(0, 0, 0, 0), pos_hint={'top': 0.9})

        self.sub_layout5.add_widget(self.upload)
        self.card = MDCard(size_hint=(None, None), style='elevated',
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
            # self.sound = SoundLoader.load(f"music/{value[1]}.mp3")
            # self.sound.play()
            # self.manager.current = "box"
            Clock.schedule_once(self.musicplayer)

    def ai_texture_size(self, dt):
        print(self.text.text_size)
        if '\n' in self.text.text:
            self.card.height = self.text.texture_size[1] + \
                2*self.text.padding[1]
        else:
            if len(self.text.text) > 178:
                self.card.height = f"{(len(self.text.text)/178)*110}dp"

    def resize(self, window, width, height):
        self.rect.size = Window.size

    def Window_Size(self):
        return Window.size

    def musicplayer(self, dt):
        self.manager.get_screen('musicplayer').new = True
        self.manager.get_screen('musicplayer').prev_screen = 'chat'
        self.manager.get_screen(
            "musicplayer").song_name = self.value[1]
        self.manager.get_screen("musicplayer").clicked = True
        if self.manager.get_screen("musicplayer").sound and self.manager.get_screen("musicplayer").sn != self.value[1]:
            self.manager.get_screen("musicplayer").sound.stop()
        self.manager.current = 'musicplayer'


class AIChatBot():
    global agent_chain
    global new_memory
    global conversation
    global memory_list
    global memory
    global screen_change
    global song_name
    global author
    memory_list = []
    counter = 0
    screen_change = False
    song_name = None
    author = None

    dburl = 'mysql+pymysql://root:@localhost/musicplayer'
    db = SQLDatabase.from_uri(dburl)

    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
        ),
        Tool(
            name="get song details",
            func=lambda text: AIChatBot.sqloutput(text),
            description="strictly use it when user wants to listen to a song. The Final Answer should be a message saying 'playing song'"
        ),
        WriteFileTool(),
        ReadFileTool(),
        MoveFileTool()
    ]

    prefix = "You are Aeris, A multifunctional chatbot that tends to user's queries"

    memory = ConversationBufferMemory(
        memory_key="chat_history")
    llm = ChatOpenAI(temperature=0,
                     model="gpt-3.5-turbo-0613", max_tokens=1000)
    # )'''
    agent_chain = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, early_stopping_method='generate',
                                   verbose=True, agent_kwargs={'prefix': prefix}, max_iterations=5)  # , memory=memory)  # agent_kwargs={'prefix': prefix, 'suffix': suffix, 'input_variables': ['input', 'chat_history', 'agent_scratchpad']}, memory=memory)

    def output(text):
        global screen_change
        screen_change = False
        output = agent_chain.run(input=text)
        if output.startswith("egnahc_neercs:"):
            output.remove("egnahc_neercs:")
        print(screen_change)
        print(output)

        return output

    def output3():
        return (screen_change, song_name, author)

    def output4(value: bool):
        global screen_change
        screen_change = value
        print(screen_change)
        return screen_change

    def sqloutput(text):
        db = SQLDatabase.from_uri(
            'mysql+pymysql://root:@localhost/musicplayer', sample_rows_in_table_info=10)
        llm = ChatOpenAI(temperature=0.1, model='gpt-3.5-turbo-0613')
        agent = SQLDatabaseSequentialChain.from_llm(llm=llm,  # llm_chain=LLMChain(llm=HuggingFaceHub(repo_id='google/flan-t5-xl', model_kwargs={"temperature": 0, "max_length": 4096})),
                                                    database=db, return_direct=True)
        out = agent.run(text)
        y = ast.literal_eval(out)
        print(y)
        if len(y) == 0 or len(y[0]) == 0:
            return "Couldnt fetch the required song"
        elif len(y[0]) == 7:
            x = y[0][1]
            AIChatBot.song_infos(y[0][1], y[0][2])
        else:
            x = y[0][0]
            AIChatBot.song_infos(y[0][0], y[0][1])

        return f"Song {x} being played successfully"

    def song_infos(name_of_song: str, author_of_song: str):
        global song_name
        global author
        global screen_change
        song_name = name_of_song
        author = author_of_song
        screen_change = True


class Settings(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VoiceAssistant():
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = pyttsx3.init()
        self.speaker.setProperty("rate", 150)

        while True:
            try:
                print(0)
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)

                    audio = self.recognizer.listen(mic)
                    text = self.recognizer.recognize_google(audio).lower()
                    print(1, text)

                    if "alexa" in text:
                        audio2 = self.recognizer.listen(mic)
                        text2 = self.recognizer.recognize_google(
                            audio2).lower()
                        print(2, text2)

                        if text2 is not None:
                            print(3, text2)
                            self.speaker.say(text2)
                            self.speaker.runAndWait()
            except Exception as e:
                print(e)
                continue


class spotify(MDApp):
    def build(self):

        Database.connect()
        self.icon = 'images/bheeshma parvam.jpg'
        self.title = "Music Player"
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_hue = '500'
        # self.theme_cls.primary_palette = "Blue"
        sm = MDScreenManager()
        # sm.add_widget(Welcome(name='welcome'))

        sm.add_widget(WelcomeScreen(name=''))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(AITextArtScreen(name='aiart'))
        sm.add_widget(MusicPlayer(name='musicplayer'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(Playlist(name='playlist'))
        sm.add_widget(Playlist_Songs(name='playlist_songs'))
        sm.add_widget(ChatUI(name='chat'))
        # Thread(target=self.hello, name="Voice Assistant")
        return sm

    def hello(self):
        print("hello")


if __name__ == '__main__':
    spotify().run()
