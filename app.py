from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS
import re
import time
from glob import glob
from PIL import Image
import numpy as np
import os
import cv2
import uuid
import json
from PIL import Image
from datetime import datetime
from model_post_type import ocr as OCR
from model_postE_invoice import ocr as ocr_E
from model_postM_invoice import ocr as ocr_M
from apphelper.image import union_rbox
from application.invoice_e import invoice_e
from application.invoice_m import invoice_m
import pytz
port = 11111
allowed_extension = ['jpg','png','JPG']

# Flask
app = Flask(__name__)
CORS(app, resources=r'/*')

# 构建接口返回结果
def build_api_result(code, message, data,file_name,ocr_identify_time):
    result = {
        "code": code,
        "message": message,
        "data": data,
        "FileName": file_name,
        "ocrIdentifyTime": ocr_identify_time
    }
    return jsonify(result)

# 检查文件扩展名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension


# 增值税发票OCR识别接口
@app.route('/invoice-ocr', methods=['POST'])
def invoice_ocr():
    # 校验请求参数
    if 'file' not in request.files:
        return build_api_result(101, "请求参数错误", {},{},{})

    # 获取请求参数
    file = request.files['file']
    invoice_file_name = file.filename
    
    # 检查文件扩展名
    if not allowed_file(invoice_file_name):
        return build_api_result(102, "失败，文件格式问题", {},{},{})
   
    upload_path = "test"
    whole_path = os.path.join(upload_path,invoice_file_name)
    file.save(whole_path)
    
    #去章处理方法
    def remove_stamp(path,invoice_file_name):
        img = cv2.imread(path,cv2.IMREAD_COLOR)
        B_channel,G_channel,R_channel=cv2.split(img)     # 注意cv2.split()返回通道顺序
        _,RedThresh = cv2.threshold(R_channel,170,355,cv2.THRESH_BINARY)
        cv2.imwrite('./test/RedThresh_{}.jpg'.format(invoice_file_name),RedThresh)
    
    def Recognition_invoice(path):
        '''
        识别发票类别
        :param none:
        :return: 发票类别
        '''
        remove_stamp(path,invoice_file_name)
        img1 = './test/RedThresh_{}.jpg'.format(invoice_file_name)
        img1 = cv2.imread(img1)
        result_type = OCR(img1)
        result_type = union_rbox(result_type, 0.2)
        
        print(result_type)
        
        if len(result_type) > 0:
            N = len(result_type)
            for i in range(N):
                txt = result_type[i]['text'].replace(' ', '')
                txt = txt.replace(' ', '')
                type_1 = re.findall('电子普通',txt)
                type_2 = re.findall('普通发票',txt)
                type_3 = re.findall('专用发票',txt)
                if type_1 == None:
                    type_1 = []
                if type_2 == None:
                    type_2 = []
                if type_3 == None:
                    type_3 = []
            print(type_1)
            print(type_2)
            print(type_3)
            if len(type_1) > 0:
                return 1
            else:
                return 2
        elif len(result_type)==0:
            return 2
    
    Recognition_invoice = Recognition_invoice(whole_path)
    img = cv2.imread(whole_path)
    h, w = img.shape[:2]
    if Recognition_invoice == 1:
        result = ocr_E(img)
        res = invoice_e(result)
        res = res.res
    elif Recognition_invoice == 2:
        result = ocr_M(img)
        res = invoice_m(result)
        res = res.res
    else:
        res = []
    if len(res) > 0:
        tz = pytz.timezone('Asia/Shanghai') #东八区
        ocr_identify_time = datetime.fromtimestamp(int(time.time()),pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        return build_api_result(100, "识别成功" , res, invoice_file_name,ocr_identify_time)
    elif len(res) == 0:
        return build_api_result(104, "识别为空！" ,{},{},{})
        
if __name__ == "__main__":
    # Run
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
