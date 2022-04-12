import json
import os
import tkinter
from tkinter import messagebox
from tkinter import ttk
from functions import return_id_title_seen, set_channel_seen, print_id_title_seen, remove_channel, write_json
from scrapevideos import scrape_channel, scrape_all_channels ,update_channel, update_all_channels
from functools import partial
import webbrowser
import re

CHANNELS = dict()
CHANNEL_JSON = "test.json"


if not os.path.isfile(CHANNEL_JSON):
    with open(CHANNEL_JSON, 'w') as f:
        to_write = {'channels': []}
        json.dump(to_write, f)

def init_database():
    global CHANNELS
    with open(CHANNEL_JSON, 'r') as f:
        CHANNELS = json.load(f)

init_database()
###############################3############################3############################3

root = tkinter.Tk()
root.title("yt-notify")
root.minsize(width=150, height=172)
root.config(padx=20, pady=20)
root.tk.call('tk', 'scaling', 1.0)



#Get the length of the longest string from channels
def get_max_button_length():
    chan_list = list()
    for channel in CHANNELS['channels']:
        if channel == "channels":
            continue
        chan_list.append(channel['name'])
        if len(chan_list) >= 1:
            max_string = max(chan_list, key=len)
            max_len = len(max_string)
            button_width = max_len
        else:
            button_width = 5
    return button_width

#Checks if channel has unseen videos
def check_unseen(channel_name):
    for channel in CHANNELS[channel_name]:
        if channel['seen'] == False:
            return True
    return False

#Makes buttons for each channel name
def draw_channel_names():
    column_int = 0
    row_int = 0
    button_width = get_max_button_length()
    for channel in CHANNELS['channels']:
        if channel == "channels":
            continue
        
        name = channel['name']
        open_channel = partial(video_window,name)
#        tkinter.Button(text=name, command=open_channel).pack()
        if column_int == 3:
            row_int += 1
            column_int = 0
        check_vid = partial(video_window, name)
        update = partial(update_channel_window, name)
        if check_unseen(name):
            name += "*"
#        tkinter.Button(text=name,width=button_width, command=open_channel).grid(column=column_int, row=row_int)
        menub = tkinter.Menubutton(root, text=name,width=button_width, relief='groove')
        menub.grid(column=column_int, row=row_int)
        menub.menu = tkinter.Menu(menub, tearoff=0)
        menub["menu"] = menub.menu
        menub.menu.add_command(label="Video's", command=check_vid)
        menub.menu.add_command(label="Check for new video's", command=update)
        column_int +=1
    root.geometry("")

#Removes all widgets in root placed with pack, then make them again.
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
                               message=f"""Do you want to scrape the channel now?
                                       This may take a while depending on the uploaded video's""",
                               parent=add_channel_window)
        if input == 'yes':
            scrape_channel(name, CHANNELS)
        write_json(CHANNELS, CHANNEL_JSON)
        init_database()
        redraw_channel_names()
        add_channel_window.destroy()


    def url_check(url):
        re_http = re.compile("^https?://www.youtube.com/c/.*/$")
        if re.search(re_http, url) is None:
            return False
#            button_add.config(state='disabled')
        else:
            return True
#            button_add.config(state='normal')



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

def delete_channel_window():
    def delete_channel():
        name = entry_channel.get()
        for index, channel in enumerate(CHANNELS['channels']):
            if name == channel['name']:
                input = messagebox.askquestion(title="Delete channel",
                                       message=f"are you sure you want to delete, {name} and all it's video's?",
                                       parent=delete_channel_window)
                if input == 'yes':
                    CHANNELS['channels'].pop(index)
                    CHANNELS.pop(name)
                    write_json(CHANNELS, CHANNEL_JSON)
                    init_database()
                    redraw_channel_names()
                    delete_channel_window.destroy()
                    return
        messagebox.showerror(title="Error", 
                             message="Channel not found",
                             parent=delete_channel_window)


    delete_channel_window = tkinter.Tk()
    delete_channel_window.title("Add Channel")
    delete_channel_window.config(padx=20, pady=20)


    label_channel = tkinter.Label(delete_channel_window, text="Channel Name: ")
    label_channel.grid(column=0, row=0)

    entry_channel = tkinter.Entry(delete_channel_window, width=30)
    entry_channel.grid(column=1, row=0)

    button_add = tkinter.Button(delete_channel_window, text="Delete",command = delete_channel)
    button_add.grid(column=0, row=3)

    button_cancel = tkinter.Button(delete_channel_window, text="Cancel", command=delete_channel_window.destroy)
    button_cancel.grid(column=1, row=3)


    delete_channel_window.mainloop()

