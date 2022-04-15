#!/usr/bin/python
import os
import json
import re
import tkinter
import webbrowser
import pystray
import platform
from functions import write_json, init_database, get_max_button_length, check_unseen, url_check
from scrapevideos import scrape_channel, scrape_all_channels ,update_channel, update_all_channels
from tkinter import ttk
from tkinter import messagebox
from functools import partial
from pystray import MenuItem as item
from PIL import Image, ImageTk
from notifypy import Notify

PLATFORM = platform.system()
CHANNEL_JSON = "./data/data.json"
CHANNELS = init_database(CHANNEL_JSON)
SCALING = ('tk', 'scaling', 1)


########### Functions for systray ###############
def quit_window(icon, item):
    icon.stop()
    root.destroy()

def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify())

def hide_window():
    root.withdraw()
    image=Image.open("./images/icon.ico")
    menu=(item('Show', show_window),item("Update all channels", notify_update), item('Quit', quit_window))
    icon=pystray.Icon("name", image, "yt-notify", menu)
    icon.run()
########### End Functions for systray ###########



#Makes buttons for each channel name
def draw_channel_names():
    column_int = 0
    row_int = 0
    button_width = get_max_button_length(CHANNELS)
    for channel in CHANNELS['channels']:
        if channel == "channels":
            continue
        
        name = channel['name']
        if column_int == 3:
            row_int += 1
            column_int = 0
        open_channel = partial(video_window,name)
        check_vid = partial(video_window, name)
        update = partial(update_channel_window, name)
        delete = partial(delete_channel, name)
        #Check if channel has unseen videos, if so put astericks after name
#        if check_unseen(name, CHANNELS):
#            name += "*"
        menub = tkinter.Menubutton(root, text=name,width=button_width, relief='raised')
        if check_unseen(name, CHANNELS):
            menub.config(fg='red')
        else:
            menub.config(fg='blue')

        menub.grid(column=column_int, row=row_int)
        menub.menu = tkinter.Menu(menub, tearoff=0)
        menub["menu"] = menub.menu
        menub.menu.add_command(label="Video's", command=check_vid)
        menub.menu.add_command(label="Check for new video's", command=update)
        menub.menu.add_separator()
        menub.menu.add_command(label="Remove channel", command=delete)
        column_int +=1
    #Prints text in root if no channels are added
    if len(root.winfo_children()) <= 1: 
        add_label = tkinter.Label(root, text="Add channels to list them here.")
        add_label.grid(column=0, row=0)

    root.geometry("")

#Removes all widgets in root placed with grid, then make them again.
def redraw_channel_names():
    list = root.grid_slaves()
    for l in list:
        l.destroy()
    #Makes them again
    draw_channel_names()

#Make window "Add channel" 
def add_channel_window(): 

    def add_channel():
        name = entry_channel.get()
        url = entry_url.get()
        for channel in CHANNELS['channels']:
            if not url_check(url):
                messagebox.showerror("Error", "Incorrect URL format", parent=add_channel_window)
                return
            elif name == channel['name']:
                messagebox.showerror("Error", f"{name} already in database", parent=add_channel_window)
                return
            elif url == channel['url']:
                messagebox.showerror("Error", "URL already in database", parent=add_channel_window)
                return

        CHANNELS['channels'].append({'name': name, 'url': url})
        CHANNELS[name] = []
        input = messagebox.askquestion(title="Scrape",
                               message=f"Do you want to scrape the channel now?\nThis may take a while depending on the uploaded video's", parent=add_channel_window)
        if input == 'yes':
            try:
                scrape_channel(name, CHANNELS)
            except:
                messagebox.showerror("Error", "Channel probably not found", parent=add_channel_window)
                for index, channel in enumerate(CHANNELS['channels']):
                    if name == channel['name']:
                        CHANNELS['channels'].pop(index)
                        CHANNELS.pop(name)
                        return

            write_json(CHANNELS, CHANNEL_JSON)
            init_database(CHANNEL_JSON)
            redraw_channel_names()
            add_channel_window.destroy()


    add_channel_window = tkinter.Tk()
    add_channel_window.title("Add Channel")
    add_channel_window.config(padx=20, pady=20)

    label_channel = tkinter.Label(add_channel_window, text="Channel Name: ")
    label_channel.grid(column=0, row=0)

    label_url = tkinter.Label(add_channel_window, text="Youtube URL: ")
    label_url.grid(column=0, row=1)

    entry_channel = tkinter.Entry(add_channel_window, width=38)
    entry_channel.grid(column=1, row=0)

    entry_url = tkinter.Entry(add_channel_window, width=38)
    entry_url.grid(column=1, row=1)
    entry_url.insert(tkinter.END, string="https://www.youtube.com/c/ChannelName/")

    button_add = tkinter.Button(add_channel_window, text="Add",command = add_channel)
    button_add.grid(column=0, row=3)

    button_cancel = tkinter.Button(add_channel_window, text="Cancel", command=add_channel_window.destroy)
    button_cancel.grid(column=1, row=3)


    add_channel_window.mainloop()

