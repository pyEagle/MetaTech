# -*- coding:utf-8 -*-

import os

import tensorflow_text as text

import tensorflow as tf
import tensorflow_hub as hub

class TextEmbeddingBert:

    def __init__(self, conf=None):
        self.conf = conf
        
        self.load_model()
        
    def load_model(self):
        model_file = self.conf.get('bert_model')
        self.bert = hub.load(model_file)
        
        sentence_file = self.conf.get('sentence')
        self.sentence = hub.load(sentence_file)
    
    def get_single_text_embedding(self, text):
        inputs = self.sentence(text)
        output = self.bert(inputs)['pooled_output']
        
        return output
    
    def get_multi_text_embedding(self, text_list):
        inputs = self.sentence(text_list)
        output = self.bert(inputs)['pooled_output']
        
        return output.numpy()
