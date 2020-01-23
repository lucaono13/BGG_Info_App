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
    def __init__(self,games, **kwargs):
        super(RV, self).__init__(**kwargs)
        #print(list)
        print('made it here')
        self.data = [{'text':str(x)} for x in games]
        #print(self.data)


"""Builder.load_string('''
<RV>:
    viewclass:'Label'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')
class RV(RecycleView):
    def __init__(self,games,**kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text':str(x)} for x in games]
        #self.data = [{'text':str(x)} for x in range(10)]"""


class SearchScreen(GridLayout):
    all_r = []
    search = ObjectProperty(None)
    dynamic_ids = DictProperty({})

    def print_out(self, game):
        print(str(self.all_r[2][game]))

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
        #print(self.all_r)
        #return RV(self.all_r)
        #self.add_widget(RV(self.all_r[2]))
        #self.Results()
        return(RV(self.all_r[2]))
        #print('azul')
        #Results.data = self.all_r[2]
        # add function to query BGG API2
        # GridLayout for search results: 3 cols [Name; Type; ID]

    #def Results(self, *kwargs):

        #print(self.all_r[2])


        """scroll = self.ids.resultados
        scroll.clear_widgets()
        print("names: " + str(len(self.all_r[0])) + "; years: " + str(len(self.all_r[1])) + "; IDs: " + str(len(self.all_r[2])))

        grid = GridLayout(cols=3, size_hint_y=None, spacing = '25dp', padding=[0,"10dp",0,0], height=200)
        buttons = {}
        id_but = {}
        for game in range(len(self.all_r[0])):
            #id = str(self.all_r[2][game])
            name = str(self.all_r[2][game])
            grid.add_widget(Label(text=self.all_r[0][game], halign="left",text_size=(199,None), shorten=True, height = "10dp"))
            grid.add_widget(Label(text=self.all_r[1][game], height = "10dp"))

            buttons[name] = Button(text=self.all_r[2][game], background_color = (0,0,0,1), size_hint_y=None, height="10dp")
            id_but[buttons[name]] = str(self.all_r[2][game])
            #nButton.bind(on_press=self.print_out(game))
            #buttons[name].bind(on_press = lambda x: print(id_but[buttons[name]]))
            grid.add_widget(buttons[name])

            #print(buttons[name])
            #f_nextCheck.bind(on_active=self.print_out)
            #grid.add_widget(CheckBox(height = "10dp"))
            #self.CBID = CheckBox()

            #self.ids[str(self.all_r[2][game])].add_widget(self.CBID)
            #grid.add_widget(Label(text=self.all_r[2][game], size_hint_x=1))
        print(buttons)"""
        #scroll.add_widget(grid)






class BGGApp(App):
    def build(self):
        return SearchScreen()
        #self.load_kv('BGG.kv')

"""class Results(App):
    data = []
    def build(self):
        return RV()"""

if __name__ == '__main__':
    BGGApp().run()
    #Results().run()
