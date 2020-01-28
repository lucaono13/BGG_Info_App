import kivy
kivy.require('1.11.1')
#import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty, StringProperty, DictProperty, BooleanProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout

# KivyMD Imports
import pandas as pd
from bgg_api_functions import query, getBoxArt, getInfo

id_list = []


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class RecycleViewRow(RecycleDataViewBehavior, BoxLayout):
    ''' Adds selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    name = StringProperty('')
    year = StringProperty('')
    uid = StringProperty('')
    img = StringProperty('')

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(RecycleViewRow, self).refresh_view_attrs(rv,index,data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(RecycleViewRow, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self,rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            #print(rv.data[index]['selected'])
            print("{0} selected".format(rv.data[index]['name']))
            id_list.append(rv.data[index]['uid'])

        else:
            #3rv.data[index]['selected'] = False
            print("{0} not selected".format(rv.data[index]['name']))
            if(rv.data[index]['uid'] in id_list):
                id_list.remove(rv.data[index]['uid'])

# Creates the search function
class SearchScreen(GridLayout):
    all_r = ListProperty([])
    searchinput = ObjectProperty()
    search_results = ObjectProperty()
    searchrs = DictProperty({})

    def print_out(self, game):
        print(str(self.all_r[2][game]))

    # Imports the data to the RecycleView
    def found_search(self,name, year, uid, img):
        #games = ['{} ({})'.format(name[d], year[d]) for d in range(len(name))]
        self.search_results.data = [{'name':str(name[x]), 'year':str(year[x]), 'uid':str(uid[x]), 'img':str(img[x])} for x in range(len(name))]
#, 'img':str(img[x])

    # function to search from API
    def on_search(self, bg, expan, src):
        keyword = src.text
        keyword = keyword.replace(" ", '+')
        link = ""
        if((bg.state == 'down') & (expan.state == 'normal')):
            link = "https://api.geekdo.com/xmlapi2/search?query={}&type=boardgame".format(keyword)
        elif((bg.state == 'normal') & (expan.state == 'down')):
            link = "https://api.geekdo.com/xmlapi2/search?query={}&type=boardgameexpansion".format(keyword)
        elif((bg.state == 'down') and (expan.state == 'down')):
            link = "https://api.geekdo.com/xmlapi2/search?query={}&type=boardgame,boardgameexpansion".format(keyword)
        else:
            link = "https://api.geekdo.com/xmlapi2/search?query={}".format(keyword)


        all_r = query(link)
        all_n = all_r[0]
        all_y = all_r[1]
        all_d = all_r[2]

        all_i = []
        all_i = getBoxArt(all_d)

        print(type(all_i))

        self.found_search(all_n, all_y, all_d, all_i)

class RV(RecycleView):

    data_added = StringProperty('')
    data_removed = StringProperty('')

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)



class AddRemove(GridLayout):

    filename = "Exported Data\\default.csv"
    add_rem = StringProperty('')
    gameinfo_df = pd.DataFrame(columns = ['Name', 'Year','Link','Min. Players','Max Players'])
    csvExp = []

    def AddData(self):
        print(id_list)
        print(self.filename)
        print(type(self.gameinfo_df))
        self.csvExp = getInfo(self.filename, id_list, self.gameinfo_df)
        #return csvExp

    def RemoveData():
        pass

    def Export(self):
        #print(id_list)
        self.csvExp.to_csv(self.filename, index=False, encoding='utf-8-sig')
        print('Exported!')

    def CSV_name(self,name):
        self.filename = "Exported Data\\" + name.text + ".csv"
        #print(filename)


class GameRoot(BoxLayout):
    pass



class BGGApp(App):
    title = "BGG App"

    def build(self):
        #return SearchScreen()
        #return RV()
        #return Builder.load_string(kv)
        return Builder.load_file('main.kv')

# run the application
if __name__ == '__main__':
    BGGApp().run()
    #Results().run()
