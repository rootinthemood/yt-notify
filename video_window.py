import tkinter
import os
from functions import write_json
import webbrowser


def video_window(channel_list, channel_name, json_location):
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

    #Close window function
    def close():
        window_name.quit()

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
    button_check = tkinter.Button(text="check all", command=check_all, width=10)
    button_check.pack(side='bottom', anchor='e')

    #Uncheck button
    button_uncheck = tkinter.Button(text="uncheck all", command=uncheck_all)
    button_uncheck.pack(side='bottom', anchor='e')

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
