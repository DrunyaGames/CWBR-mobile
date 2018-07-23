from random import randint
from color_cat import color_cat
from kivy.uix.image import Image
from kivy.clock import mainthread
import os

def hex2rgb(hex_color):
    m = {'0':0, '1':1, '2':2, '3':3,
         '4':4, '5':5, '6':6, '7':7,
         '8':8, '9':9, 'a':10, 'b':11,
         'c':12, 'd':13, 'e':14, 'f':15}
    color1 = hex_color[1:3]
    color2 = hex_color[3:5]
    color3 = hex_color[5:7]
    r = m[color1[0]]*16 + m[color1[1]]
    g = m[color2[0]]*16 + m[color2[1]]
    b = m[color3[0]]*16 + m[color3[1]]
    return (r, g, b)
#id name color power owner_id

class User():
    def __init__(self, user_id, name, rights, cats):
        self.user_id = user_id
        self.name = name
        self.rights = rights
        self.cats = cats

class Collection():
    def __init__(self):
        self.collection = []

    def create_collection(self, cats):
        for cat_data in cats:
            new_cat = Cat(cat_data)
            self.collection.append(new_cat)




class Cat():
    def __init__(self, cat_data):
        self.id = cat_data['id']
        self.name = cat_data['name']
        self.hex_color = cat_data['color']
        self.main_color = hex2rgb(self.hex_color)  
        self.power = cat_data['power']
        self.owner_id = cat_data['owner_id']
        self.is_tum = cat_data['tum']
        self.path = 'temp_cats/'+str(self.id)+'.png'
        self.gen_cat()

    def gen_cat(self):        
        color_cat(self.main_color, self.is_tum, self.id)


