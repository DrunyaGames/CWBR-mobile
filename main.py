__version__ = '1.0'

import codecs
from kivy.app                import App
from kivy.lang               import Builder
# from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager  import *  # ScreenManager, Screen
from kivy.uix.textinput      import TextInput
from kivy.uix.popup          import Popup
from kivy.uix.label          import Label
from kivy.uix.behaviors      import ButtonBehavior
from kivy.uix.image          import Image
from kivy.uix.gridlayout     import GridLayout
from kivy.uix.boxlayout      import BoxLayout
from kivy.uix.floatlayout    import FloatLayout
from kivy.config             import Config
from kivy.uix.button         import Button
from kivy.properties         import BooleanProperty, ObjectProperty
from kivy.clock              import mainthread, Clock
from kivydnd.dragndropwidget import DragNDropWidget
from client                  import Client
from classes                 import User, Cat, Collection
from editable_lable          import EditableLabel
from time                    import sleep
from traceback               import print_exc
import os

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '854')
Config.write()

client = Client()

fileobj = codecs.open('cat_main.kv', 'r', 'utf_8_sig')
text = fileobj.read()
fileobj.close()

Builder.load_string(text)


# main_theme = SoundLoader.load('main_theme.mp3')

class UserDataInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = substring.replace(' ', '').replace('\t', '')
        return super().insert_text(s, from_undo=from_undo)


class ImageButton(ButtonBehavior, Image):
    pass


class BoxButton(ButtonBehavior, BoxLayout):
    orientation = 'vertical'

class Shelf(BoxLayout):
    milk_textures = {'2':'textures/items/milk.png',
                    '2:1':'textures/items/milk_normal.png',
                    '2:2':'textures/items/milk_hard.png',
                    '2:3':'textures/items/milk_legendary.png'
                    }
    def __init__(self, **kw):
        super().__init__(**kw)

    @mainthread
    def add_food(self, id):
        food = CatFood(source=self.milk_textures[id],
                       droppable_zone_objects=[game_menu.ids.miner],
                       drop_func=game_menu.ids.miner.send_data,
                       drop_args=[id])
        self.add_widget(food)
        


class CatFood(ImageButton, DragNDropWidget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.text = ''
        self.size_hint = (None, None)
        self.size = (100, 100)
        #self.remove_on_drag = False


class MinerButton(ImageButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_data(self, *args, **kwargs):
        client.send('use_item', {'item_id': args[1]})

    @mainthread
    @staticmethod
    @client.handle('item_used')
    def success_start():
        game_menu.ids.miner.source = 'textures/buttons/full_bowl.png'

    @mainthread
    @staticmethod
    @client.handle('new_cat')
    def get_answer(**cat):
        new_cat = Cat(cat)
        collection.collection.append(new_cat)
        cs.add_cat(new_cat)
        game_menu.ids.miner.source = 'textures/buttons/empty_bowl.png'

        # game_menu.stop_mining()


class CatCollectionButton(BoxButton):
    
    @mainthread
    def __init__(self, cat, **kwargs):
        super().__init__(**kwargs)
        self.cat_id = None
        #self.ids.cat_power.text = str(cat.power)
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
        self.show_cats()

    def add_cat(self, cat):
        self.widgets.append(CatCollectionButton(cat, size_hint_y=None, height=140))
        sleep(0.1)
        self.add_widget(self.widgets[-1])

    def show_cats(self):
        print('AAA', self.widgets)  # DO NOT ERASE
        for cat in collection.collection:
            sleep(0.1)
            self.add_cat(cat)

        ##    def update_collection(self):


##        for i in self.widgets:
##            self.remove_widget(i)
##            sleep(0.1)
##        self.widgets = []
##        for cat in collection.collection:
##            sleep(0.1)
##            self.add_cat(cat)
##        # self.show_cats()


class SignScreen(Screen):
    username = ''
    password = ''
    mess_send_type = ''
    mess_get_type = ''

    def callback(self):
        print(self.username)
        print(self.password)
        self.send_data()

    def send_data(self):
        client.send(self.mess_send_type, {'name': self.username, 'password': self.password})


class SignInScreen(SignScreen):
    mess_send_type = 'auth'
    mess_get_type = 'auth_ok'

    @staticmethod
    @client.handle(mess_get_type)
    def get_answer(user_id, name, rights, cats, session, is_mining, inventory):
        collection.create_collection(cats)
        game_menu.add_nickname(name)
        cs.show_cats()
        sm.current = 'gamemenu'
        print(inventory)
        game_menu.add_food(inventory)
        # main_theme.play()


class SignUpScreen(SignScreen):
    mess_send_type = 'reg'
    mess_get_type = 'reg_ok'

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

    @staticmethod
    @client.handle(mess_get_type)
    def get_answer(user_id, name, rights, cats, session, is_mining, inventory):
        collection.create_collection(cats)
        game_menu.add_nickname(name)
        cs.show_cats()
        sm.current = 'gamemenu'
        game_menu.add_food(inventory)
        # main_theme.play()


class GameMenuScreen(Screen):
    @mainthread
    def start_mining(self):
        self.ids.miner.source = 'textures/buttons/full_bowl.png'

    @mainthread
    def stop_mining(self):
        self.ids.miner.source = 'textures/buttons/empty_bowl.png'

    @mainthread
    def add_nickname(self, name):
        self.ids.nickname.text = name

    def add_food(self, inventory):
        for milk in inventory:
            for i in range(milk['count']):
                self.ids.shelf.add_food(milk['id'])


class CollectionScreen(Screen):
    changed_name = ''

    def show_cats(self):
        self.ids.cl1.show_cats()

    def add_cat(self, new_cat):
        self.ids.cl1.add_cat(new_cat)

    def hello(self):
        print(self.changed_name)


class CatInfoScreen(Screen):
    pass

class InventoryScreen(Screen):
    pass


collection = Collection()

sm = ScreenManager()

ss = SignInScreen(name='signin')
cs = CollectionScreen(name='collection')
game_menu = GameMenuScreen(name='gamemenu')
inventory = InventoryScreen(name='inventory')

sm.add_widget(ss)
sm.add_widget(SignUpScreen(name='signup'))
sm.add_widget(game_menu)
sm.add_widget(cs)
sm.add_widget(CatInfoScreen(name='catinfo'))
sm.add_widget(inventory)


class CatApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return sm

if __name__ == '__main__':
    try:
        CatApp().run()
    except:
        print_exc()
