
import os
import numpy as np
import librosa
#model lib
import tensorflow as tf
# bash lib
from subprocess import call
# my functions
from record import Record
from split import Split_sound


def clean():
	"""
	This function removes old run data cunks and numpy files
	"""
	print("Started cleaning....")
	rc = call("./clean.sh", shell=True)
	print("Cleaning done.")



def load_model():
	"""
	Load .h5 models
	"""
	model = tf.keras.models.load_model("model/ASR_01.h5")
	# print(model.summary())
	return model

def wav2mfcc(file_path, max_len=44, n_mfcc=20):
	"""
	convert file to wav2mfcc using the algorithm 
	Mel-frequency cepstral coefficients (MFCC)
	"""
	wave, sr = librosa.load('Chunk/'+file_path, mono=True)
	wave = np.asfortranarray(wave[::3])
	mfcc = librosa.feature.mfcc(wave, sr=16000, n_mfcc=n_mfcc)
	if (max_len > mfcc.shape[1]):
   		pad_width = max_len - mfcc.shape[1]
   		mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
	else:
   		mfcc = mfcc[:, :max_len]
	
	return mfcc


def data_to_array():
	"""

	"""
	path = 'Chunk/'
	for wavfile in os.listdir(path):
		mfcc = wav2mfcc(wavfile, max_len = 44, n_mfcc=20)
		np.save('Data/'+wavfile.split(".")[0]+'.npy', mfcc)

def get_data(chunk):
	"""
	
	"""
	data_to_array()
	file_path = 'Data/'
	list_file = os.listdir(file_path)
	X = np.load(file_path+list_file[0])
	for i, label in enumerate(list_file[1:]):
		x = np.load(file_path+label)
		X = np.vstack((X, x))
	return X

def get_labels():
	dataLabels = ['tree','house','zero','bed','yes','four','up','stop','no','wow','nine','happy','follow', 'visual','cat','two', 'forward', 'down','right', 'marvin', 'seven', 'go', 'three',  'backward', 'on', 'dog', 'one', 'sheila', 'eight', 'bird', 'six', 'learn', 'off', 'left', 'five']
	return dataLabels

def predictStream(X):
	model = load_model()
	y = model.predict(X)
	for iss in y:
		temp = max(iss) 
		res = [i for i, j in enumerate(iss) if j == temp]
		val = res[0]
		print(get_labels()[val])

def streamCOnvert():
	RATE = 44100
	CHUNK = int(RATE/20) # RATE / number of updates per second
	p=pyaudio.PyAudio()
	stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)
	for i in range(int(20*RATE/CHUNK)):
		predictStream(stream)
	stream.stop_stream()
	stream.close()
	p.terminate()


if __name__=="__main__": 
	channels = 1
	max_len = 44
	buckets = 20
	# Cleaning all teh old recordings
	clean()
	streamCOnvert()  