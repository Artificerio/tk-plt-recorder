import os
import matplotlib.pyplot as plt
import numpy as np
import wave
import secrets
from datetime import datetime
from tkinter import *
import pyaudio


APP_PATH = os.getcwd() + '/recordings'


class App:
    def __init__(self, root):
        root.title('voice recorder')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.geometry("400x400")

        self.my_rec = Recording()
        self.my_rec.create_rec_dir()
        self.my_button = Button(root, text='Record voice', command=self.my_rec.record_and_plot)
        self.finder_button = Button(root, text='Open finder', command=self.open_explorer)
        self.dir_button = Button(root, text='Update directory', command=self.update_dir)
        self.open_rec = Button(root, text='Listen', command=self.listen)
        self.my_label = Label(root, text='Search files')
        self.my_entry = Entry(root, font=('Helvetica', 14), width=50)
        self.my_listbox = Listbox(root, width=50, font=('Helvetica', 14))
        self.files = [os.path.basename(f.path) for f in os.scandir(APP_PATH) if f.is_file()]
        self.my_label.pack()
        self.my_entry.pack()
        self.my_listbox.pack(pady=10)
        self.my_button.pack()
        self.dir_button.pack()
        self.finder_button.pack(side='right')
        self.open_rec.pack(side='left')

        self.update(self.files)

        self.my_listbox.bind('<<ListboxSelect>>', self.fillout)
        self.my_entry.bind('<KeyRelease>', self.check)
    
    def update(self, data):
        self.my_listbox.delete(0, END)
        for file in data:
            self.my_listbox.insert(END, file)

    def fillout(self, *args):
        self.my_entry.delete(0, END)
        self.my_entry.insert(0, self.my_listbox.get(ACTIVE))
    
    def check(self, *args):
        typed = self.my_entry.get()
        if typed == '':
            data = self.files
        else:
            data = []
            for file in self.files:
                if typed.lower() in file.lower():
                    data.append(file)
        self.update(data)
    
    def update_dir(self):
        self.files = [os.path.basename(f.path) for f in os.scandir(APP_PATH) if f.is_file()]
        self.update(self.files)
    
    def open_explorer(self):
        file_to_open = APP_PATH + '/' + self.my_listbox.get(ACTIVE)
        os.system(f'open -R {file_to_open}')

    def listen(self):
        file_to_listen = APP_PATH + '/' + self.my_listbox.get(ACTIVE)
        if self.my_listbox.get(ACTIVE):
            os.system(f'ffplay {file_to_listen}')
    

class Recording:
    def __init__(self, rate=44100, seconds=1000, channels=1, chunk=1024 * 4,
                 frmt=pyaudio.paInt16, amp_limit=4096):
        self.rate = rate
        self.seconds = seconds
        self.channels = channels
        self.chunk = chunk
        self.format = frmt
        self.amp_limit = amp_limit
        self.rec_dir = os.getcwd() + r'/recordings'
        self.filetype = r'/*wav'

    def create_rec_dir(self):
        if not os.path.exists(self.rec_dir):
            os.makedirs(self.rec_dir)

    def create_plot(self):
        # interactive mode
        plt.ion()
        plt.rcParams["keymap.quit"] = "ctrl + w", "cmd + w", "q"
        self.fig, self.ax = plt.subplots(1, figsize=(4, 4))
        self.x = np.arange(0, 2 * self.chunk, 2)
        self.line, = self.ax.plot(self.x, np.random.rand(self.chunk), '-')

        # format axes
        self.ax.set_title('audio waveform')
        self.ax.set_xlabel('samples')
        self.ax.set_ylabel('amplitude')
        self.ax.set_ylim(-self.amp_limit, self.amp_limit)
        self.ax.set_xlim(0, 2 * self.chunk)

    def render_plot(self):
        self.p = pyaudio.PyAudio()

        # read data from mic
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            frames_per_buffer=self.chunk,
            input=True,
            output=True
        )
        self.frames = []
        for _ in range(0, int(self.rate / self.chunk * self.seconds) + 1):
            if plt.get_fignums():
                self.data = self.stream.read(self.chunk)
                self.frames.append(self.data)
                self.data_np = np.frombuffer(self.data, dtype=np.int16)
                self.line.set_ydata(self.data_np)
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def save_recording(self):
        os.chdir(self.rec_dir)
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        if os.path.exists(self.rec_dir + '/' + self.filename):
            print(f'file was saved as {self.filename}')
        wf.close()
        os.chdir('..')

    def update_name(self):
        self.id = secrets.token_hex(8)
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.filename = f'recording_{self.id}_{self.date}.wav'

    def record_and_plot(self):
        self.create_plot()
        self.render_plot()
        self.update_name()
        self.save_recording()
