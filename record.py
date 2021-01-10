# Importing libs
import sounddevice as sd 
from scipy.io.wavfile import write 

def Record():
	# Sampling frequency
	freq = 44100
	# Recoding Duration
	duration = 10

	audio_name = "recording.wav"

	# Start the recorder
	recording =  sd.rec(int(duration*freq),samplerate=freq, channels=2)
	print("Start")
	sd.wait()
	print("Stop")
	# Saving the file 
	write(audio_name, freq, recording)
	
