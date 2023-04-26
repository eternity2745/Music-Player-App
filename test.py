import os
# os.environ["KIVY_VIDEO"] = "python-vlc"
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
from kivy.uix.actionbar import ActionView, ActionOverflow, ActionBar, ActionButton, ActionPrevious
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


class Settings(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scroll = MDScrollView(size_hint_x=0.7, pos_hint={'top': 0.95, 'center_x': 0.5}, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0])
        self.add_widget(self.scroll)
        self.main = MDBoxLayout(
            size_hint_y=None, orientation='vertical', adaptive_height=True)
        self.scroll.add_widget(self.main)

        for i in range(20):
            self.item = TwoLineRightIconListItem(
                text="Single-line item with avatar", secondary_text="Secondary text here")
            self.main.add_widget(self.item)

        self.main.add_widget(MDLabel(size_hint_y=2, text=""))


class Test(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.primary_palette = "Blue"

        self.sm = MDScreenManager()
        self.sm.add_widget(Settings(name='settings'))
        return self.sm
        # self.fps_monitor_start()


if __name__ == '__main__':
    Test().run()
