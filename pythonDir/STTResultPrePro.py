import numpy as np 
import pandas as pd
import os
import seaborn as sns
import re
import json
from konlpy.tag import Okt
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer

from soynlp.normalizer import *

DATA_IN_PATH = './csvData/'
test_data = pd.read_csv(DATA_IN_PATH+'STTResult.csv', header = 0)
test_length = test_data['sentence'].astype(str).apply(len)


def cleanse(text):
    pattern = re.compile(r'\s+')
    text = re.sub(pattern, ' ', str(text))
    text = re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ0-9]', '', str(text))
    return text

def preprocessing(sentence, okt, remove_stopwords = False, stop_words = []):
    # 함수의 인자는 다음과 같다.
    # sentence : 전처리할 텍스트
    # okt : okt 객체를 반복적으로 생성하지 않고 미리 생성후 인자로 받는다.
    # remove_stopword : 불용어를 제거할지 선택 기본값은 False
    # stop_word : 불용어 사전은 사용자가 직접 입력해야함 기본값은 비어있는 리스트
    
    # 1. 한글 및 공백을 제외한 문자 모두 제거.
    sentence_text = repeat_normalize(sentence, num_repeats=2)
    
    # 2. okt 객체를 활용해서 형태소 단위로 나눈다.
    wd_sentence = okt.morphs(sentence_text, stem=True)
    
    if remove_stopwords:
        
        # 불용어 제거(선택적)
        wd_sentence = [token for token in wd_sentence if not token in stop_words]
        
   
    return wd_sentence

stop_words = [ '은', '는', '이', '가', '하', '아', '것', '들','의', '있', '되', '수', '보', '주', '등', '한']
okt = Okt()
test_data['sentence'] = test_data['sentence'].apply(cleanse)

clean_test_sentence = []

for review in test_data['sentence']:
    # 비어있는 데이터에서 멈추지 않도록 string인 경우만 진행
    if type(review) == str:
        clean_test_sentence.append(preprocessing(review, okt, remove_stopwords = True, stop_words=stop_words))
    else:
        clean_test_sentence.append([])  #string이 아니면 비어있는 값 추가
        
clean_test_onlysentence_df = pd.DataFrame({'sentence':clean_test_sentence})

tokenizer = Tokenizer()

clean_train_data = pd.read_csv(DATA_IN_PATH + 'real_train_38.csv')
clean_train_sentence = []
clean_train_sentence = clean_train_data['text']
array_text = []
print("시발")
for arr in clean_train_data['text']:
    array_text.append(eval(arr))

tokenizer.fit_on_texts(array_text) ###only train data만 단어사전에 
test_sequences = tokenizer.texts_to_sequences(clean_test_sentence)

word_vocab = tokenizer.word_index # 단어 사전 형태
# word_vocab["<PAD>"] = 0

MAX_SEQUENCE_LENGTH = 38 #문장 최대 길이, 중간값 지정

test_inputs = pad_sequences(test_sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post') #test data 벡터화

DATA_IN_PATH = './data_in/'
from collections import OrderedDict

TEST_INPUT_DATA = 'STT_input_09.npy'
TEST_CLEAN_DATA = 'STT_clean_09.csv'

np.save(open(DATA_IN_PATH + TEST_INPUT_DATA, 'wb'), test_inputs)
clean_test_onlysentence_df.to_csv(DATA_IN_PATH +TEST_CLEAN_DATA, index = False)