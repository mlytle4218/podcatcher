#!/usr/bin/env python
import menu
import menu2
import curses                                                                
import podcatcher
from curses import panel                                                     
import time
import new

import collections


class MyApp(object):                                                         

    def __init__(self, stdscreen):                                         
        self.screen = stdscreen 
                                          
        curses.curs_set(0)                                                   
                          
        newmenu = menu2.Menu([], self.screen)

        main_menu_items = [                                                  
                ('add new feed', newmenu.input_podcast_info),
                ('edit feed', newmenu.edit_podcast_info),
                ('delete feed',newmenu.delete_feed),
                ('download all new files', newmenu.download_new)
                # ('exit', exit)                               
                ]  
        main_menu = menu2.Menu(main_menu_items, self.screen)                       
        main_menu.display()                                              

if __name__ == '__main__':                                                       
    curses.wrapper(MyApp)