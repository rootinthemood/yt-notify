import tkinter
import os
from functions import write_json


def all_videos_window(channel_list, channel_name, json_location):
    """Makes a window for a given channel and lists all videotitles with a checkbutton, """
    window_name = channel_name + "_window"
    window_name = tkinter.Tk()
    window_name.title(channel_name)
    window_name.minsize(width=600, height=600)
    window_name.maxsize(width=600, height=600)
    window_name.config(padx=20, pady=20)

    def save():
        """Saves the values from all checkboxes to the main channel"""
        for key, value in var_list.items():
            for index, video in enumerate(channel_list[channel_name]):
                if key == video['video_id']: 
                    if value.get() == 1:
                        channel_list[channel_name][index]['seen'] = True
                    elif value.get() == 0:
                        channel_list[channel_name][index]['seen'] = False

        write_json(channel_list, json_location)


    def check_all():
        for key, value in var_list.items():
            value.set(1)

    def uncheck_all():
        for key, value in var_list.items():
            value.set(0)

    canvas = tkinter.Canvas(window_name)
    scroll_y = tkinter.Scrollbar(window_name, orient='vertical', command=canvas.yview)
    frame = tkinter.Frame(canvas)

    frame_title = tkinter.Frame(window_name)
    frame_title.pack()

    #Make Title and Seen labels
    label_title = tkinter.Label(frame_title, text="Title", font=('Ariel', 20, 'bold'))
    label_title.grid(column=0, row=0, sticky="W")

    label_blanc = tkinter.Label(frame_title, text="           \t\t\t\t       ")
    label_blanc.grid(column=1, row=0)

    label_seen = tkinter.Label(frame_title, text="Seen", font=('Ariel', 20, 'bold'))
    label_seen.grid(column=2, row=0, sticky="E")

    #Make Save and Print buttons
    button_save = tkinter.Button(text="Save", command=save)
    button_save.pack()

    button_uncheck = tkinter.Button(text="Check all", command=check_all)
    button_uncheck.pack()

    button_check = tkinter.Button(text="uncheck all", command=uncheck_all)
    button_check.pack()

    #Make Label for title and checkbox for seen for every video
    label_channels=[]
    var_list={}

    for index, channel in enumerate(channel_list[channel_name]):
        #Make title shorter if too long
        title = channel['title']
        if len(title) > 57:
            title = title[0:57]

        #Make label for each title
        label_channels.append(tkinter.Label(frame, text=title).grid(column=0, row=index+1, sticky="W"))

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

    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')



    window_name.mainloop()
