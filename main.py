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

from bgg_api_functions import query


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Adds selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv,index,data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self,rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

# Creates the search function
class SearchScreen(GridLayout):
    all_r = ListProperty([])
    search = ObjectProperty()
    search_results = ObjectProperty()

    def print_out(self, game):
        print(str(self.all_r[2][game]))

    def found_search(self,name, year, uid):
        games = ['{} ({})'.format(name[d], year[d]) for d in range(len(name))]
        self.search_results.data = [{'game':x} for x in games]
        print(f"self.search_results.data={self.search_results.data}")

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

        self.found_search(all_n, all_y, all_d)

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
