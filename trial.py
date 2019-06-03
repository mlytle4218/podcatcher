#!/usr/bin/env python
import npyscreen

import datetime
import time


import new
import curses


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


'''
Classes to list and delete podcasts
'''
class ListAvailablePodcastsDelete(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(ListAvailablePodcastsDelete, self).__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.quit_screen
        })

    def display_value(self, vl):
        return "%s" % (vl['name'])

    def actionHighlighted(self, act_on_this, keypress):
        log( str( act_on_this['podcast_id'] ) )
        new.remove_podcast(act_on_this['podcast_id'])
        self.parent.parentApp.switchFormPrevious()

    def quit_screen(self, *args, **keywords):
        self.parent.parentApp.switchFormPrevious()

class ListAvailablePodcastsDeleteMutt(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = ListAvailablePodcastsDelete
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = new.get_podcasts()
        self.wMain.display()

'''
Classes to list and update podcasts
'''
class ListAvailablePodcast(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(ListAvailablePodcast, self).__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.quit_screen
        })

    def display_value(self, vl):
        return "%s" % (vl['name'])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDITPODCAST').value = act_on_this
        self.parent.parentApp.switchForm('EDITPODCAST')

    def quit_screen(self, *args, **keywords):
        self.parent.parentApp.switchFormPrevious()

class ListAvailablePodcastsMutt(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = ListAvailablePodcast
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = new.get_podcasts()
        self.wMain.display()

        '''
Classes to list podcasts with available downloads
'''
class ListAvailableDownloads(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(ListAvailableDownloads, self).__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.quit_screen,
            "^D": self.download
        })

    def display_value(self, vl):
        return "%s" % (vl['name'])

    def actionHighlighted(self, act_on_this, keypress):
        # log( str( vars( self.parent.parentApp.getForm('LISTEPISODES') )  ) )
        self.parent.parentApp.getForm('LISTEPISODES').value = act_on_this

        # log( str( vars( self.parent.parentApp.getForm('LISTEPISODES') )  ) )
        self.parent.parentApp.switchForm('LISTEPISODES')

    def quit_screen(self, *args, **keywords):
        self.parent.parentApp.switchFormPrevious()

    def download(self, *args, **keywords):
         log( str( vars( self ) ) )

