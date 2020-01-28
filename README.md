# BGG Info App
App that will take board game info from Board Game Geek and will create a .csv file from it.

Created using Python and Kivy (while learning about Kivy along the way)


**Features**
* Search Board Game Geek XMLAPI2 for results that fit the search
* Read results from search [WIP] - Working on added Recycle View instead of scroll view
  - ~~Recycle view is giving errors: search function does return results, put doesn't output to a recycle view correctly yet.~~ *Resolved.*
  - ~~Missing labels for RecycleView. Functionality is working otherwise~~ *Resolved*
* When selected, add ID to list of IDs to search as well as remove from list [WIP]
* See Box Art image of board game in search results [Current WIP]
* Selected board games to add to csv file [WIP]
* Import .csv file and add/remove board games [WIP]
* See rows on database like results [WIP]
* More features...

This is a very barebones ReadMe file. As I get more done and know what I can and can't do with Kivy, I will update readme as much as possible.


---
In order to run the Python script, you will need to install Kivy (run only main.py):

> Windows: https://kivy.org/doc/stable/installation/installation-windows.html

> MacOS: https://kivy.org/doc/stable/installation/installation-osx.html

> Linux: https://kivy.org/doc/stable/installation/installation-linux.html
