#!/usr/bin/env python
import npyscreen
import datetime
import time




def log(input):
    with open("test.txt", "a") as myfile:
        string=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        string=string+ ' - ' +input + '\n'
        myfile.write(string)

class LogIt:
    def __init__(self, input):
        self.input = input
    def __call__(self):
       log(str(self.input))

class FormObject(npyscreen.ActionForm):
    def create(self):
        self.name = self.add( npyscreen.TitleText, name="name" )
    
    def afterEditing( self ):
        self.parentApp.setNextForm(None)

    def on_ok( self):
     log(str( self.name.value))

class MainFormObject(npyscreen.ActionForm):
    def create( self ):


class App( npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', FormObject, name ="npyscreen form")

    
        
if (__name__ == "__main__"):
    app = App().run(0)
