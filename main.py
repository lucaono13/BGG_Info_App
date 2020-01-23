import kivy
kivy.require('1.11.1')

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

from bgg_api_functions import query

g_names = []
g_ids = []
g_years = []
g_types = []
#all_r = []
Builder.load_string('''
<SelectableLabel>:
    canvas.before:
    Color:
        rgba:(.0,0.9,.1,.3) if self.selected else (0, 0, 0, 1)
    Rectangle:
        pos: self.pos
        size: self.size

<RV>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: True
        pos_hint: {'top':1, 'right': 1}
''')

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
        if super(SelectableLabel, self).on_press(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self,rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        #print(list)
        print('made it here')
        #self.data = [{'text':str(x)} for x in self.data]
        print(self.data)


# Creates the search function
class SearchScreen(GridLayout):
    all_r = []
    search = ObjectProperty(None)
    #dynamic_ids = DictProperty({})

    def print_out(self, game):
        print(str(self.all_r[2][game]))

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

        self.all_r = query(link)
        print(self.all_r[0][0], self.all_r[1][0], self.all_r[2][0])
        g_ids = list(map(int, self.all_r[2]))
        listy = {}
        for x in range(len(self.all_r[0])):
            listy[self.all_r[0][x]] = g_ids[x]
        #RV.data = self.all_r[2]
        #RV.data = listy
        RV.data = g_ids
        return RV()







class BGGApp(App):
    def build(self):
        return SearchScreen()
        #return RV()

# run the application
if __name__ == '__main__':
    BGGApp().run()
    #Results().run()
