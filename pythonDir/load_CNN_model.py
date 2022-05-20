import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import layers
import numpy as np
import pandas as pd
import os
import json
from tqdm import tqdm

# 경로 정의
DATA_IN_PATH = './data_in/'
DATA_OUT_PATH = './data_out/'
DATA_CONFIGS = 'real_data_configs_38.json'
STTResult_IN_PATH = '/var/www/html/webpage/pythonDir/csvData/'
SAVE_WEIGHTS_FILE_NM = 'weights.h5' #저장된 best model 이름=일단 불러옴

INPUT2_TEST_DATA = 'STT_input_09.npy'
model = tf.keras.models.load_model(filepath='/var/www/html/webpage/pythonDir/data_out/cnn_classifier_krmy_model.tf')
test_input2 = np.load(open(DATA_IN_PATH + INPUT2_TEST_DATA, 'rb'))
test_input2 = pad_sequences(test_input2, maxlen=test_input2.shape[1])

results = model.predict(test_input2)
return_data = pd.read_csv(STTResult_IN_PATH + 'STTResult.csv', header=0)
return_data['results'] = results

return_data.to_csv('clova_result.csv', index=False)
