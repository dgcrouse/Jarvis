from JarvisIOHandler import JarvisIOHandler
from pocketsphinx import Decoder
import speech_recognition as sr
import pyaudio
import pyvona


class VoiceIOHandler(JarvisIOHandler):
	
	def __init__(self):
		JarvisIOHandler.__init__(self)
		hmm = '/usr/local/share/pocketsphinx/model/en-us/en-us'
		dic ='/usr/local/share/pocketsphinx/model/en-us/cmudict-en-us.dict'
		lm ='/usr/local/share/pocketsphinx/model/en-us/en-us.lm.bin'

		config = Decoder.default_config()
		config.set_string('-hmm',hmm)
		config.set_string('-lm',lm)
		config.set_string('-dict',dic)
		config.set_string('-logfn','/dev/null')

		self.decoder = Decoder(config)

		self.microphone = pyaudio.PyAudio()

		pyvona_config = open('configs/pyvona.txt')
		pvcfg = pyvona_config.readlines()
		pyvona_config.close()
		self.voice = pyvona.create_voice(pvcfg[0].strip(),pvcfg[1].strip())
		self.voice.region = 'us-west'
		self.voice.voice_name='Brian'
		self.voice.sentence_break = 200

		googleSTT_config = open('configs/GoogleSTT.txt')
		self.key = googleSTT_config.readlines()[0].strip()
		googleSTT_config.close()
		self.recognizer = sr.Recognizer()
		with sr.Microphone() as source:
			self.recognizer.adjust_for_ambient_noise(source)

	def waitForInput(self):
		if self._isLowPower:
			utt = ''
			stream = self.microphone.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
			stream.start_stream()
			in_speech_bf = True
			self.decoder.start_utt()
			while True:
				buf = stream.read(1024)
				if buf:
					self.decoder.process_raw(buf, False, False)
					if self.decoder.get_in_speech() != in_speech_bf:
						in_speech_bf = self.decoder.get_in_speech()
						if not in_speech_bf:
							self.decoder.end_utt()
							try:
								if  self.decoder.hyp().hypstr != '':
									utt = self.decoder.hyp().hypstr
									break
							except AttributeError:
								pass
							self.decoder.start_utt()
			stream.stop_stream()
			stream.close()
			print utt
			return utt.lower().strip()
		
		else:
			with sr.Microphone() as source:
				print 'Listening'
				audio = self.recognizer.listen(source)

			print 'Recognizing...'
			try:
				rec = self.recognizer.recognize_google(audio,key=self.key).lower().strip()
				print rec
				return rec
			except sr.UnknownValueError:
				print("Google Speech Recognition could not understand audio")
				return 'CNU'
			except sr.RequestError as e:
				print("Could not request results from Google Speech Recognition service; {0}".format(e))
				return 'CNC'
			

	def output(self,text_to_output):
		self.voice.speak(text_to_output)