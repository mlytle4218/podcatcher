import curses                                                                
import podcatcher
from curses import panel                                                     
import time,datetime
import math

import random

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

class Menu(object):
    log('Started Menu')                                                   

    def __init__(self, items, stdscreen): 
        self.height,self.width = stdscreen.getmaxyx()                   
        self.window = stdscreen.subwin(0,0)                                  
        self.window.keypad(1)                                                
        self.panel = panel.new_panel(self.window)                            
        self.panel.hide()                                                    
        panel.update_panels()                                                

        self.position = 0                                                    
        self.items = items                                           
    


    
    def navigateList(self, n):                                                 
        self.position += n
        log(str(self.items[self.position]))
        if self.position < 0:                                                
            self.position = 0                                            
        elif self.position >= len(self.items)+2:                               
            self.position = len(self.items)+1

    def navigateResultsList(self, n):                                                 
        self.position += n
        if self.items[self.position][3] > 0:
            curses.beep()
        if self.position < 0:                                                
            self.position = 0                                            
        elif self.position >= len(self.items)+2:                               
            self.position = len(self.items)+1
                                                  
                              

    def display(self):   

        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear()                                                  

        while True:                                                          
            self.window.refresh()                                            
            curses.doupdate()                                                
            for index, item in enumerate(self.items):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                                  
                else:                                                        
                    mode = curses.A_NORMAL                                   

                msg = '%d. %s' % (index, item[0])                            
                self.window.addstr(1+index, 1, msg, mode)                    

            key = self.window.getch()                                        

            if key in [curses.KEY_ENTER, ord('\n')]:                         
                if self.position == len(self.items)-1:                       
                    break                                                    
                else:                                                        
                    self.items[self.position][1]()                           

            elif key == curses.KEY_UP:                                       
                self.navigateList(-1)                                            

            elif key == curses.KEY_DOWN:                                     
                self.navigateList(1)
            
            elif key == ord('q'):
                break


        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()
    
    def input_request(self):                                                       
        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear() 


        self.window.refresh()
        curses.doupdate()
        search_string = "Enter search keywords"
        self.window.addstr(search_string)
        curses.echo()
        input = self.window.getstr(0, len(search_string) +1 ,80)
        curses.noecho()
        self.data = podcatcher.getlists(input)

        self.window.addstr("bbb")
        curses.echo()
        input = self.window.getstr(5,3,80)
        curses.noecho()

        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()

        # self.display_from_results()
    
    # def show_info(self,info):                                                       
    #     self.panel.top()                                                     
    #     self.panel.show()                                                    
    #     self.window.clear() 


    #     self.window.refresh()
    #     curses.doupdate()
    #     for value in info:
    #         log(value)
    #         self.window.addstr(value)
    #         self.window.addstr("\n")
    #     # self.window.addstr("Enter search keywords")
    #     curses.echo()
    #     input = self.window.getstr(2,3,20)
    #     curses.noecho()
    #     # self.data = podcatcher.getlists(input)

    #     self.window.clear()                                                  
    #     self.panel.hide()                                                    
    #     panel.update_panels()                                                
    #     curses.doupdate()

    def show_info(self,info):
        for value in info:
            log(str(value) + " " +str(info[value]))
    
    # def show_info(self,info):
    #     screen = curses.initscr()
    #     highlightText = curses.color_pair( 1 )
    #     normalText = curses.A_NORMAL
    #     max_row = 10 #max number of rows
    #     box = curses.newwin( max_row + 2, 64, 1, 1 )
    #     box.box()


    #     strings = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "l", "m", "n" ] #list of strings
    #     row_num = len( strings )

    #     pages = int( math.ceil( row_num / max_row ) )
    #     position = 1
    #     page = 1
    #     for i in range( 1, max_row + 1 ):
    #         if row_num == 0:
    #             box.addstr( 1, 1, "There aren't strings", highlightText )
    #         else:
    #             if (i == position):
    #                 box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
    #             else:
    #                 box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], normalText )
    #             if i == row_num:
    #                 break

    #     screen.refresh()
    #     box.refresh()

    #     x = screen.getch()
    #     while x != 27:
    #         if x == curses.KEY_DOWN:
    #             if page == 1:
    #                 if position < i:
    #                     position = position + 1
    #                 else:
    #                     if pages > 1:
    #                         page = page + 1
    #                         position = 1 + ( max_row * ( page - 1 ) )
    #             elif page == pages:
    #                 if position < row_num:
    #                     position = position + 1
    #             else:
    #                 if position < max_row + ( max_row * ( page - 1 ) ):
    #                     position = position + 1
    #                 else:
    #                     page = page + 1
    #                     position = 1 + ( max_row * ( page - 1 ) )
    #         if x == curses.KEY_UP:
    #             if page == 1:
    #                 if position > 1:
    #                     position = position - 1
    #             else:
    #                 if position > ( 1 + ( max_row * ( page - 1 ) ) ):
    #                     position = position - 1
    #                 else:
    #                     page = page - 1
    #                     position = max_row + ( max_row * ( page - 1 ) )
    #         if x == curses.KEY_LEFT:
    #             if page > 1:
    #                 page = page - 1
    #                 position = 1 + ( max_row * ( page - 1 ) )
            
    #         if x == ord( "q" ):
    #             break

    #         if x == curses.KEY_RIGHT:
    #             if page < pages:
    #                 page = page + 1
    #                 position = ( 1 + ( max_row * ( page - 1 ) ) )
    #         if x == ord( "\n" ) and row_num != 0:
    #             screen.erase()
    #             screen.border( 0 )
    #             screen.addstr( 14, 3, "YOU HAVE PRESSED '" + strings[ position - 1 ] + "' ON POSITION " + str( position ) )

    #         box.erase()
    #         screen.border( 0 )
    #         box.border( 0 )

    #         for i in range( 1 + ( max_row * ( page - 1 ) ), max_row + 1 + ( max_row * ( page - 1 ) ) ):
    #             if row_num == 0:
    #                 box.addstr( 1, 1, "There aren't strings",  highlightText )
    #             else:
    #                 if ( i + ( max_row * ( page - 1 ) ) == position + ( max_row * ( page - 1 ) ) ):
    #                     box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
    #                 else:
    #                     box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + strings[ i - 1 ], normalText )
    #                 if i == row_num:
    #                     break



    #         screen.refresh()
    #         box.refresh()
    #         x = screen.getch()

    #     curses.endwin()
    #     exit()
        
    def log_result(self):
        log(str(self.data['resultCount']))

    # def display2(self):                                                       
    #     self.panel.top()                                                     
    #     self.panel.show()                                                    
    #     self.window.clear()   
    #     self.pages = 0
    #     self.currentPage = 0


    #     self.window.refresh()
    #     curses.doupdate()
    #     self.window.addstr("Enter search keywords")
    #     curses.echo()
    #     input = self.window.getstr(2,3,20)
    #     curses.noecho()
    #     data = podcatcher.getlists(input)

 
    #     resultsArray = []


    #     def updatePages(n):
    #         self.currentPage += n
    #         if self.currentPage < 0:
    #             self.currentPage = 0
    #         if self.currentPage >= self.pages:
    #             self.currentPage = self.pages-1
            
    #         self.items = resultsArray[self.currentPage]
    #         self.position = 0


        
    #     results = data['results']           



    #     resultsWatcher = []
        
    #     for index, item in enumerate(results):
    #         res={}
    #         res['index'] = index
    #         res['item'] = item
    #         res['selected'] = False
    #         res['function'] = curses.flash
    #         resultsWatcher.append(res)


    #     # log(str(resultsWatcher))

        
    #     while len(resultsWatcher) > 0:
    #         holder=[]
    #         for i in range(self.height-3):
    #             if len(resultsWatcher) > 0:
    #                 popped = resultsWatcher.pop(0)
    #                 bob = str(popped['item']['artistName'].encode('ascii','ignore'))

    #                 holder.append((bob, LogIt('hi'),'nothing'))
            
    #         # log(str(len(holder)))
    #         resultsArray.append(holder)
        
    #     self.items = resultsArray[0]
    #     self.pages = len(resultsArray)

        


 
    #     while True:                
    #         self.window.clear()                                          
    #         self.window.refresh()                                            
    #         curses.doupdate()     

            
    #         for index, item in enumerate(self.items):                        
    #             if index == self.position:                                   
    #                 mode = curses.A_REVERSE                                  
    #             else:                                                        
    #                 mode = curses.A_NORMAL                                   
                
    #             msg = '%d. %s' % (index+1, item[0])    
    #             # self.window.addstr(str(self.items.count))
    #             if ((1+index)<self.height-2):
    #                 #the msg[:self.width-(1+len(str(1+index)))] adjusts the line ouput so it doesn't grow
    #                 #too much with the addition of the index numbers
    #                 self.window.addstr(1+index, 1, msg[:self.width-(1+len(str(1+index)))], mode)


    #         # this is hackery to make sure the next and previous tags light up when higlighted.
    #         if self.position == len(self.items):
    #             self.window.addstr(self.height-1, 1, "Previous Page", curses.A_REVERSE)
    #         else:
    #             self.window.addstr(self.height-1, 1, "Previous Page", curses.A_NORMAL)
    #         if self.position == len(self.items)+1:
    #             self.window.addstr(self.height-1, self.width-10, "Next Page", curses.A_REVERSE)
    #         else:
    #             self.window.addstr(self.height-1, self.width-10, "Next Page", curses.A_NORMAL)

    #         key = self.window.getch()                                        

    #         if key in [curses.KEY_ENTER, ord('\n')]:
    #             if self.position < len(self.items) -2:
    #                 if isinstance(self.items[self.position][1], tuple):
    #                     self.items[self.position][1][0](*self.items[self.position][1][1:])
    #                 else:
    #                     if self.items[self.position][1] is None:
    #                         self.items[self.position][1]
    #                     else:
    #                         self.items[self.position][1]()
                        
    #             elif self.position == len(self.items):
    #                 updatePages(-1)
    #             elif self.position == len(self.items)+1:
    #                 updatePages(1)                        

    #         elif key == curses.KEY_UP:                                       
    #             self.navigateList(-1)                                            

    #         elif key == curses.KEY_DOWN:                                     
    #             self.navigateList(1)

    #         elif key == ord('p'):
    #             updatePages(-1)
            
    #         elif key == ord('n'):
    #             updatePages(1)

    #         elif key == ord(' '):
    #             curses.beep() 
            
    #         elif key == ord('q'):
    #             self.items = []
    #             break



    #     self.window.clear()
    #     self.panel.hide()
    #     panel.update_panels()
    #     curses.doupdate()

    def display_from_results(self):                                                       
        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear()   
        self.pages = 0
        self.currentPage = 0

 
        resultsArray = []


        def updatePages(n):
            self.currentPage += n
            if self.currentPage < 0:
                self.currentPage = 0
            if self.currentPage >= self.pages:
                self.currentPage = self.pages-1
            
            self.items = resultsArray[self.currentPage]
            self.position = 0


        
        results = self.data['results']           

        resultsWatcher = []
        
        for index, item in enumerate(results):
            res={}
            res['index'] = index
            res['item'] = item
            res['selected'] = False
            res['function'] = curses.flash
            resultsWatcher.append(res)



        
        while len(resultsWatcher) > 0:
            holder=[]
            for i in range(self.height-3):
                if len(resultsWatcher) > 0:
                    popped = resultsWatcher.pop(0)
                    bob = str(popped['item']['artistName'].encode('ascii','ignore')) + " - " + str(popped['item']['collectionName'].encode('ascii','ignore'))
                    holder.append([bob, LogIt(bob),popped['index'],False])
                    # ran = random.uniform(0,1)
                    # if ran > .8:)
                    #     holder.append([bob, LogIt(bob),popped['index'],True])
                    # else:
                    #     holder.append([bob, LogIt(bob),popped['index'],False])
            
            resultsArray.append(holder)
        
        self.items = resultsArray[0]
        self.pages = len(resultsArray)

        


 
        while True:                
            self.window.clear()                                          
            self.window.refresh()                                            
            curses.doupdate()     

            
            for index, item in enumerate(self.items):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                             
                else:                                                        
                    mode = curses.A_NORMAL   

                if item[3] > 0:
                    mode = curses.A_REVERSE                         
                
                msg = '%d. %s' % (item[2]+1, item[0])    
                # self.window.addstr(str(self.items.count))
                if ((1+index)<self.height-2):
                    #the msg[:self.width-(1+len(str(1+index)))] adjusts the line ouput so it doesn't grow
                    #too much with the addition of the index numbers
                    self.window.addstr(1+index, 1, msg[:self.width-(1+len(str(1+index)))], mode)


            # this is hackery to make sure the next and previous tags light up when higlighted.
            if self.position == len(self.items):
                self.window.addstr(self.height-1, 1, "Previous Page", curses.A_REVERSE)
            else:
                self.window.addstr(self.height-1, 1, "Previous Page", curses.A_NORMAL)
            if self.position == len(self.items)+1:
                self.window.addstr(self.height-1, self.width-10, "Next Page", curses.A_REVERSE)
            else:
                self.window.addstr(self.height-1, self.width-10, "Next Page", curses.A_NORMAL)

            key = self.window.getch()                                        

            if key in [curses.KEY_ENTER, ord('\n')]:
                if self.position < len(self.items) -2:
                    if isinstance(self.items[self.position][1], tuple):
                        self.items[self.position][1][0](*self.items[self.position][1][1:])
                    else:
                        if self.items[self.position][1] is None:
                            self.items[self.position][1]
                        else:
                            # self.items[self.position][1]()
                            self.show_info(results[self.items[self.position][2]])
                        
                elif self.position == len(self.items):
                    updatePages(-1)
                elif self.position == len(self.items)+1:
                    updatePages(1)                        

            elif key == curses.KEY_UP:                                       
                self.navigateResultsList(-1)                                            

            elif key == curses.KEY_DOWN:                                     
                self.navigateResultsList(1)

            elif key == ord('p'):
                updatePages(-1)
            
            elif key == ord('n'):
                updatePages(1)

            elif key == ord('a'):
                if self.items[self.position][3]:
                    self.items[self.position][3]=False
                else:
                    self.items[self.position][3]=True
                    log(str(results[self.items[self.position][2]]))
                # log(str(self.items[self.position][3]))
                # if self.items[self.position][3] > 0:
                #     self.items[self.position][3] = 0
                # else:
                #     # temp = [self.items[self.position][0],
                #     #     self.items[self.position][1],
                #     #     self.items[self.position][2],
                #     #     1]
                #     # self.items[self.position]=temp
                #     # self.items[self.position][3] = int(1)
                #     self.items[self.position][3] = 1
                #     log(str(self.items[self.position][3]))
            
            elif key == ord('q'):
                self.items = []
                break



        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()