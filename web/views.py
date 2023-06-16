from flask import Blueprint, render_template, request, flash, jsonify, abort
#from flask_login import login_required, current_user
from .models import Diary
from . import db
from google.cloud import storage
#Importing library
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import requests
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
from google.cloud import translate_v2 as translate

import contractions
import spacy
import re
import string
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#recommendation
import pandas as pd
import numpy as np

views = Blueprint('views', __name__)

# Mendownload model dari bucket
def download_model():
    url = 'https://storage.googleapis.com/healthdiary-c23-ps111/model.h5'
    response = requests.get(url)
    with open('model.h5', 'wb') as f:
        f.write(response.content)

# Mendownload tokenizer dari bucket
def download_tokenizer():
    url = 'https://storage.googleapis.com/healthdiary-c23-ps111/tokenizer.pickle'
    response = requests.get(url)
    with open('tokenizer.pickle', 'wb') as f:
        f.write(response.content)

# Mendownload credentials.json dari bucket
def download_credentials():
    url = 'https://storage.googleapis.com/healthdiary-c23-ps111/credentials.json'
    response = requests.get(url)
    with open('credentials.json', 'wb') as f:
        f.write(response.content)

# Cek apakah file credentials.json sudah ada
if not os.path.exists('credentials.json'):
    download_credentials()

    # Memuat model dan tokenizer
def load_model_tokenizer():
    download_model()
    download_tokenizer()
    download_credentials()

    new_model = tf.keras.models.load_model('model.h5')

    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    return new_model, tokenizer

def download_credentials():
    url = 'https://storage.googleapis.com/healthdiary-c23-ps111/credentials.json'
    response = requests.get(url)
    with open('credentials.json', 'wb') as f:
        f.write(response.content)

# Memuat model dan tokenizer
new_model, tokenizer = load_model_tokenizer()


@views.route('/mydiary', methods=['GET'])
#@login_required
def mydiary():
       # user_id = current_user.id
        diaries = Diary.query.filter_by(id=id).all()
        diary_list = []
        for diary in diaries:
            diary_data = {
                'id': diary.id,
                'data': diary.data,
                'date': diary.date,
                'Anxiety': diary.Anxiety,
                'Depresi': diary.Depresi,
                'Lonely': diary.Lonely,
                'Normal': diary.Normal,
                #'user_id': diary.user_id,
                'rekomendasi': diary.rekomendasi
            }
            diary_list.append(diary_data)
        return jsonify({'status': 'success', 'data': diary_list}), 200

@views.route('/adddiary', methods=['POST'])
#@login_required
def adddiary():
        diary = request.form.get('diary')

        if len(diary) < 1:
            flash('Your Diary is too short!', category='error')
            return {'status': 'error', 'message': 'Your Diary is too short!'}
            response.status_code = 400
        else:
            
            # Fungsi untuk melakukan preprocessing pada teks
            en = spacy.load('en_core_web_sm')
            stopwords = en.Defaults.stop_words

            def preprocessing(sentence):
                # Convert text to lowercase, contraction, remove numbers, remove punctuation
                sentence = re.sub(r'\d+', '', contractions.fix(sentence.lower()).translate(str.maketrans('', '', string.punctuation)))

                # Remove stopwords
                text = [word for word in sentence.split() if word not in stopwords]

                # Remove extra whitespace
                sentence = ' '.join(text).strip()

                return sentence

            # Inisialisasi klien Cloud Translation
            translate_client = translate.Client()

            # Fungsi untuk menerjemahkan teks menggunakan Google Cloud Translation API
            def translate_text(text, target_language):
                translation = translate_client.translate(
                    text,
                    target_language=target_language
                )
                translated_text = translation['translatedText']
                return translated_text

            # Menerjemahkan teks input ke bahasa Inggris
            translated_text = translate_text(diary, 'en')

            # Cek hasil translate
            print(translated_text)

            # Melakukan preprocessing pada teks
            preprocessed_text = preprocessing(translated_text)

            # Cek hasil preprosessing
            print(preprocessed_text)

            # Prediksi menggunakan model dan tokenizer yang dimuat
            def predict_text_sentiment(seed_text, model, tokenizer):
                token_list = tokenizer.texts_to_sequences([seed_text])[0]
                # Pad the sequences
                token_list = pad_sequences([token_list], padding='post')
                # Get the probabilities of predicting a word
                predicted = model.predict(token_list, verbose=0)[0]
                #print('Probabilitas:')
                #print('Anxiety : {:.2%}'.format(predicted[0]))
                #print('Depresi : {:.2%}'.format(predicted[1]))
                #print('Lonely : {:.2%}'.format(predicted[2]))
                #print('Normal : {:.2%}'.format(predicted[3]))
                return predicted

            # Menjalankan prediksi menggunakan model
            predict=predict_text_sentiment(preprocessed_text, new_model, tokenizer)
            anxiety=predict[0]
            depresi=predict[1]
            lonely=predict[2]
            normal=predict[3]

            def recommendation(sentence, csv_url):
                # Membaca file CSV dari URL
                df = pd.read_csv(csv_url)

                df_new = df.copy()
                df_new.loc[len(df_new['Motivation'])] = [sentence]
                df_new['Motivation'] = df_new['Motivation'].apply(preprocessing)
                CV = CountVectorizer()
                converted_metrix = CV.fit_transform(df_new['Motivation'])
                cosine_sim = cosine_similarity(converted_metrix)
                score = list(enumerate(cosine_sim[len(df_new['Motivation']) - 1]))
                # sort in descending order
                sorted_score = sorted(score, key=lambda x: x[1], reverse=True)
                sorted_score = sorted_score[1:]
                i = 0
                recom_motivation = []
                for item in sorted_score:
                    recom_motivation.append(df.iloc[item[0]].values[0])
                    i = i + 1
                    if i > 4:
                        break
                return random.choice(recom_motivation)
                

            # URL publik objek CSV
            csv_url = 'https://storage.googleapis.com/healthdiary-c23-ps111/quote.csv'

            #Mendapatkan rekomendasi quote
            rekom=recommendation(preprocessed_text, csv_url)

            new_diary = Diary(data=diary, Anxiety=anxiety*100, Depresi=depresi*100, Lonely=lonely*100, Normal=normal*100, rekomendasi=rekom)
            datapredict=np.array(predict)
            predict_list=datapredict.tolist()
            db.session.add(new_diary) 
            db.session.commit()
            flash('Diary added!', category='success')
            return jsonify({'status': 'success', 'diary': diary, 'hasil_predict': predict_list, 'recommendation': rekom}), 200

    #return render_template("home.html", user=current_user)