#Deletes all data from data.json for given channel
def delete_channel(name):
    for index, channel in enumerate(CHANNELS['channels']):
        if name == channel['name']:
            input = messagebox.askquestion(title="Delete channel",
                                   message=f"are you sure you want to delete, {name} and all it's video's?",
                                   parent=root)
            if input == 'yes':
                CHANNELS['channels'].pop(index)
                CHANNELS.pop(name)
                write_json(CHANNELS, CHANNEL_JSON)
                init_database(CHANNEL_JSON)
                redraw_channel_names()
                return
            return
    messagebox.showerror(title="Error", 
                         message="Channel not found",
                         parent=root)

#Draws all the videos including checkboxes for the given channel
def video_window(channel_name):
    """Makes a window for a given channel and lists all videotitles with a checkbutton, """
    window_name = tkinter.Tk()
    window_name.title(channel_name)
    window_name.minsize(height=900, width=780)
    window_name.config(padx=20, pady=20)
#    window_name.tk.call('tk', 'scaling', 1.0)

    def save():
        """Saves the values from all checkboxes to CHANNELS and writes them to CHANNEL_JSON"""
        for key, value in var_list.items():
            for index, video in enumerate(CHANNELS[channel_name]):
                if key == video['video_id']: 
                    if value.get() == 1:
                        CHANNELS[channel_name][index]['seen'] = True
                    elif value.get() == 0:
                        CHANNELS[channel_name][index]['seen'] = False

        write_json(CHANNELS, CHANNEL_JSON)
        redraw_channel_names()

    #Functions to check/unceck checkboxes
    def check_all():
        for value in var_list.values():
            value.set(1)

    def uncheck_all():
        for value in var_list.values():
            value.set(0)

    #Functions to change foreground of widgets on leave/enter
    def on_leave(e):
        e.widget['fg'] = 'black'

    def on_enter(e):
        e.widget['fg'] = 'blue'

    #Close window function
    def close():
        redraw_channel_names()
        window_name.destroy()

    canvas = tkinter.Canvas(window_name)
    scroll_y = ttk.Scrollbar(window_name, orient='vertical', command=canvas.yview)
    frame = tkinter.Frame(canvas)
    frame.configure(borderwidth=2, relief='sunken')
    frame.pack()

    label_channel_name = tkinter.Label(window_name, text=channel_name, font=('Ariel', 20, 'bold'))
    label_channel_name.pack(side='top')

    frame_title_seen = tkinter.Frame(window_name)
    frame_title_seen.pack(side='top', fill='x')

    #Make Title and Seen labels
    label_title = tkinter.Label(frame_title_seen, text="Title", font=('Ariel', 12, 'bold'))
    label_title.pack(side='left')

    label_seen = tkinter.Label(frame_title_seen, text="Seen", font=('Ariel', 12, 'bold'))
    label_seen.pack(side='right')


    #Make a frame for save and close button
    frame_save_close = tkinter.Frame(window_name)
    frame_save_close.pack(side='bottom', anchor='w')

    #Save button
    frame_save = tkinter.Frame(frame_save_close)
    frame_save.pack(side='left', padx=100)
    button_save = tkinter.Button(frame_save, text="SAVE", font=('Ariel', 12, 'bold'), fg='green', padx=100, command=save)
    button_save.pack()

    #Close button
    frame_close = tkinter.Frame(frame_save_close)
    frame_close.pack(side='right')
    button_close = tkinter.Button(frame_close, text="Close", font=('Ariel', 12, 'bold'), command=close)
    button_close.pack()

    #Check button
    button_check = tkinter.Button(window_name, text="check all", command=check_all, width=10)
    button_check.pack(side='bottom', anchor='e')

    #Uncheck button
    button_uncheck = tkinter.Button(window_name, text="uncheck all", command=uncheck_all)
    button_uncheck.pack(side='bottom', anchor='e')

    #Make Label for title and checkbox for seen for every video
    var_list={}
    for index, channel in enumerate(CHANNELS[channel_name]):
        #Make title shorter if too long
        title = channel['title']
        if len(title) > 57:
            title = title[0:57]

        #Make label for each title
        label = tkinter.Label(frame, text=title, cursor='hand2', font=('Ariel', 12))
        link = "https://www.youtube.com/watch?v=" + channel['video_id'] 
        #Make binds for each label and put on grid
        label.bind("<ButtonRelease-1>", lambda e, link=link: webbrowser.open_new_tab(link))
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
        label.grid(column=0, row=index+1, sticky="W")
        
        #Sets checkbox on/off for video true/false
        if channel['seen'] == True:
            var_list[channel['video_id']]= tkinter.IntVar(frame, value=1)
        else:
            var_list[channel['video_id']] = tkinter.IntVar(frame, value=0)

        #Make checkboxes
        tkinter.Checkbutton(frame, variable=var_list[channel['video_id']]).grid(column=1, row=index+1)

    #Creates a canvas in a frame so a scrollbar can be added
    canvas.create_window(0, 0, anchor='nw', window=frame)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set)

    canvas.pack(anchor='nw', fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')


    window_name.mainloop()

#Draws update channel window and asks if users wants to update, if so then scrape and update channel.
def update_channel_window(name):
    input = messagebox.askquestion(title="Update channel",
                       message=f"Do you want to update the channel now?\nThis may take a while depending on the uploaded video's",
                       parent=root)
    if input == 'yes':
        updates = update_channel(name, CHANNELS)
        if updates[0] == 'no':
            text = f"{name} has no new videos"
        elif updates[0] == 'yes':
           text = f"{updates[1]} - {updates[2]} new video(s)\n" 
        write_json(CHANNELS, CHANNEL_JSON)
        redraw_channel_names()
        messagebox.showinfo(title="Updates", message=text, parent=root)

#Updates all channels and then gives a notification of found videos for each channel
def notify_update():
    updates = update_all_channels(CHANNELS)
    text = ""
    count_no = 0
    for channel in updates:
        if channel[0] == 'no':
            count_no += 1
        elif channel[0] == 'yes':
           text += f"{channel[1]} - {channel[2]} new video(s)\n" 
    if count_no == len(updates):
        text = "No new videos"

    notify = Notify()
    notify.title = "yt-notify"
    notify.message = text
    notify.icon = ""
    notify.icon = "./images/icon.ico"
    if PLATFORM == 'Darwin':
        notify.icon = ""
    notify.send()
    write_json(CHANNELS, CHANNEL_JSON)
    redraw_channel_names()

def about_window():
    about = tkinter.Toplevel()
    about.title("About")
    about.minsize(width=500, height=300)
    about.config(padx=20, pady=20)

    canvas = tkinter.Canvas(about, width=150 , height=150)
    canvas.pack(side='left', anchor='n')
    logo = ImageTk.PhotoImage(Image.open('./images/icon.png'))
    canvas.create_image(20, 20, anchor='nw', image=logo)
    
    titel = tkinter.Label(about, text="yt-notify", font=('Ariel', 24, 'bold', 'italic'))
    titel.pack(side='top', anchor='e')
    version = tkinter.Label(about, text="version: 0.1", font=('Ariel', 10, 'italic'))
    version.pack(side='top', anchor='e')
    version = tkinter.Label(about, text="rbr", font=('Ariel', 10, 'italic'))
    version.pack(side='top', anchor='e')

    about.mainloop()


if __name__ == "__main__":

    root = tkinter.Tk()
    root.title("yt-notify")
    icon = tkinter.PhotoImage(file = './images/icon.png')
    root.iconphoto(False, icon)
    root.minsize(width=300, height=172)
    root.config(padx=20, pady=20)
#    root.tk.call(SCALING)

    #Add menubar at top
    menubar = tkinter.Menu(root)
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Add channel", command=add_channel_window)
    filemenu.add_separator()
    filemenu.add_command(label="Update all channels", command=notify_update)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="Menu", menu=filemenu)

    helpmenu = tkinter.Menu(menubar, tearoff=0)
#    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=about_window)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)

    draw_channel_names()

    root.protocol('WM_DELETE_WINDOW', hide_window)
    root.mainloop()

