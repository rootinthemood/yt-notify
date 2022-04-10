import json
import os
import tkinter
from functions import add_channel, return_id_title_seen, set_channel_seen, print_id_title_seen, remove_channel, write_json
from scrapevideos import scrape_channel, scrape_all_channels ,update_channel, update_all_channels
from functools import partial

CHANNELS = dict()
CHANNEL_JSON = "test.json"

if not os.path.isfile(CHANNEL_JSON):
    with open(CHANNEL_JSON, 'w') as f:
        to_write = {'channels': []}
        json.dump(to_write, f)

with open(CHANNEL_JSON, 'r') as f:
    CHANNELS = json.load(f)
###############################3############################3############################3

root = tkinter.Tk()
root.title("yt-notify")
root.minsize(width=900, height=900)
root.config(padx=20, pady=20)
root.tk.call('tk', 'scaling', 1.0)

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
        window_name.destroy()

    canvas = tkinter.Canvas(window_name)
    scroll_y = tkinter.Scrollbar(window_name, orient='vertical', command=canvas.yview)
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
    canvas.create_window(0, 0, anchor='s', window=frame)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set)

    canvas.pack(anchor='n', fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')



    window_name.mainloop()

def donothing():
   x = 0
   

menubar = tkinter.Menu(root)
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

#    helpmenu = tkinter.Menu(menubar, tearoff=0)
#    helpmenu.add_command(label="Help Index", command=donothing)
#    helpmenu.add_command(label="About...", command=donothing)
#    menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

for channel in CHANNELS:
    if channel == "channels":
        continue
    open_channel = partial(video_window,channel)
    tkinter.Button(text=channel, command=open_channel).pack()



root.mainloop()

#videos_window(CHANNELS, "V for Valentine", CHANNEL_JSON)
#root_window(CHANNELS, CHANNEL_JSON)

