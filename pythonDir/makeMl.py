import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import layers
import numpy as np
import pandas as pd
import os
import h5py
import json
import time
from tqdm import tqdm

# 모델 선언 및 컴파일 
class CNNClassifier(tf.keras.Model):
    def __init__(self, **kargs):
        super(CNNClassifier, self).__init__(name=kargs['model_name'])
        self.embedding = layers.Embedding(input_dim=kargs['vocab_size'],output_dim=kargs['embedding_size'])
        self.conv_list = [layers.Conv1D(filters=kargs['num_filters'],kernel_size=kernel_size,padding='valid',activation=tf.keras.activations.relu,kernel_constraint=tf.keras.constraints.MaxNorm(max_value=3.))for kernel_size in [3,4,5]]
        self.pooling = layers.GlobalMaxPooling1D()
        self.dropout = layers.Dropout(kargs['dropout_rate'])
        self.fc1 = layers.Dense(units=kargs['hidden_dimension'],activation=tf.keras.activations.relu,kernel_constraint=tf.keras.constraints.MaxNorm(max_value=3.))
        self.pooling = layers.GlobalMaxPooling1D()
        self.dropout = layers.Dropout(kargs['dropout_rate'])
        self.fc2 = layers.Dense(units=kargs['hidden_dimension'],activation=tf.keras.activations.relu,kernel_constraint=tf.keras.constraints.MaxNorm(max_value=3.))
        self.pooling = layers.GlobalMaxPooling1D()
        self.dropout = layers.Dropout(kargs['dropout_rate'])
        self.fc3 = layers.Dense(units=kargs['output_dimension'],activation=tf.keras.activations.sigmoid,kernel_constraint=tf.keras.constraints.MaxNorm(max_value=3.))
    
    def call(self, x):
        x = self.embedding(x)
        x = self.dropout(x)
        x = tf.concat([self.pooling(conv(x)) for conv in self.conv_list], axis=-1)
        x = self.fc1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.fc3(x)      
        return x


# 경로 정의
DATA_IN_PATH = './data_in/'
DATA_OUT_PATH = './data_out/'
INPUT_TRAIN_DATA = 'real_train_input_38.npy'
LABEL_TRAIN_DATA = 'real_train_label_38.npy'
DATA_CONFIGS = 'real_data_configs_38.json'
STTResult_IN_PATH = '/var/www/html/webpage/pythonDir/csvData/'
SEED_NUM = 1234
tf.random.set_seed(SEED_NUM)
SAVE_FILE_NM = './weights.h5'

time.sleep(3)

train_input = np.load(open(DATA_IN_PATH + INPUT_TRAIN_DATA, 'rb'))
train_input = pad_sequences(train_input, maxlen=train_input.shape[1])
train_label = np.load(open(DATA_IN_PATH + LABEL_TRAIN_DATA, 'rb'),allow_pickle = True)
prepro_configs = json.load(open(DATA_IN_PATH + DATA_CONFIGS, 'rt', encoding='UTF8'))

# 모델 하이퍼파라미터 정의 
model_name = 'cnn_classifier_kr'
BATCH_SIZE = 512
NUM_EPOCHS = 10 #10
VALID_SPLIT = 0.1 #0.1
MAX_LEN = train_input.shape[1]

kargs = {'model_name': model_name,
        'vocab_size': prepro_configs['vocab_size'],
        'embedding_size': 32,
        'num_filters': 100, #100
        'dropout_rate': 0.5,
        'hidden_dimension': 250,
        'output_dimension':1}

model = CNNClassifier(**kargs)
model.compile(optimizer=tf.keras.optimizers.Adam(),loss=tf.keras.losses.BinaryCrossentropy(),metrics=[tf.keras.metrics.BinaryAccuracy(name='accuracy')])

# overfitting을 막기 위한 ealrystop 추가
earlystop_callback = EarlyStopping(monitor='val_accuracy', min_delta=0.0001,patience=2)
checkpoint_path = DATA_OUT_PATH + model_name + '/weights.h5'
checkpoint_dir = os.path.dirname(checkpoint_path)

if os.path.exists(checkpoint_dir):
    print("{} -- Folder already exists \n".format(checkpoint_dir))
else:
    os.makedirs(checkpoint_dir, exist_ok=True)
    print("{} -- Folder create complete \n".format(checkpoint_dir))
    

cp_callback = ModelCheckpoint(
    checkpoint_path, monitor='val_accuracy', verbose=1, save_best_only=True, save_weights_only=True)
    
history = model.fit(train_input, train_label, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS,
                    validation_split=VALID_SPLIT, callbacks=[earlystop_callback, cp_callback])

# 결과 평가하기 
INPUT_TEST_DATA = 'real_test_input_38.npy'
LABEL_TEST_DATA = 'real_test_label_38.npy'

test_input = np.load(open(DATA_IN_PATH + INPUT_TEST_DATA, 'rb'))
test_input = pad_sequences(test_input, maxlen=test_input.shape[1])
test_label_data = np.load(open(DATA_IN_PATH + LABEL_TEST_DATA, 'rb'))

model.load_weights(SAVE_FILE_NM)

INPUT2_TEST_DATA = 'STT_input_09.npy'
test_input2 = np.load(open(DATA_IN_PATH + INPUT2_TEST_DATA, 'rb'))
test_input2 = pad_sequences(test_input2, maxlen=test_input.shape[1])

results = model.predict(test_input2)
return_data = pd.read_csv(STTResult_IN_PATH + 'STTResult.csv', header=0)
return_data['results'] = results

return_data.to_csv('clova_result.csv', index=False)