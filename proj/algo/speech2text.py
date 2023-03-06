# -*- coding:utf-8 -*-

import os
import math
import warnings
warnings.filterwarnings('ignore')

import soundfile as sf

from pydub import AudioSegment
from pydub.utils import make_chunks
from paddlespeech.cli.asr.infer import ASRExecutor



class SpeechToText:
    def __init__(self, conf=None):
        self.conf = conf
        
        self.speech2 = 'speech2'
        self.text2 = 'text2'
        
        self.check_fold(os.path.join(self.conf['out_path'], self.speech2))
        self.check_fold(os.path.join(self.conf['out_path'], self.text2))
        
        self.min_per_split = 45
        
        self.asr = ASRExecutor()
    
    def list_audio(self, path=None):
        root_path = self.conf['input_path'] if path is None else path
        for audio in os.listdir(root_path):
            if not audio.endswith('wav'):
                continue
                
            yield audio, os.path.join(root_path, audio)
    
    def rewrite_audio(self):
        for _, audio_file in self.list_audio():
            data, samplerate = sf.read(audio_file)
            sf.write(audio_file, data, samplerate) 
    
    def single_convert_text(self, audo_file):
        result = self.asr(audio_file=audo_file, force_yes=True)
        return result
    
    @staticmethod
    def save_text(file_name, text):
        with open(file_name, 'w') as fid:
            fid.write(text)
    
    @staticmethod
    def speech_seconds(audio_file):
        audio = AudioSegment.from_wav(audio_file)
        return audio.duration_seconds
    
    @staticmethod
    def check_fold(folder_str, flag=True):
        if not os.path.exists(folder_str) and flag:
            os.makedirs(folder_str)
    
    def single_spilt(self, audio, from_min, to_min, save_file):
        t1 = from_min*1000
        t2 = to_min*1000
        split_audio = audio[t1:t2]
        split_audio.export(save_file, format='wav')
        
    def split_audio(self, audio_file):
        audio = AudioSegment.from_wav(audio_file)
        temp_str =audio_file.split('/')[-1].split('.')[0]
        total_mins  = math.ceil(self.speech_seconds(audio_file))
        for i in range(0, total_mins, self.min_per_split):
            save_file = os.path.join(self.conf['out_path'], 
                                     self.speech2, 
                                     temp_str+'_{}'.format(i)+'.wav'
                                    )
            self.single_spilt(audio, i, i+self.min_per_split, save_file)
                
        if i < total_mins-1:
            self.single_spilt(audio, i, i+self.min_per_split, save_file)
    
    def multi_split_audio(self):
        for _, audio_file in self.list_audio():
            self.split_audio(audio_file)
        
    def run(self):
        self.rewrite_audio()
        print('rewrite done')
        
        self.multi_split_audio()
        print('audio split done!')
        
        audio_path = os.path.join(self.conf['out_path'], self.speech2)
        for audio, audio_file in self.list_audio(audio_path):
            save_file = os.path.join(self.conf['out_path'], 
                                     self.text2,
                                     audio.split('.')[0]+'.txt',
                                    )
            # print('auido >>> ', audio_file)
            text = self.single_convert_text(audio_file)
            self.save_text(save_file, text)
            
            # print('text <<< ', save_file)

    
if __name__ == "__main__":
    conf = {
        'input_path': 'your_audio_path',
        'out_path': 'write_text_path',
    }
    
    stt = SpeechToText(conf)
    stt.run()
    