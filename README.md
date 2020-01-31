# BGG Info App
App that will take board game info from Board Game Geek and will create a .csv file from it.

Created using Python and Kivy (while learning about Kivy along the way)

![App Main Screen](https://i.imgur.com/yeptBlu.png "App Screen")


**Features**
* Search Board Game Geek using their XMLAPI2 from user input search
* Show results in a RecycleView (with images)
* Select and add games to be added to exported csv
  - When you make all your selections for a search, click "Get data" and the app will get the data (deselect the selections every search)
* Export data to csv file
  - Once all data has been collected, click export (default .csv name is default.csv)

Decided to switch over to PyQT instead to make a program that's more to my vision of how it would look like. Will make a new repo and link it below. All functionality from this project will be reused in my other project, but will add more features like:
* Ability to import .csv file and add/remove board games to that file
* Second RecycleView to see which games are going to be exported to csv
* Ability to get specific info on games (e.g. Designers, Mechanics, Playtime, etc)
* And more to come...

Link to new project: https://github.com/lucaono13/Board-Game-Info-Grabber

---
In order to run the Python script, you will need to install Kivy (run only main.py):

> Windows: https://kivy.org/doc/stable/installation/installation-windows.html

> MacOS: https://kivy.org/doc/stable/installation/installation-osx.html

> Linux: https://kivy.org/doc/stable/installation/installation-linux.html
