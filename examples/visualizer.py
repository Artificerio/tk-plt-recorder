import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave

CHUNK = 1024 * 4             # samples per frame
FORMAT = pyaudio.paInt16     # bytes per sample
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second
SECONDS = 5
# Signal range is -32k to 32k
# limiting amplitude to +/- 4k
AMPLITUDE_LIMIT = 4096
FILENAME = 'output.wav'

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	output=True,
	frames_per_buffer=CHUNK
)

# Use interactive mode
plt.ion()
fig, ax1, = plt.subplots(1, figsize=(15, 7))
# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

# create a line object with random data
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('amplitude')
ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
ax1.set_xlim(0, 2 * CHUNK) # because we read half of the possible 
# plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])

print('stream started')

frames = []
if __name__ == '__main__':
    for i in range(0, int(RATE / CHUNK * SECONDS) + 1):
        data = stream.read(CHUNK)
        frames.append(data)
        data_np = np.frombuffer(data, dtype=np.int16)
        line.set_ydata(data_np)
        fig.canvas.draw()
        fig.canvas.flush_events()
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('finished recording')

    wf = wave.open(FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
