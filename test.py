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

os.environ['OPENAI_API_KEY'] = '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'


class ChatBox(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.scroll = MDScrollView()
        # self.add_widget(self.scroll)

        self.main_layout = MDBoxLayout(orientation='vertical')
        self.add_widget(self.main_layout)

        # self.sub_layout1 = MDBoxLayout(
        #    orientation='vertical', adaptive_size=True, size_hint=(None, None))
        # self.main_layout.add_widget(self.sub_layout1)

        self.sub_layout1 = MDFloatLayout(size=(1920, 1080))
        self.main_layout.add_widget(self.sub_layout1)

        # self.user_card = MDCard(radius=10, md_bg_color=[
        #    1, 1, 1, 1], pos_hint={'center_x': 0.8, 'top': 0.9}, size_hint=(0.2, 0.1))
        # self.sub_layout1.add_widget(self.user_card)
        # self.text = MDLabel(text="Hello there my name is Aaron. What's your name? Well it works almost well i dont know how it will be handling large texts.",
        #                    pos=(1200, 750), size_hint=(None, None), text_color=(0, 0.2, 1, 1), theme_text_color="Custom", font_style="H4",
        #                    bold=True, italic=True, halign='center', valign='top',
        # outline_color=(0, 0, 1, 1),
        # outline_width=11)
        # height="50dp",
        # width="500dp"

        #                    )
        # self.text.height = self.text.texture_size[1]
        # print(self.text.texture_size)
        # self.sub_layout1.add_widget(self.text)

        # self.text.width = len(self.text.text) * 17.24
        # self.text.height = self.text.width/10
        # if self.text.width > 690:
        #    self.text.width = 690
        #    self.text.adaptive_height = True

        # print(self.text.text_size)

        # with self.text.canvas.before:
        #    Color(0, 1, 0.5)
        #    x = self.text.size
        #    y = x[0]
        #    z = x[1]
        #    print(len(self.text.text))
        #    if self.text.adaptive_height == True:
        #        z = x[1] - (len(self.text.text) / 1.5)
        #    print(self.text.size)
        #    RoundedRectangle(size=(x[0]+10, z),
        #                     pos=self.text.pos, radius=[43, 43, 0, 43])
        self.sub_layout2 = MDBoxLayout(
            pos=(1250, 100),
            size_hint=(None, None),
            adaptive_size=True,
            padding=[500, 30, 10, 50],
            spacing="20px"
        )
        self.main_layout.add_widget(self.sub_layout2)

        self.text_input = MDTextField(
            mode='fill', hint_text="Send a message", pos=(1080, 20), size_hint=(None, None), size=(1000, 200), fill_color_normal=[192, 192, 192, 0.5])
        self.sub_layout2.add_widget(self.text_input)

        self.send_button = MDIconButton(icon='send', md_bg_color="blue")
        self.send_button.bind(on_press=self.send)
        self.sub_layout2.add_widget(self.send_button)

    def send(self, dt):
        self.t = self.text_input.text
        self.text = MDLabel(text=self.t,
                            pos=(1200, 750), size_hint=(None, None), text_color=(0, 0.2, 1, 1), theme_text_color="Custom", font_style="H4",
                            bold=True, italic=True, halign='center', valign='top',
                            # outline_color=(0, 0, 1, 1),
                            # outline_width=11),
                            height="50dp",
                            width="500dp"

                            )
        # self.text.height = self.text.texture_size[1]
        # print(self.text.texture_size)
        self.sub_layout1.add_widget(self.text)

        self.text.width = len(self.text.text) * 17.24
        self.text.height = self.text.width/9
        if self.text.width > 690:
            self.text.width = 690
            self.text.adaptive_height = True

        print(self.text.text_size)

        with self.text.canvas.before:
            Color(0, 1, 0.5)
            x = self.text.size
            y = x[0]
            z = x[1]
            print(len(self.text.text))
            if self.text.adaptive_height == True:
                z = x[1] - (len(self.text.text) / 1.5)
            print(self.text.size)
            RoundedRectangle(size=(x[0]+10, z),
                             pos=self.text.pos)  # , radius=[23, 23, 0, 23])


class ChatterBox(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = 1

        self.layout = MDCard(size_hint=(1, 0.1), pos_hint={
            'center_x': 0.5, 'bottom': 1}, md_bg_color=(0, 0, 0, 1), elevation=3)
        self.add_widget(self.layout)

        self.sub_layout2 = MDBoxLayout(
            size_hint=(None, None),
            adaptive_size=True,
            padding=[500, 30, 10, 50],
            spacing="20px"
        )
        self.layout.add_widget(self.sub_layout2)

        self.text_input = MDTextField(
            mode='fill', hint_text="Send a message", pos=(1080, 20), size_hint=(None, None), size=(1000, 200), fill_color_normal=[192, 192, 192, 0.5])
        self.sub_layout2.add_widget(self.text_input)

        self.send_button = MDIconButton(icon='send', md_bg_color="blue")
        self.send_button.bind(on_press=self.send_user_message)
        self.sub_layout2.add_widget(self.send_button)

        self.scroll = MDScrollView(do_scroll_x=False, pos_hint={'top': 0.95}, size_hint_y=0.84, scroll_wheel_distance=5, scroll_type=['bars', 'content'], smooth_scroll_end=75,
                                   always_overscroll=False, bar_margin=0.5, bar_width=7, bar_inactive_color=[0, 0, 0, 0], background_hue='100')
        self.add_widget(self.scroll)

        self.main_layout = MDBoxLayout(
            orientation='vertical', size_hint_y=None, adaptive_height=True, width="1920dp", spacing="20dp")
        self.scroll.add_widget(self.main_layout)

        # self.sub_layout1 = MDFloatLayout(
        #    size_hint_y=None, adaptive_height=True, width="50dp")
        # self.scroll.add_widget(self.sub_layout1)

        self.welcome_card = MDCard(radius=[23, 23, 23, 0], md_bg_color=[
            1, 1, 1, 1], pos_hint={'center_x': 0.2, 'top': 0.9}, size_hint=(0.25, None), height="100dp", padding=[10, 3, 2, 2])
        self.main_layout.add_widget(self.welcome_card)

        self.welcome_text = MDLabel(text="Hello there nice to meet you my friend how are you? you amHello there nice to meet you my friend how are you? you am", size_hint=(
            1, 1), bold=True, font_style="H4", halign='left', italic=True, valign='top')
        self.welcome_card.add_widget(self.welcome_text)

        if len(self.welcome_text.text) > 58:
            self.welcome_card.height = f"{(len(self.welcome_text.text)/58)*100}dp"

        # if len(self.ai_response.text) > 58:
        #    self.ai_response.size_hint_y = (
        #        len(self.ai_response.text)/58) / 10

        # self.user_card = MDCard(radius=10, md_bg_color=[1, 1, 1, 1], pos_hint={
        #    'center_x': 0.8, 'top': 0.7}, size_hint=(0.25, 0.1), padding=[10, 3, 2, 2])
        # self.main_layout.add_widget(self.user_card)

        # self.user_ask = MDLabel(text="Hello there nice to meet you my friend how are you? you am there nice to meet you my friend how are you? you am", size_hint=(
        #    1, 1), bold=True, font_style="H4", halign='left', italic=True, valign='top')
        # self.user_card.add_widget(self.user_ask)

        # if len(self.user_ask.text) > 58:
        #    self.user_card.size_hint_y = (len(self.user_ask.text)/58) / 10

    def send_user_message(self, dt):
        self.counter += 1
        self.text = self.text_input.text
        # self.main_layout.height = f"{self.counter*175}dp"
        self.text_input.text = ''
        self.text_input.disabled = True
        self.send_button.disabled = True

        self.user_card = MDCard(radius=[23, 23, 0, 23], md_bg_color=[1, 1, 1, 1], pos_hint={
            'center_x': 0.8, 'top': 0.7}, size_hint=(0.25, None), height="100dp", padding=[10, 3, 2, 2])
        self.main_layout.add_widget(self.user_card)

        self.user_ask = MDLabel(text=self.text, size_hint=(
            1, 1), bold=True, font_style="H4", halign='left', italic=True, valign='top')
        self.user_card.add_widget(self.user_ask)

        if len(self.user_ask.text) > 58:
            self.user_card.height = f"{(len(self.user_ask.text)/58)*100}dp"

        Clock.schedule_once(self.send_ai_message)

    def send_ai_message(self, dt):
        self.counter += 1
       # self.main_layout.height = f"{self.counter*175}dp"
        self.ai_text = AIChatBot.output(text=self.user_ask.text)
        self.ai_card = MDCard(radius=[23, 23, 23, 0], md_bg_color=[
            1, 1, 1, 1], pos_hint={'center_x': 0.2, 'top': 0.9}, size_hint=(0.25, None), height="100dp", padding=[10, 3, 2, 2])
        self.main_layout.add_widget(self.ai_card)

        self.ai_response = MDLabel(text=self.ai_text, size_hint=(
            1, 1), bold=True, font_style="H4", halign='left', italic=True, valign='top')
        self.ai_card.add_widget(self.ai_response)

        if len(self.ai_response.text) > 58:
            self.ai_card.height = f"{(len(self.ai_response.text)/58)*100}dp"

        print(self.main_layout.height)

        self.text_input.disabled = False
        self.send_button.disabled = False


class AIChatBot:
    global conversation
    global new_memory
    template = """
    You are a fun chatbot in a music player app and helps user's with their queries.
    You're name is Aeris.

    Context:
    {entities}

    Current conversation:
    {history}
    Last line:
    Human: {input}
    You:
    """

    llm = OpenAI(temperature=0.3, max_tokens=156)
    # agent = create_csv_agent(llm=llm, path='test.csv', verbose=False)
    # memory = ConversationEntityMemory(llm=llm)
    # llm = HuggingFaceHub(repo_id='google/flan-t5-xl',
    #                     model_kwargs={"temperature": 0, "max_length": 512})
    new_memory = ConversationEntityMemory(llm=llm)
    conversation = ConversationChain(
        memory=new_memory, llm=llm, prompt=PromptTemplate(input_variables=['entities', 'history', 'input'], template=template))
    # onversation.add_agent(agent)

    def output(text):
        output = conversation.run(input=text)
        new_memory.save_context(
            {'inputs': text},
            {'outputs': output}

        )
        return output


class Test(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.primary_palette = "Blue"

        self.sm = MDScreenManager()
        self.sm.add_widget(ChatterBox(name='chat'))
        return self.sm
        # self.fps_monitor_start()


if __name__ == '__main__':
    Test().run()
