from datetime import datetime as dt
from kivymd.uix.spinner.spinner import MDSpinner
from kivy.core.text import LabelBase
from kivy.factory import Factory
from kivy.lang import Builder
from infi.systray import SysTrayIcon
import win32con
import winreg
import ctypes
from wallpaper import set_wallpaper
import azapi
from googletrans import Translator
from lyrics_extractor import SongLyrics
import lyricsgenius
from langchain.chains import SQLDatabaseSequentialChain
from langchain import HuggingFaceHub
import ast
from langchain.tools import StructuredTool
from langchain.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
import pyjokes
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.prompts.chat import BaseMessagePromptTemplate
from langchain.prompts.base import BasePromptTemplate
from langchain.agents import OpenAIFunctionsAgent, StructuredChatAgent
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.agents import LLMSingleActionAgent
from langchain import LLMChain
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
import faiss
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import VectorStoreRetrieverMemory
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from datetime import datetime
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import Tool
from kivymd.uix.behaviors import HoverBehavior
import random
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
from kivymd.uix.toolbar.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screenmanager import ScreenManager, MDScreenManager
from kivymd.uix.transition.transition import MDSwapTransition
from kivymd.app import MDApp
from kivymd.uix.screen import Screen, MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.label.label import MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.video import Video
from kivymd.theming import ThemeManager
from kivymd.uix.gridlayout import MDGridLayout
from kivy.graphics import Color
from kivy.animation import Animation
from kivymd.toast import toast
from kivy.graphics.vertex_instructions import Rectangle, RoundedRectangle
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
from kivymd.uix.list.list import MDList, TwoLineAvatarIconListItem, TwoLineRightIconListItem, ImageRightWidget, ImageLeftWidget, IconRightWidget, TwoLineIconListItem, IconLeftWidget, TwoLineListItem
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
from kivy.clock import _default_time as __time
import time
from kivymd.uix.stacklayout import MDStackLayout
from plyer import filechooser
from datetime import date
from colorthief import ColorThief
from PIL import Image as Im
from kivymd.uix.menu import MDDropdownMenu
from PIL import Image as Im
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pandas as pd
import openai
import subprocess
import os
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_csv_agent
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.memory import ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from kivy.core.window import WindowBase
from kivy_garden.frostedglass import FrostedGlass

from langchain.utilities import SerpAPIWrapper
from kivymd.uix.navigationrail import (
    MDNavigationRail,
    MDNavigationRailMenuButton,
    MDNavigationRailFabButton,
    MDNavigationRailItem,
)
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.pickers import MDColorPicker, MDTimePicker
from kivy.uix.colorpicker import ColorPicker
import asynckivy as ak
from kivymd.uix.filemanager.filemanager import MDFileManager
from kivymd.uix.sliverappbar.sliverappbar import MDSliverAppbar, MDSliverAppbarContent, MDSliverAppbarHeader
from kivy.graphics.vertex_instructions import Ellipse
from kivymd.uix.imagelist.imagelist import MDSmartTile


