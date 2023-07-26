import tkinter

def label1(root):
    label = tkinter.Label(root, text = "correct")
    label.pack()

def Window2():
    window1 = tkinter.Tk()
    window1.title("start")
    label = tkinter.Label(window1, text= "how do you spell this Sh--ld")
    label.pack()
    points = 0
    i = points + 1
    button = tkinter.Button(window1, text = "ou", command = lambda root = window1: label1(root))
    button.pack()



window = tkinter.Tk()
window.title("menu")

button = tkinter.Button(window, text = "start", command = Window2)
button.pack()

window.mainloop()