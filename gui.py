import tkinter
import os
from functions import write_json
import webbrowser


def all_videos_window(channel_list, channel_name, json_location):
    """Makes a window for a given channel and lists all videotitles with a checkbutton, """
    window_name = channel_name + "_window"
    window_name = tkinter.Tk()
    window_name.title(channel_name)
    window_name.minsize(width=770, height=900)
    window_name.maxsize(width=770, height=900)
    window_name.config(padx=20, pady=20)
    window_name.tk.call('tk', 'scaling', 1.0)

    def save():
        """Saves the values from all checkboxes to CHANNELS and writes them to JSON_LOCATION"""
        for key, value in var_list.items():
            for index, video in enumerate(channel_list[channel_name]):
                if key == video['video_id']: 
                    if value.get() == 1:
                        channel_list[channel_name][index]['seen'] = True
                    elif value.get() == 0:
                        channel_list[channel_name][index]['seen'] = False

        write_json(channel_list, json_location)

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

    canvas = tkinter.Canvas(window_name)
    scroll_y = tkinter.Scrollbar(window_name, orient='vertical', command=canvas.yview)
    frame = tkinter.Frame(canvas)

    frame_title_seen = tkinter.Frame(window_name)
    frame_title_seen.pack()

    #Make Title and Seen labels
    label_title = tkinter.Label(frame_title_seen, text="Title", font=('Ariel', 20, 'bold'))
    label_title.grid(column=0, row=0, sticky="W")

    label_blanc = tkinter.Label(frame_title_seen, text="           \t\t\t\t       ")
    label_blanc.grid(column=1, row=0)

    label_seen = tkinter.Label(frame_title_seen, text="Seen", font=('Ariel', 20, 'bold'))
    label_seen.grid(column=2, row=0, sticky="E")

    #Make Save and Print buttons
    button_save = tkinter.Button(text="Save", command=save)
    button_save.pack(anchor="center")

    button_uncheck = tkinter.Button(text="check all", command=check_all)
    button_uncheck.pack(anchor="e")

    button_check = tkinter.Button(text="uncheck all", command=uncheck_all)
    button_check.pack(anchor="e")

    #Make Label for title and checkbox for seen for every video
    label_channels=[]
    var_list={}
    binds=[]

    for index, channel in enumerate(channel_list[channel_name]):
        #Make title shorter if too long
        title = channel['title']
        if len(title) > 57:
            title = title[0:57]

        #Make label for each title
        label = tkinter.Label(frame, text=title, cursor='hand2', font=('Ariel', 12))
        label_channels.append(label)
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

#    for index, label in enumerate(label_channels):
#        link = "https://www.youtube.com/watch?v=" + str(index) 
#        label.bind("<ButtonRelease-1>", lambda e, link=link: webbrowser.open_new_tab(link))
#        label.grid(column=0, row=index+1, sticky="W")
#        label.bind('<Leave>', on_leave)
#        label.bind('<Enter>', on_enter)
#        binds.append(label_url)
    #Creates a canvas in a frame so a scrollbar can be added
    canvas.create_window(0, 0, anchor='nw', window=frame)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set)

    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')



    window_name.mainloop()
