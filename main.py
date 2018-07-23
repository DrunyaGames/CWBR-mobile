__version__ = '1.0'

import codecs
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import *  # ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.clock import mainthread, Clock
from kivy.core.audio import SoundLoader
from client import Client
from classes import User, Cat, Collection
from editable_lable import EditableLabel
from time import sleep
from traceback import print_exc
import os

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '854')

client = Client()

fileobj = codecs.open('cat_main.kv', 'r', 'utf_8_sig')
text = fileobj.read()
fileobj.close()

Builder.load_string(text)
main_theme = SoundLoader.load('main_theme.mp3')


class CatCollectionImage(Image):
    pass


class UserDataInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = substring.replace(' ', '').replace('\t', '')
        return super().insert_text(s, from_undo=from_undo)


class ImageButton(ButtonBehavior, Image):
    pass


class BoxButton(ButtonBehavior, BoxLayout):
    orientation = 'vertical'


class MinerButton(ImageButton):
    is_mining = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_texture()

    def send_data(self):
        client.send('mine_new_cat', {'mode': 'easy'})
        game_menu.update_texture()

    @mainthread
    def update_texture(self):
        if self.is_mining:
            self.source = 'textures/buttons/full_bowl.png'
            self.is_mining = False
        else:
            self.source = 'textures/buttons/empty_bowl.png'
            self.is_mining = True

    @staticmethod
    @client.handle('new_cat')
    def get_answer(**cat):
        new_cat = Cat(cat)
        collection.collection.append(new_cat)
        cs.update_collection()
        game_menu.update_texture()


class CatCollectionButton(BoxButton):
    cat_id = None

    @mainthread
    def __init__(self, cat, **kwargs):
        super().__init__(**kwargs)

        self.ids.cat_power.text = f'СИЛА: {cat.power}'
        self.ids.cat_image.source = cat.path
        self.ids.cat_name.text = cat.name
        self.cat_id = cat.id

    def change_cat_name(self):
        if self.cat_id != None:
            print(self.cat_id, self.ids.cat_name.text)
            client.send('change_cat_name', {'name': self.ids.cat_name.text, 'cat_id': self.cat_id})


class CollectionLayout(GridLayout):
    widgets = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))
        self.update_collection()

    def add_cat(self, cat):
        self.widgets.append(CatCollectionButton(cat, size_hint_y=None, height=140))
        sleep(0.1)
        self.add_widget(self.widgets[-1])

    def show_cats(self):
        print('AAA', self.widgets)  # DO NOT ERASE
        # for i in self.widgets:
        # sleep(0.1)
        # self.add_widget(i)

    def update_collection(self):
        for i in self.widgets:
            self.remove_widget(i)
            sleep(0.1)
        self.widgets = []
        for cat in collection.collection:
            sleep(0.1)
            self.add_cat(cat)
        # self.show_cats()


class SignInScreen(Screen):
    username = ''
    password = ''

    def callback(self):
        print(self.username)
        print(self.password)
        self.send_data()

    def send_data(self):
        client.send('auth', {'name': self.username, 'password': self.password})

    @staticmethod
    @client.handle('auth_ok')
    def get_answer(user_id, name, rights, cats, session):
        collection.create_collection(cats)
        sm.current = 'gamemenu'
        cs.update_collection()
        main_theme.play()


class SignUpScreen(Screen):
    username = ''
    password = ''
    sec_password = ''
    popup = Popup(title='ERROR',
                  content=Label(text='Пароли не совпадают!'),
                  size_hint=(0.4, 0.2))

    def callback(self):
        if self.password == self.sec_password:
            print(self.username)
            print(self.password)
            self.send_data()
        else:
            self.popup.open()

    def send_data(self):
        client.send('reg', {'name': self.username, 'password': self.password})

    @staticmethod
    @client.handle('reg_ok')
    def get_answer(user_id, name, rights, cats, session):
        print('okk')
        sm.current = 'gamemenu'
        cs.update_collection()
        main_theme.play()


class GameMenuScreen(Screen):
    def update_texture(self):
        self.ids.miner.update_texture()


class CollectionScreen(Screen):
    changed_name = ''

    def update_collection(self):
        self.ids.cl1.update_collection()

    def hello(self):
        print(self.changed_name)


class CatInfoScreen(Screen):
    pass


collection = Collection()

sm = ScreenManager()

ss = SignInScreen(name='signin')
cs = CollectionScreen(name='collection')
game_menu = GameMenuScreen(name='gamemenu')

sm.add_widget(ss)
sm.add_widget(SignUpScreen(name='signup'))
sm.add_widget(game_menu)
sm.add_widget(cs)
sm.add_widget(CatInfoScreen(name='catinfo'))


class CatApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    try:
        CatApp().run()
    except:
        print_exc()
