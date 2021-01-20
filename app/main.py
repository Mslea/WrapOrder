from pyzbar import pyzbar
import cv2

import json
import io
import numpy as np
from flask import Flask, jsonify, request

from PIL import Image, ImageOps
import base64
import re
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

print("load1")


def predict_ja(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    # img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    # find the barcodes in the image and decode each of the barcodes
    barcodes = pyzbar.decode(img)
    # cv2.imshow("gray",img)
    # cv2.waitKey()
    s = []
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        # (x, y, w, h) = barcode.rect
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
        #     0.5, (0, 0, 255), 2)
        # print the barcode type and data to the terminal
        s.append(barcodeData)
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    print(s)
    return s


@app.route('/predict', methods=['POST'])
def predict():
     if request.method == 'POST':
        # print("ha/hahahah")
        # print(request.data)
        # date = jsonify.load1
        # print(str(request.form["fileBase64"]))
        #image_data = re.sub('^data:image/.+;base64,', '', str(request.form["fileBase64"]))
        data = request.get_json()
        image_data = data["Image_base64"]
        result= predict_ja(image_bytes=base64.b64decode(image_data))
        # result = "haha"
        print("hehehhehehehhehe", result)
        return jsonify({"predicted":result})

@app.route('/')
def r():
    return "HAHAHAAHAHAHH!"
