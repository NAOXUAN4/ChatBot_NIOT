import requests


class GenshinTTS():
    def __init__(self):
        self.API_URL = 'https://genshinvoice.top/api'
        self.txt=''  #apiport.res_text
        self.spk="派蒙"
        self.length=1
        self.format="wav"
        self.noise=0.5
        self.noisew=0.9
        self.sdq_ratio=0.2

    def genshin_tts(self,txt):
        """"调用GenshinVoice API进行TTS"""

        params = {
            'speaker': self.spk,
            'text': txt,
            'format': self.format,
            'length': self.length,
            'noise': self.noise,
            'noisew': self.noisew,
            'sdp_ratio': self.sdq_ratio,
        }

        response = requests.get(self.API_URL,params=params)
        audio=response.content
        return [response.url, audio]
