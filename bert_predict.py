# %%
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import optimization  # to create AdamW optmizer
from official.modeling import tf_utils
from official import nlp
from official.nlp import bert
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
import datatable
from utils import *
# %%
pd.set_option('display.max_columns', None)

tf.get_logger().setLevel('ERROR')

gpus = tf.config.experimental.list_physical_devices('GPU')

if gpus:
  # 텐서플로가 첫 번째 GPU만 사용하도록 제한
    tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
    tf.config.experimental.set_memory_growth(gpus[0], True)
# %%
csv = pd.read_csv('./data/apply_exclusion.csv', index_col=0)
csv = csv.drop_duplicates('환자번호#1')

# %%
data = csv[csv['검사결과내용(최초1) #110'] != '']
data = data[data['검사결과내용(최초1) #110'].map(lambda x: map_fn(x)) != 0]
# %%
p = re.compile('[-=#)(:]')
data['processed_text'] = data['검사결과내용(최초1) #110'].map(lambda x: re.sub(p, '', x[1:]))
# %%
bert_model_name = 'experts_wiki_books' 
map_name_to_handle = {
    'experts_wiki_books':
        'https://tfhub.dev/google/experts/bert/wiki_books/2',
}
map_model_to_preprocess = {
    'experts_wiki_books':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
}

tfhub_handle_encoder = map_name_to_handle[bert_model_name]
tfhub_handle_preprocess = map_model_to_preprocess[bert_model_name]
bert_preprocess_model = hub.KerasLayer(tfhub_handle_preprocess)

# %%
def build_classifier_model():
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
    preprocessing_layer = hub.KerasLayer(tfhub_handle_preprocess, name='preprocessing')
    encoder_inputs = preprocessing_layer(text_input)
    encoder = hub.KerasLayer(tfhub_handle_encoder, trainable=True, name='BERT_encoder')
    outputs = encoder(encoder_inputs)
    net = outputs['pooled_output']
    net = tf.keras.layers.Dropout(0.1)(net)
    net = tf.keras.layers.Dense(1, activation='sigmoid', name='classifier')(net)
    return tf.keras.Model(text_input, net)
classifier_model = build_classifier_model()
batch_size = 32
epochs = 3
# steps_per_epoch = len(train) // batch_size
steps_per_epoch = len(data) // batch_size
num_train_steps = steps_per_epoch * epochs
num_warmup_steps = int(0.1*num_train_steps)

init_lr = 3e-5
optimizer = optimization.create_optimizer(init_lr=init_lr,
                                          num_train_steps=num_train_steps,
                                          num_warmup_steps=num_warmup_steps,
                                          optimizer_type='adamw')

classifier_model.compile(optimizer=optimizer,
                         loss='binary_crossentropy',
                         metrics=['accuracy'])
# %%
classifier_model.load_weights('./../Helicobacter/weight/divide_sklearn.h5')
# %%
prediction = classifier_model.predict(data['processed_text'])

temp = prediction.copy()
temp = np.where(temp < 0.5, 0, 1)
# %%
data['result'] = temp
# %%
data['result'].to_csv('./data/analysis_bert_predict.csv')
# %%
