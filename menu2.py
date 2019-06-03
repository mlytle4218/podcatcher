import curses                                                        
import podcatcher
from curses import panel                                                     
import time,datetime
import math
import csv
from tempfile import NamedTemporaryFile
import shutil

import random

import new

podcast_reference = ['name','url','audio','video']



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
    


    
    def navigate_list(self, n):                                                 
        self.position += n
        # log(str(self.items[self.position]))
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
                self.items[self.position][1]()
                # if len(self.items[self.position]) == 3:
                #     self.items[self.position][1](
                #         self.items[self.position][2]
                #     )
                #     log('==3')
                # # elif len(self.items[self.position]) == 2:
                # #     log(str(self.items[self.position]))
                # #     self.items[self.position][1](
                # #         self.items[self.position][2]
                # #     )
                # #     log('==2')
                # else:
                #     log('else')
                #     self.items[self.position][1]()                         

            elif key == curses.KEY_UP:                                       
                self.navigate_list(-1)                                            

            elif key == curses.KEY_DOWN:                                     
                self.navigate_list(1)
            
            elif key == ord('q'):
                break


        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()


    def show_info(self,info):
        for value in info:
            log(str(value) + " " +str(info[value]))
    


    def input_request(self, inputs, func):                                                       
        inputs = self.update_dict_with_reference(inputs)

        func(inputs, 'feeds.csv')

    def input_podcast_info(self):
        info = new.get_podcast_dict()
        results = self.update_dict_with_reference(info)
        log(str(results))
        new.add_new_podcast(results)

    def edit_podcast_info(self):
        podcasts = new.get_podcasts()
        choice = self.list_choices_with_index(podcasts[:],'name','podcast_id')
        if choice:
            updated = self.update_dict_with_reference(podcasts[choice-1])
            log(str(updated))
            id = new.update_podcast(updated)
            log(str(id))
        return 0


    def update_dict_with_reference(self, inputDict):

        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear() 


        self.window.refresh()
        curses.doupdate()

        count = 0
        for entry in podcast_reference:
            self.window.addstr(count, 0, entry +":"+inputDict[entry])
            curses.echo()
            input = self.window.getstr(count+1, 0, self.width)
            if(input == '-1'):
                break
            curses.noecho()

            while len(inputDict[entry]) ==0 and len(input) ==0:
                self.window.addstr(count, 0, "this must not be blank - " + entry + ":" + inputDict[entry])
                curses.echo()
                input = self.window.getstr(count+1, 0, self.width)
                if(input == '-1'):
                    break
                curses.noecho()

            log(str(entry == 'url'))

            if (entry == 'url'):
                while not new.check_feed(inputDict[entry]):
                    self.window.addstr(count, 0, "this url did not check out - " + input)
                    curses.echo()
                    input = self.window.getstr(count+1, 0, self.width)
                    if(input == '-1'):
                        break
                    curses.noecho()


            if len(input) > 0:
                inputDict[entry] = input
            count = count + 2

        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()
        return inputDict

    def update_dict(self, inputDict):

        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear() 


        self.window.refresh()
        curses.doupdate()

        count = 0
        for key, value in inputDict.iteritems():
            self.window.addstr(count, 0, key +":"+str(value))
            curses.echo()
            # value_length = len(value) +1
            # input = self.window.getstr(count+1, value_length, self.width-(value_length))
            input = self.window.getstr(count+1, 0, self.width)
            curses.noecho()

            while len(value) ==0 and len(input) ==0:
                self.window.addstr(count, 0, "this must not be blank - " + key+":"+value)
                curses.echo()
                input = self.window.getstr(count+1, 0, self.width)
                curses.noecho()

            if len(input) > 0:
                inputDict[key] = input
            count = count + 2

        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()
        return inputDict

    def delete_feed(self):
        return 0


    def download_new(self):
        new.start_download('feeds.csv')
        return 0



   



    # send it a list of lists as inputs, 
    # prt is the column to print to the screen
    # ret is the column you want to return after choice is made        
    def list_choices_with_index(self, inputs, prt, ret):
        list_of_lists = []

        while len(inputs) > 0:
            temp_holder = []
            for i in range(self.height-1):
                if len(inputs) > 0:
                    # popped = inputs.pop()
                    # temp_holder.append(popped['name'])
                    temp_holder.append(inputs.pop())
            list_of_lists.append(temp_holder)

        # log(str(list_of_lists))

        new_items_index = 0
        # log(str(self.width))
        # log(str(self.height))

        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear()                                                  

        while True:                                                          
            self.window.refresh()                                            
            curses.doupdate()                                                
            for index, item in enumerate(list_of_lists[new_items_index]):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                                  
                else:                                                        
                    mode = curses.A_NORMAL                                   

                # msg = '%d. %s' % (index + 1, item)     
                msg = '%s' % (item[prt])                       
                self.window.addstr(1+index, 1, msg, mode) 

            key = self.window.getch()                                        

            if key in [curses.KEY_ENTER, ord('\n')]:
                log( str( list_of_lists[new_items_index][self.position][ret] ))
                self.window.clear()                                                 
                self.panel.hide()                                                    
                panel.update_panels()                                                
                curses.doupdate()
                return list_of_lists[new_items_index][self.position][ret]
                # if len(self.items[self.position]) > 2:
                #     self.items[self.position][1](
                #         self.items[self.position][2],
                #         self.items[self.position][3]
                #     )
                # else:
                #     self.items[self.position][1]()                         

            elif key == curses.KEY_UP:   
                self.position -= 1
                if self.position < 0:                                                
                    self.position = 0                                       

            elif key == curses.KEY_DOWN:  
                self.position += 1
                if self.position > len(list_of_lists[new_items_index])-1:
                    self.position = len(list_of_lists[new_items_index])-1
            
            elif key == ord('q'):
                break

            elif key == ord('n'):
                if len(list_of_lists)-1 > new_items_index:
                    new_items_index += 1
                    self.window.clear()
                    self.position = 0
            
            elif key == ord('p'):
                if new_items_index != 0:
                    new_items_index -= 1
                    self.window.clear()
                    self.position = 0


        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()              




    
    def list_choices(self, inputs):
        list_of_lists = []

        while len(inputs) > 0:
            temp_holder = []
            for i in range(self.height-1):
                if len(inputs) > 0:
                    # popped = inputs.pop()
                    # temp_holder.append(popped['name'])
                    temp_holder.append(inputs.pop())
            list_of_lists.append(temp_holder)

        # log(str(list_of_lists))

        new_items_index = 0
        # log(str(self.width))
        # log(str(self.height))

        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear()                                                  

        while True:                                                          
            self.window.refresh()                                            
            curses.doupdate()                                                
            for index, item in enumerate(list_of_lists[new_items_index]):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                                  
                else:                                                        
                    mode = curses.A_NORMAL                                   

                # msg = '%d. %s' % (index + 1, item)     
                msg = '%s' % (item)                       
                self.window.addstr(1+index, 1, msg, mode) 

            key = self.window.getch()                                        

            if key in [curses.KEY_ENTER, ord('\n')]:
                log( str( list_of_lists[new_items_index][self.position] ))
                self.window.clear()                                                 
                self.panel.hide()                                                    
                panel.update_panels()                                                
                curses.doupdate()
                return list_of_lists[new_items_index][self.position]
                # if len(self.items[self.position]) > 2:
                #     self.items[self.position][1](
                #         self.items[self.position][2],
                #         self.items[self.position][3]
                #     )
                # else:
                #     self.items[self.position][1]()                         

            elif key == curses.KEY_UP:   
                self.position -= 1
                if self.position < 0:                                                
                    self.position = 0                                       

            elif key == curses.KEY_DOWN:  
                self.position += 1
                if self.position > len(list_of_lists[new_items_index])-1:
                    self.position = len(list_of_lists[new_items_index])-1
            
            elif key == ord('q'):
                break

            elif key == ord('n'):
                if len(list_of_lists)-1 > new_items_index:
                    new_items_index += 1
                    self.window.clear()
                    self.position = 0
            
            elif key == ord('p'):
                if new_items_index != 0:
                    new_items_index -= 1
                    self.window.clear()
                    self.position = 0


        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()



    # def get_it2(self):
    #     filename = 'feeds.csv'
    #     tempfile = NamedTemporaryFile(delete=False)
    #     results = ()#= new.get_data_from_csv('feeds.csv')
    #     with open(filename, 'r+') as file:
    #         dictReader = csv.DictReader(file)
    #         fieldnames = dictReader.fieldnames
    #         results = list(dictReader)
    #         temp_list = []
    #         for input in results:
    #             # log(str(input['name']))
    #             temp_list.append(input['name'])
    #             # temp_list.append(input['name'])
    #             # log(str(type(input['name'])))
    #         # log(str(temp_list))
    #         choice = self.list_choices(temp_list)

    #         rows = []
    #         file.seek(0)
    #         for row in dictReader:
    #             if row['name'] == choice:
    #                 row = self.update_dict(row)
    #                 rows.append(row)
    #             else:
    #                 rows.append(row)
            
    #         file.seek(0)
    #         writer = csv.DictWriter(file, fieldnames=fieldnames)
    #         writer.writeheader()
    #         writer.writerows(rows)
    #         file.truncate()