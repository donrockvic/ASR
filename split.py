
# 
# Breaking down the word can be done by looking  
# at the pause in the waveform, but to save time 
# i am using pydub
# 

from pydub import AudioSegment
from pydub.silence import split_on_silence

def Split_sound():
	rec_file = AudioSegment.from_wav("recording.wav")
	audio_chunks = split_on_silence(rec_file,
					# silence time
					min_silence_len = 10,
					# if quiter then -16 dBFS, assumed silence
					silence_thresh = -16
					)

	for i,chunk in enumerate(audio_chunks):
		out_file = ".//Chunk//chunk{0}.wav".format(i);
		print("Exporting"+out_file)
		# print(type(out_file))
		chunk.export(out_file, format="wav")