class ListAvailableDownloadsMutt(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = ListAvailableDownloads
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = new.get_podcasts_that_have_downloads_available()
        self.wMain.downloads = None
        self.wMain.display()


'''
Class to list and mark episodes for download
'''
class ListEpisodes(npyscreen.ActionForm):
    def __init__(self, *args, **keywords):
        super(ListEpisodes, self).__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.quit_screen,
            curses.ascii.CR: self.quit_screen,
            "^P": self.selected_return

        })

    def actionHighlighted(self, act_on_this, key_press):
        "Override this Method"
        log( ' higlighted')
        pass

    def selected_return( self, *args, **keywords ):
        # log( str( self.multiSelect._last_cursor_line ) )
        log( str( "control P" ) ) 
    
    def display_value(self, vl):
        return "%s ," % (vl)

    def create( self ):
        self.multiSelect =  self.add(npyscreen.MultiSelect, values=['here','herehere'])

    def beforeEditing( self ):
        self.results = new.get_episodes_by_podcast_id( self.value['podcast_id'] )
        filtered = [result['title'] for result in self.results]
        self.multiSelect.values = filtered
    
    def on_ok( self ):
        # temp_downloads = self.parentApp.getForm('LISTAVAILABLEDOWNLOADSMUTT').wMain.downloads
        # if temp_downloads:
        #     for each in self.multiSelect.value:
        #         temp_downloads.append( self.results[ each ] )
        # else:
        #     temp_downloads = []
        #     for each in self.multiSelect.value:
        #         temp_downloads.append( self.results[ each ] )
        
        log( 'before' )
        log( str( vars( self.parentApp.getForm('LISTAVAILABLEDOWNLOADSMUTT').parentApp ) ) )
        
        temp_downloads = self.parentApp.getForm('LISTAVAILABLEDOWNLOADSMUTT').wMain.downloads
        if not temp_downloads:
            temp_downloads = []
            
        for each in self.multiSelect.value:
            temp_downloads.append( self.results[ each ] )

        self.parentApp.getForm('LISTAVAILABLEDOWNLOADSMUTT').wMain.downloads = temp_downloads

        log( 'after' )
        log( str( self.parentApp.getForm('LISTAVAILABLEDOWNLOADSMUTT').wMain.downloads  ) )

        # log( str( temp_downloads ) )
        # log( str( vars( self.multiSelect )  ) )
        # log( str( self.multiSelect._last_cursor_line  ) )
        # log( str( vars( self.parentApp.getForm('LISTAVAILABLEDOWNLOADSMUTT').wMain ) ) )
        # log( str(  self.parentApp.getForm('LISTAVAILABLEDOWNLOADSMUTT')  ) )
        # self.parentApp.switchFormPrevious()
    def on_cancel( self ):
        self.parentApp.switchFormPrevious()


    def quit_screen(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

'''
Class to update and create podcast
'''
class EditPodcast(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.name = self.add(npyscreen.TitleText, name="podcast name")
        self.url   = self.add(npyscreen.TitleText, name = "podcast url",)
        self.audio = self.add(npyscreen.TitleText, name = "audio save location")
        self.video = self.add(npyscreen.TitleText, name = "video save location")

    def beforeEditing(self):
        if self.value:
            self.name.value = self.value['name']
            self.url.value = self.value['url']
            self.audio.value = self.value['audio']
            self.video.value = self.value['video']

    def on_ok(self):
        if self.value:
            self.value['name'] = self.name.value
            self.value['url'] = self.url.value
            self.value['audio'] = self.audio.value
            self.value['video'] = self.video.value
            new.update_podcast(self.value)
            self.name.value = ""
            self.url.value = ""
            self.audio.value = ""
            self.video.value = ""
        else:
            new_podcast = {}
            new_podcast['name'] = self.name.value
            new_podcast['url'] = self.url.value
            new_podcast['audio'] = self.audio.value
            new_podcast['video'] = self.video.value
            new.add_new_podcast(new_podcast)
            self.name.value = ""
            self.url.value = ""
            self.audio.value = ""
            self.video.value = ""

        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.name.value = ""
        self.url.value = ""
        self.audio.value = ""
        self.video.value = ""
        self.parentApp.switchFormPrevious()





class MainMenu(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(MainMenu, self).__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.quit_screen
        })

    def display_value(self, vl):
        return "%s" % (vl)

    def actionHighlighted(self, act_on_this, keypress):
        if (act_on_this == 'add new podcast'):
            self.parent.parentApp.switchForm('EDITPODCAST')
        elif (act_on_this == 'edit existing podcast'):
            self.parent.parentApp.getForm('LISTAVAILABLEPODCAST').value = 'update'
            self.parent.parentApp.switchForm('LISTAVAILABLEPODCAST')
        elif (act_on_this == 'delete existing podcast'):
            self.parent.parentApp.switchForm('LISTAVAILABLEPODCASTDELETE')
        elif (act_on_this == 'check available downloads'):
            self.parent.parentApp.switchForm('LISTAVAILABLEDOWNLOADSMUTT')

    def quit_screen(self, *args, **keywords):
        self.parent.parentApp.switchForm(None)

class MainMenuDisplayMutt(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = MainMenu
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = [
            ("add new podcast"),
            ('edit existing podcast'),
            ('delete existing podcast'),
            ('check available downloads')]
        self.wMain.display()






















class AddressBookApplication(npyscreen.NPSAppManaged):
    download_queue = []

    def onStart(self):
        pass
        # self.myDatabase = AddressDatabase()
        self.addForm("MAIN", MainMenuDisplayMutt)
        self.addForm("EDITPODCAST", EditPodcast)
        self.addForm("LISTAVAILABLEPODCAST",ListAvailablePodcastsMutt)
        self.addForm("LISTAVAILABLEPODCASTDELETE",ListAvailablePodcastsDeleteMutt)
        self.addForm("LISTAVAILABLEDOWNLOADSMUTT",ListAvailableDownloadsMutt)
        self.addForm("LISTEPISODES", ListEpisodes)

if __name__ == '__main__':
    myApp = AddressBookApplication()
    myApp.run()
