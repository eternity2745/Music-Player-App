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
from kivymd.uix.list.list import MDList, TwoLineAvatarIconListItem, TwoLineRightIconListItem, ImageRightWidget, ImageLeftWidget, IconRightWidget, TwoLineIconListItem, IconLeftWidget
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

from typing import Union

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.pickers import MDColorPicker

KV = '''
MDScreen:

    MDTopAppBar:
        id: toolbar
        title: "MDTopAppBar"
        pos_hint: {"top": 1}

    MDRaisedButton:
        text: "OPEN PICKER"
        pos_hint: {"center_x": .5, "center_y": .5}
        md_bg_color: toolbar.md_bg_color
        on_release: app.open_color_picker()
'''


class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def open_color_picker(self):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color,
            on_release=self.get_selected_color,
        )

    def update_color(self, color: list) -> None:
        self.root.ids.toolbar.md_bg_color = color

    def get_selected_color(
        self,
        instance_color_picker: MDColorPicker,
        type_color: str,
        selected_color: Union[list, str],
    ):
        '''Return selected color.'''

        print(f"Selected color is {selected_color}")
        self.update_color(selected_color[:-1] + [1])

    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        '''Called when a gradient image is clicked.'''


MyApp().run()
