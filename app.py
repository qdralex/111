from flask import Flask, request, redirect, render_template
from utils import *
from PIL import Image
from matplotlib import cm
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from models import *
import cv2
import os
import uuid
import datetime
import traceback
#import DbManager
from db import *
#import torch
#import torchvision
#import io
#import base64
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import OneHotEncoder
#import tensorflow as tf
#


app = Flask(__name__)

result_dir = 'result//'
original_suf = '_original'
jpg_ext = '.jpg'


if not os.path.isdir(result_dir):
    os.mkdir(result_dir)

model_loaded = Sequential()
model_loaded = keras.models.load_model('brain.keras')



@app.route("/")
def index():
    return render_template('index.html')

@app.route('/process', methods = ['POST'])
def process():

    imgParameter = request.files['imgParameter']

    
    try:
        pil_image = Image.open(imgParameter)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        errorName = e
        stackTrace = traceback.format_exc()
        return render_template('error.html', errorName = errorName, stackTrace = stackTrace)
    
    
    imgOriginal = img2byte(pil_image)
    input_np = np.array(pil_image, dtype=np.float32)
    
    file_name = str(uuid.uuid4())    
    original_file_path = result_dir+file_name+jpg_ext

    print('original_file_path='+original_file_path)

    # original_img_reshaped_pil = Image.fromarray(original_img_reshaped, mode="L")
    # original_img_reshaped = original_img.reshape(original_img.shape[0], original_img.shape[1])
    cv2.imwrite(original_file_path, input_np)
    
    x = np.array(pil_image.resize((128,128)))

    x = x.reshape(1,128,128,3)

    res = model_loaded.predict_on_batch(x)

    classification = np.where(res == np.amax(res))[1][0]

    if classification==0:
        predict = (str(res[0][classification]*100) + '% предсказания, что заболевание присутствует')  
        print(predict)
    else:
        predict = (str(res[0][classification]*100) + '% предсказания, что заболевания нет')          
        print(predict)
        
    db_manager = DbManager('db\\db1.db')
    y = datetime.datetime.now()
    date, time = str(y).split(' ')
    print(date, time)

    usage_id = db_manager.get_row_qty()

    print("usage_id=" + str(usage_id))
    if(usage_id == None):
        usage_id = 0

    print("usage_id="+str(usage_id))

    db_manager.insert_result(original_file_path, predict, usage_id, date, time)

    db_manager.insert_history(usage_id, date, time)

    return render_template('process.html', predict = predict, imgOriginal = imgOriginal.decode('utf-8'))

@app.route("/result")
def result():
    db_manager = DbManager('db\\db1.db')
    all_result_with_usage = db_manager.get_all_result_with_usage()

    data = []
    for res in all_result_with_usage:
        original_img = cv2.imread(res.original_path, cv2.IMREAD_GRAYSCALE)
        original_img_reshaped = original_img.reshape(original_img.shape[0], original_img.shape[1])
        original_img_reshaped_pil = Image.fromarray(original_img_reshaped, mode="L")
        original_img_byte = img2byte(original_img_reshaped_pil).decode('utf-8')

        print(res.predict)

        data.append(ResultWeb(original_img_byte, res.predict, res.date, res.time))
    
    return render_template('result.html', data = data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