def video_window(channel_name):
    """Makes a window for a given channel and lists all videotitles with a checkbutton, """
    window_name = tkinter.Tk()
    window_name.title(channel_name)
    window_name.minsize(width=780, height=900)
    window_name.maxsize(width=780, height=900)
    window_name.config(padx=20, pady=20)
    window_name.tk.call('tk', 'scaling', 1.0)

    def save():
        """Saves the values from all checkboxes to CHANNELS and writes them to JSON_LOCATION"""
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

    label_channel_name = tkinter.Label(window_name, text=channel_name, font=('Ariel', 20, 'bold'))
    label_channel_name.pack(side='top')

    frame_title_seen = tkinter.Frame(window_name)
    frame_title_seen.pack(side='top')

    #Make Title and Seen labels
    label_title = tkinter.Label(frame_title_seen, text="Title", font=('Ariel', 12, 'bold'))
    label_title.grid(column=0, row=0, pady=5)

    label_title = tkinter.Label(frame_title_seen, text="\t\t\t\t\t\t", font=('Ariel', 12, 'bold'))
    label_title.grid(column=1, row=0, pady=5)

    label_seen = tkinter.Label(frame_title_seen, text="Seen", font=('Ariel', 12, 'bold'))
    label_seen.grid(column=2, row=0, pady=5)



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
    label_channels=[]
    var_list={}
    binds=[]


    for index, channel in enumerate(CHANNELS[channel_name]):
        #Make title shorter if too long
        title = channel['title']
        if len(title) > 57:
            title = title[0:57]

        #Make label for each title
        label = tkinter.Label(frame, text=title, cursor='hand2', font=('Ariel', 12))
#        label_channels.append(label)
        link = "https://www.youtube.com/watch?v=" + channel['video_id'] 
        #Make binds for each label and put on grid
        label.bind("<ButtonRelease-1>", lambda e, link=link: webbrowser.open_new_tab(link))
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
        label.grid(column=0, row=index+1, sticky="W")
        

        #Sets checkbox on/off for for video true/false
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

def update_channel_window(name):
    input = messagebox.askquestion(title="Update channel",
                       message=f"""Do you want to update the channel now?
                               This may take a while depending on the uploaded video's""",
                       parent=root)
    if input == 'yes':
        updates = update_channel(name, CHANNELS)
        write_json(CHANNELS, CHANNEL_JSON)
        redraw_channel_names()
        messagebox.showinfo(title="Updates", message=updates, parent=root)

def update_all_channels_window():
    input = messagebox.askquestion(title="Update all channels",
                       message=f"""Do you want to update all channels?
                               This may take a while depending on the uploaded video's""",
                       parent=root)
    if input == 'yes':
        updates = update_all_channels(CHANNELS)
        string = ""
        for update in updates:
            string += update + "\n"
        write_json(CHANNELS, CHANNEL_JSON)
        redraw_channel_names()
        messagebox.showinfo(title="Updates", message=string, parent=root)
   
#Add menubar at top
menubar = tkinter.Menu(root)
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Add channel", command=add_channel_window)
filemenu.add_command(label="Delete channel", command=delete_channel_window)
filemenu.add_separator()
filemenu.add_command(label="Update all channels", command=update_all_channels_window)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=filemenu)

#    helpmenu = tkinter.Menu(menubar, tearoff=0)
#    helpmenu.add_command(label="Help Index", command=donothing)
#    helpmenu.add_command(label="About...", command=donothing)
#    menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

#def window_size():
#    root.update()
#    screen_width = root.winfo_width()
#    screen_height = root.winfo_height()
#
#    print("Screen width:", screen_width)
#    print("Screen height:", screen_height)
#window_size()
draw_channel_names()

#window_size()
root.mainloop()

#videos_window(CHANNELS, "V for Valentine", CHANNEL_JSON)
#root_window(CHANNELS, CHANNEL_JSON)

