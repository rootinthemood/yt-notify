import json
import os
import tkinter
from functions import add_channel, return_id_title_seen, set_channel_seen, print_id_title_seen, remove_channel, write_json
from scrapevideos import scrape_channel, scrape_all_channels ,update_channel, update_all_channels
from gui import all_videos_window

CHANNELS = dict()
CHANNEL_JSON = "test.json"

if not os.path.isfile(CHANNEL_JSON):
    with open(CHANNEL_JSON, 'w') as f:
        to_write = {'channels': []}
        json.dump(to_write, f)

with open(CHANNEL_JSON, 'r') as f:
    CHANNELS = json.load(f)

#set_channel_seen("NileBlue", CHANNELS, True)
#scrape_channel("NileBlue", CHANNELS)
#write_json(CHANNELS, CHANNEL_JSON)

#####################--------GUI--------#########################
#root = tkinter.Tk()
#root.title("yt-notify")
#root.minsize(width=600, height=600)
#root.config(padx=20, pady=20)

for channel in CHANNELS:
    if channel == "channels":
        continue
    all_videos_window(CHANNELS, channel, CHANNEL_JSON)
#all_videos_window(CHANNELS, "V for Valentine")
#all_videos_window(CHANNELS, "NileBlue", "test2")
#def save():
#    for key, value in var_list.items():
#        for index, video in enumerate(CHANNELS['NileBlue']):
#            if key == video['video_id']: 
#                if value.get() == 1:
#                    CHANNELS['NileBlue'][index]['seen'] = True
#                elif value.get() == 0:
#                    CHANNELS['NileBlue'][index]['seen'] = False
#
#def print_channels():
#    os.system('clear')
#    print(CHANNELS)
#
#canvas = tkinter.Canvas(root)
#scroll_y = tkinter.Scrollbar(root, orient='vertical', command=canvas.yview)
#
#frame = tkinter.Frame(canvas)
#
#frame_title = tkinter.Frame(root)
#
##Print titles
#label_title = tkinter.Label(frame_title, text="Title", font=('Ariel', 20, 'bold'))
#label_title.grid(column=0, row=0, sticky="W")
#
#label_blanc = tkinter.Label(frame_title, text="           \t\t\t\t       ")
#label_blanc.grid(column=1, row=0)
#
#label_seen = tkinter.Label(frame_title, text="Seen", font=('Ariel', 20, 'bold'))
#label_seen.grid(column=2, row=0, sticky="E")
#
#frame_title.pack()
#
#button_save = tkinter.Button(text="Save", command=save)
#button_save.pack()
#
#button_print = tkinter.Button(text="Print", command=print_channels)
#button_print.pack()
#
#
##Print checkbox for each video
#label_channels=[]
#var_list={}
#
#for index, channel in enumerate(CHANNELS['NileBlue']):
#    label_channels.append(tkinter.Label(frame, text=channel['title']).grid(column=0, row=index+1, sticky="W"))
#    if channel['seen'] == True:
#        var_list[channel['video_id']]= tkinter.IntVar(frame, value=1)
#    else:
#        var_list[channel['video_id']] = tkinter.IntVar(frame, value=0)
#
#    tkinter.Checkbutton(frame, variable=var_list[channel['video_id']]).grid(column=1, row=index+1)
#
#canvas.create_window(0, 0, anchor='nw', window=frame)
#canvas.update_idletasks()
#canvas.configure(scrollregion=canvas.bbox('all'),
#                 yscrollcommand=scroll_y.set)
#
#canvas.pack(fill='both', expand=True, side='left')
#scroll_y.pack(fill='y', side='right')
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#root.mainloop()
#
##def write_json(channel_list, json_location):
##    with open (CHANNEL_JSON, 'w') as f:
##        json.dump(CHANNELS, f, indent=2)
#
#
##add_channel(CHANNELS)
##scrape_all_channels(CHANNELS)
##remove_channel("V for Valentine", CHANNELS)        
##print(CHANNELS)
##update_all_channels(CHANNELS)
##for channel in CHANNELS:
##    if channel == "channels":
##        continue
##    update_channel(channel, CHANNELS)
##update_channel("NileBlue", CHANNELS)
##print(CHANNELS['NileBlue'])
##print(len(CHANNELS['NileBlue']))
##print(CHANNELS['NileBlue'][0])
#
##scrape_all_channels(CHANNELS)
##scrape_channel("V for Valentine", CHANNELS)
##print(CHANNELS)
##print(CHANNELS['V for Valentine'])
##set_channel_seen("NileBlue", CHANNELS, True)
##print_id_title_seen("NileBlue", CHANNELS)
#write_json(CHANNELS, CHANNEL_JSON)
#
#
##print(CHANNELS)