class testing2(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_widget(MDLabel(text='haii'))
        self.add_widget(MDIconButton(icon='switch', on_press=self.go_back))

    def go_back(self, dt):
        self.manager.current = 'testing'


class testing3(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas.before:
            Color(1, 1, 1, mode='rgb')
            self.user_image = Ellipse(
                source='images/ai.jpg', size=(248, 248), pos=(130, 750))

        self.sub_layout1 = MDBoxLayout(
            orientation='vertical', pos_hint={'center_x': 0.73, 'top': 0.9}, size_hint_y=0.15)
        self.add_widget(self.sub_layout1)

        self.username = MDLabel(text="The King", font_style="H3", bold=True)
        self.sub_layout1.add_widget(self.username)

        self.email = MDLabel(text="abc@gmail.com", font_style="H6", bold=True)
        self.sub_layout1.add_widget(self.email)

        self.infos = MDLabel(
            text="2 Playlists | Joined On 23/12/2023", font_style="Subtitle1", bold=True)
        self.sub_layout1.add_widget(self.infos)

        self.scroll = MDScrollView(do_scroll_x=False, pos_hint={'top': 0.65}, size_hint_y=0.9, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)

        self.sub_layout3 = MDBoxLayout(
            orientation='horizontal', size_hint_x=1, spacing="20dp")
        self.sub_layout1.add_widget(self.sub_layout3)

        self.icon1 = MDIconButton(icon='rename-outline', pos_hint={
                                  'top': 1}, icon_size='23sp', md_bg_color=[0, 1, 1, 0.5])
        self.sub_layout3.add_widget(self.icon1)
        self.icon2 = MDIconButton(icon='image-edit-outline', pos_hint={
                                  'top': 1}, icon_size='23sp', md_bg_color=[0, 1, 1, 0.5])
        self.sub_layout3.add_widget(self.icon2)

        self.main_layout = MDBoxLayout(
            orientation='vertical', size_hint_y=None, height="700dp", spacing="10dp", padding=[0, 10, 0, 0])
        # self.main_layout = MDFloatLayout(size_hint_y=None)
        self.scroll.add_widget(self.main_layout)

        self.sub_layout2 = MDGridLayout(
            size_hint_y=5, size_hint_x=0.4, cols=3, spacing="35dp", padding="25dp", pos_hint={'center_x': 0.25, 'top': 0.7})
        self.label1 = MDLabel(
            text='Most Played Songs', font_style='H3', size_hint_y=None, height="25dp", bold=True, pos_hint={'center_x': 0.545, 'top': 1})
        self.main_layout.add_widget(self.label1)
        self.main_layout.add_widget(self.sub_layout2)

        l = [[214/255, 175/255, 54/255, 0.75], [167/255, 167 /
                                                255, 173/255, 0.75], [167/255, 112/255, 68/255, 0.75]]
        for i in range(3):
            # orientation="vertical", height="250dp", padding=dp(4), size_hint_y=None, spacing=dp(5),
            self.card = MDSmartTile(radius=30, box_radius=[0, 0, 30, 30], size_hint_x=None, width="420dp", box_color=l[i],  # box_color=get_color_from_hex(l[i]),
                                    lines=2, height="375dp", size_hint_y=None, source='images/Kaduva.jpeg')
            # ripple_behavior=True, focus_behavior=True, elevation=0, focus_color=(31, 31, 31, 0.15))  # , unfocus_color = (40,40,40,0.1), md_bg_color = (0,0,0,0))
            # self.card.add_widget(FitImage(source='images/ai.jpg'))
            self.songs_authors = TwoLineListItem(_no_ripple_effect=True, pos_hint={'center_y': 0.5},
                                                 text='[size=25][b]What Makes You Beautiful[/b][/size]', secondary_text='[b]Vineeth Sreenivasan, Vaikom Vijayalakshmi[/b]')
            self.card.add_widget(self.songs_authors)
            '''self.card.add_widget(
                MDLabel(text="AI Songs", font_style='Subtitle1', bold=True, size_hint=(1, 0.2)))
            self.card.add_widget(
                MDLabel(text="AI Authors", size_hint=(1, 0.2), font_style='Subtitle2'))
            self.sub_layout2.add_widget(self.card)'''
            self.sub_layout2.add_widget(self.card)

        self.app_bar = MDTopAppBar(left_action_items=[['arrow-left', lambda x: self.go_back(), "back"]],
                                   title="Profile",
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0)

        self.add_widget(self.app_bar)
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

    def hey(self, dt):
        print("hey")


class reg_screen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LabelBase.register(name='mercy',
                           fn_regular='fonts/Mercy Christole.ttf')

        with self.canvas.before:
            Color(1, 1, 1, mode='hex')
            self.rect = Rectangle(texture=Gradient.horizontal(get_color_from_hex('#7F7FD5'), get_color_from_hex('#91EAE4')),
                                  # source='images/ai.jpg',
                                  size=Window.size)
        Window.bind(on_resize=self.resize)
        self.md_bg_color = [0, 0, 0, 0]
        self.username = "Eternity"

        # self.layout = MDBoxLayout(orientation='vertical', pos_hint={'top': 1})
        # self.add_widget(self.layout)

        self.img = Image(source='images/Chorduce icon.png',
                         size_hint=(0.1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.95})
        self.add_widget(self.img)

        self.animation1 = Animation(size_hint=(
            0.5, 0.5), duration=5.0, transition='in_out_bounce', pos_hint={'center_x': 0.5, 'center_y': 0.5}) + Animation(size_hint=(0.3, 0.3), duration=2, pos_hint={
                'center_x': 0.5, 'center_y': 0.55}, transition='out_quad')
        self.animation1.bind(
            on_complete=self.loading)
        self.animation1.start(self.img)

    def loading(self, anim, widget):
        self.spinner = MDSpinner(size_hint=(0.025, 0.025), pos_hint={'center_x': 0.5, 'center_y': 0.3}, palette=[
            [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
            [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
            [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
            [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
        ])
        self.animation2 = Animation(size_hint=(
            0.32, 0.32), duration=1)+Animation(size_hint=(0.3, 0.3), duration=1)
        self.animation2.repeat = True
        self.animation2.start(self.img)
        part = self.times_of_day(dt.now().hour)
        self.add_widget(self.spinner)

        self.label = MDLabel(text=f"[font=mercy]Good {part}, {self.username}[/font]", pos_hint={
                             'center_x': 0.5, 'center_y': 0.84}, bold=True, font_style='H1', halign='center', italic=True, markup=True, size_hint=(3, 3))
        self.add_widget(self.label)

    def times_of_day(self, h):
        return (
            "Morning"
            if 1 <= h < 12
            else "Afternoon"
            if 12 <= h < 17
            else "Evening"
        )

    def resize(self, window, width, height):
        self.rect.size = Window.size


class testing(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas.before:
            print(self.pos, self.size, Window.size)
            Color(0, 0, 0.3, mode='hex', group=u'color')
            self.rect = Rectangle(texture=Gradient.vertical([0, 0, 0.3, 0.3], [0, 0, 0.5, 0.5], [0, 0, 1, 0.5]),
                                  size=(1920, 1080), group=u"rect")

        self.sleep_time = None

        print(1111)

        self.scroll = MDScrollView(do_scroll_x=False, pos_hint={'top': 0.93}, size_hint_y=0.9, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)

        self.main_layout = MDBoxLayout(
            orientation='vertical', size_hint_y=None, adaptive_height=True, spacing="10dp", padding="20dp")
        self.scroll.add_widget(self.main_layout)

        self.sub_layout1 = MDBoxLayout(
            orientation='vertical', size_hint_y=None, adaptive_height=True, spacing="10dp", padding="20dp")
        self.main_layout.add_widget(self.sub_layout1)

        self.label1 = MDLabel(text="Background Settings",
                              font_style='H4', bold=True, pos_hint={'center_x': 0.545})
        self.sub_layout1.add_widget(self.label1)

        self.list = MDList(pos_hint={'center_x': 0.5}, size_hint_x=0.9)

        self.listitem1 = TwoLineRightIconListItem(
            text="App Background Colour",
            secondary_text='Switch between Dark and Light Modes',
        )
        self.listitem1icon = IconRightWidget(
            icon='white-balance-sunny', on_press=self.dark_light)
        self.listitem1.add_widget(self.listitem1icon)
        self.sub_layout1.add_widget(self.list)
        self.list.add_widget(self.listitem1)

        self.listitem2 = TwoLineRightIconListItem(
            text="App Primary Colour",
            secondary_text="Choose App Primary Colour"
        )
        self.listitem2icon = IconRightWidget(
            icon='format-color-fill', on_press=self.change_primary_color)
        self.listitem2.add_widget(self.listitem2icon)
        self.list.add_widget(self.listitem2)

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

        self.listitem4 = TwoLineRightIconListItem(
            text='Set Main Screen Image', secondary_text="Add an image as the background for the mainscreen"
        )
        self.list2.add_widget(self.listitem4)

        self.listitem4icon = IconRightWidget(
            icon='file', on_press=self.filechoose)
        self.listitem4.add_widget(self.listitem4icon)

        self.listitem5 = TwoLineRightIconListItem(
            text='Set Music Wallpaper', secondary_text="Changes the wallpaper of the desktop according to song image"
        )
        self.listitem5icon = IconRightWidget(
            icon='toggle-switch-off', on_press=self.change_wallpaper, icon_size='43sp'
        )
        self.list2.add_widget(self.listitem5)
        self.listitem5.add_widget(self.listitem5icon)

        self.listitem7 = TwoLineRightIconListItem(
            text='TaskBar Player', secondary_text='Enable/Disable the mini player in the taskbar'
        )
        self.listitem7icon = IconRightWidget(
            icon='toggle-switch-off', on_press=self.taskbar_player, icon_size='40sp'
        )
        self.list2.add_widget(self.listitem7)
        self.listitem7.add_widget(self.listitem7icon)

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

        self.app_bar = MDTopAppBar(left_action_items=[['arrow-left', lambda x: self.go_back(), "back"]],
                                   title="Settings",
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0, opposite_colors=False)
        self.add_widget(self.app_bar)
        print(222)

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

    def ai_recommendations(self, dt):
        if self.listitem6icon.icon == 'toggle-switch':
            self.listitem6icon.icon = 'toggle-switch-off'
            toast("Turned off Assistant Recommendations")
        else:
            self.listitem6icon.icon = 'toggle-switch'
            toast("Turned On Assistant Recommendations")

    def filechoose(self, dt):
        if self.listitem4icon.icon == 'file':
            self.img = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path,
                                     preview=True, ext=['.png', 'jpg', '.jpeg'], icon_folder='folder-transparent.jpg', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
            self.img.show(os.path.expanduser("~"))
        else:
            print(self.canvas.children)
            with self.canvas.before:
                self.canvas.before.remove_group(u'img')
                self.canvas.before.remove_group(u'img_color')
                # self.canvas.before.remove_group(u'img')
                # self.rect.source = None

                Color(0, 0, 0.3, mode='hex')
                # self.rect.texture = Gradient.vertical(
                #    [0, 0, 0.3, 0.3], [0, 0, 0.5, 0.5], [0, 0, 1, 0.5])
                self.rect = Rectangle(texture=Gradient.vertical([0, 0, 0.3, 0.3], [0, 0, 0.5, 0.5], [0, 0, 1, 0.5]),
                                      size=(1920, 1080))
                # self.rect.texture = Gradient.vertical(
                #    [0, 0, 0.3, 0.3], [0, 0, 0.5, 0.5], [0, 0, 1, 0.5])
            toast("Removed Image")
            self.listitem4icon.icon = 'file'

    def select_path(self, path: str):

        self.exit_manager()
        toast("New Image Has Been Set As Background")
        with self.canvas.before:
            self.canvas.before.remove_group(u'color')
            Color(1, 1, 1, mode='rgb', group=u'img_color')
            self.canvas.before.remove_group(u'rect')
            # self.rect.texture = None
            # self.rect.source = path
            self.rect = Rectangle(source=path, size=(1920, 1080), group=u'img')

        self.listitem4icon.icon = 'toggle-switch'

    def exit_manager(self, *args):
        self.img.close()

    def dark_light(self, dt):
        if self.listitem1icon.icon == 'white-balance-sunny':
            self.listitem1icon.icon = 'moon-waxing-crescent'
            self.theme_cls.theme_style = "Light"
        else:
            self.listitem1icon.icon = 'white-balance-sunny'
            self.theme_cls.theme_style = "Dark"

    def change_primary_color(self, dt):
        picker = MDColorPicker(size_hint=(0.51, 0.51),
                               pos_hint={
            'center_x': 0.5, 'center_y': 0.5})
        picker.open()

    def time_pick(self, dt):
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

    def get_time(self, instance, time):
        self.sleep_time = time

    def check_time(self, dt):
        c = datetime.datetime.now()
        current_time = c.strftime('%H:%M:%S')

        if str(self.sleep_time) != current_time:
            return
        else:
            Clock.unschedule(self.check_time)
            self.listitem3icon.icon = 'timer-off'
            toast("App Will Close in 10 seconds")
            Clock.schedule_once(lambda x: MDApp.get_running_app().stop(), 10)

    def change_wallpaper(self, dt):
        if self.listitem5icon.icon == 'toggle-switch-off':
            FILL, FIT, STRETCH, TILE, CENTER, SPAN = 0, 1, 2, 3, 4, 5
            MODES = (0, 10), (0, 6), (0, 2), (1, 0), (0, 0), (0, 22)
            value1, value2 = MODES[FIT]  # choose mode here

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Control Panel\Desktop", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "TileWallpaper", 0,
                              winreg.REG_SZ, str(value1))
            winreg.SetValueEx(key, "WallpaperStyle", 0,
                              winreg.REG_SZ, str(value2))
            winreg.CloseKey(key)

            ctypes.windll.user32.SystemParametersInfoW(
                20, 0, rf"D:\Music Player App\images\Godha.jpeg", 0)
            self.listitem5icon.icon = 'toggle-switch'
        else:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Control Panel\Desktop", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "TileWallpaper", 0,
                              winreg.REG_SZ, str(0))
            winreg.SetValueEx(key, "WallpaperStyle", 0,
                              winreg.REG_SZ, str(10))
            winreg.CloseKey(key)

            ctypes.windll.user32.SystemParametersInfoW(
                20, 0, rf"C:\Users\pc\Documents\sample_pic.jpg", 0)
            self.listitem5icon.icon = 'toggle-switch-off'

    def taskbar_player(self, dt):
        if self.listitem7icon.icon == 'toggle-switch-off':
            menu_options = (
                ("Say Hello", 'hey', lambda x: print("Hello World")),)
            self.systray = SysTrayIcon(
                "icon.ico", "Example tray icon", menu_options)
            self.systray.start()
            self.listitem7icon.icon = 'toggle-switch'
        else:
            self.systray.shutdown()
            self.listitem7icon.icon = 'toggle-switch-off'

    def notif_config(self, dt):
        if self.listitem8icon.icon == 'toggle-switch-off':
            self.listitem8icon.icon = 'toggle-switch'
        else:
            self.listitem8icon.icon = 'toggle-switch-off'

    def user_data(self, dt):
        with open(rf'C:\Users\pc\Desktop\EuphoniusUserData.txt', 'a') as f:
            f.write('User Data for you')
            toast("User Data Downloaded")

    def go_back(self):
        self.manager.current = 'back'


class testing4(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.not_found = False

        self.scroll_view = MDScrollView(do_scroll_x=False, pos_hint={'top': 0.93, 'center_x': 0.4}, size_hint_y=0.9, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                        always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll_view)

        self.top_bar = MDTopAppBar(left_action_items=[['chevron-down', lambda x: self.go_back()],],
                                   title="Music Player",
                                   # ['microphone', lambda x: Thread(target=self.mic_ask(), name='vc_assistant').start()]],
                                   # right_action_items=[['magnify', lambda x: self.search(), "Search"]],  # [
                                   # 'tools', lambda x: spotify.open_settings]],
                                   pos_hint={'top': 1.0},
                                   md_bg_color=[1, 0, 0, 0],
                                   anchor_title='left',
                                   elevation=0
                                   )
        self.add_widget(self.top_bar)

        genius = lyricsgenius.Genius('IGWgsLHybP3wO96mxe-sH-TUiTNOEKXB8SS1udS4TMuk_ovQUJ74-IkGc9s-1EkhZ5MfsjL5sfc-8ih_SqAmYA',
                                     skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"],
                                     remove_section_headers=True)

        try:
            API = azapi.AZlyrics('google', accuracy=0.5)

            API.artist = 'Jakes Bejoy'
            API.title = 'Kalapakkaara'

            API.getLyrics(save=False)

            lyrics = API.lyrics
            if lyrics != '':
                self.not_found = False
            else:
                breh = 1/0
        except:
            try:
                print("Searching")
                x = 1/0
                song = genius.search_song('Ba', 'asda')
                print("Found")
                genius.response_format = 'markdown'
                lyrics = song.lyrics
                self.not_found = False
                print(lyrics)
            except:
                try:
                    extract_lyrics = SongLyrics(
                        'AIzaSyCEDrw4PLZvE0iEhoYo6FpNq_QqgofLWfs', 'd34c8f76177674713')

                    data = extract_lyrics.get_lyrics(
                        "Jeevamshamayi By K. S. Harisankar, Shreya Ghoshal Lyrics")
                    lyrics = data['lyrics']
                    print(lyrics)
                    self.not_found = False
                except:
                    self.not_found = True

        if self.not_found != True:
            '''translator = Translator()
            lyrics = translator.translate(lyrics)
            print(lyrics)'''

            self.label = MDLabel(text=f"{lyrics}", font_style='H3', padding=(400, 0, 0, 0), bold=True, font_name='fonts/ArialUnicodeMS',
                                 size_hint=(None, None), width="1800dp", halign='left', pos_hint={'center_x': 0.2}, markup=True, allow_copy=True, allow_selection=True)
            self.scroll_view.add_widget(self.label)
            Clock.schedule_once(self.lyric_height)

    def lyric_height(self, dt):
        print(self.label.texture_size)
        self.label.height = self.label.texture_size[1]


class MainApp(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.5
        # self.theme_cls.primary_hue = '500'
        # self.theme_cls.primary_palette = "Blue"
        self.sm = MDScreenManager()
        # sm.add_widget(testing(name='testing'))
        # sm.add_widget(testing2(name='back'))
        self.sm.add_widget(reg_screen(name='user'))
        return self.sm

    def stopping_method(self):
        MDApp.get_running_app().stop()
        Window.close()

    def on_stop(self):
        try:
            self.sm.get_screen('user').systray.shutdown()
        except:
            pass
# code to print all numbers from 1 to 1000?
# code to print all integers


MainApp().run()
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex



MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "MDNavigationRail"
        md_bg_color: rail.md_bg_color
        left_action_items: [["menu", lambda x: app.rail_open()]]

    MDBoxLayout:

        MDNavigationRail:
            id: rail
            md_bg_color: get_color_from_hex("#344954")
            color_normal: get_color_from_hex("#718089")
            color_active: get_color_from_hex("#f3ab44")
            use_resizeable: True

            MDNavigationRailItem:
                icon: "language-cpp"
                text: "[b]My Custom Item 1[/b]"

            MDNavigationRailItem:
                icon: "language-python"
                text: "[b]My Custom Item 2[/b]"

            MDNavigationRailItem:
                icon: "language-swift"
                text: "[b]My Custom Item 3[/b]"

        MDBoxLayout:
            padding: "24dp"

            ScrollView:

                MDList:
                    id: box
                    cols: 3
                    spacing: "12dp"
'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def rail_open(self):
        if self.root.ids.rail.rail_state == "open":
            self.root.ids.rail.rail_state = "close"
        else:
            self.root.ids.rail.rail_state = "open"


# Test().run()

'''from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.screen import MDScreen


class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return MDScreen(
            MDTopAppBar(
                id="toolbar",
                md_bg_color=(1, 0, 0, 0),
                pos_hint={"top": 1},
                title='TopAppBar',
                elevation=0,
                right_action_items=[
                    ["dots-vertical", lambda x: print(1)],
                    ["clock", lambda x: print(2)],
                ],
                anchor_title="left",
            ),
            MDLabel(
                text='Label',
                halign='center',
                font_style='H4',
            )
        )

    def on_start(self):
        self.root.ids.toolbar.specific_text_color = "white"


MainApp().run()'''
