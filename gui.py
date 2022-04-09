import tkinter

root = tkinter.Tk()
root.title("yt-notify")
root.geometry("400x900")


def get_size():
    width = root.winfo_width()
    height= root.winfo_height()
    print(width, height)
    root.after(1000, get_size)

root.after(1000, get_size)










root.mainloop()
