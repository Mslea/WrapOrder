from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import StreamingHttpResponse
import cv2
import base64
from process_order.models import *
import requests
import time
# Create your views here.

def base64decode(path):
    with open(path,'rb') as img_file:
        base64_encoded_data = base64.b64encode(img_file.read())
        base64_message = base64_encoded_data.decode('utf-8')
        return base64_message
    
def isorder(code):
    try:
        order = Order.objects.get(order_code=code)
        if  not order.check_wrap():
            return 1
        else:
            return 0
    except:
        return 0

def isorder_dertail(code,order):
    try:
        order_list = Order_detail.objects.filter(order=order)
        for i in order_list:
            if i.product_id == code:
                return 1
                break
        return 0
    except:
        return 0
        
        


def wrap(request):
    template =get_template('wrap.html')
    return HttpResponse(template.render({}, request))

def stream():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    order_list = list()
    order_video = list()
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('./media/video_data/demo.jpg',frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('./media/video_data/demo.jpg', 'rb').read() + b'\r\n')
        
        b64 = base64decode('./media/video_data/demo.jpg')
        r = requests.post(url='http://127.0.0.1:5000/predict',json={'Image_base64':b64})
        code =r.json()['predicted']
        if not code:
            if order_video:
                order_video[0].write(frame)
        else:
            code = code[0]
            if isorder(code):
                order = Order.objects.get(order_code=code)
                if order in order_list:
                    index = order_list.index(order)
                    order_list.remove(order)
                    order_list.index(0,order)
                    t = order_video[index]
                    order_video.remove(t)
                    order_video.insert(0,t)
                else: 
                    order_list.insert(0,order)
                    order_video.insert(0,cv2.VideoWriter('./media/video_data/{}.avi'.format(code),fourcc, 20.0, (640,480)))
                print('\n ok order {}'.format(code))
            else:
                if not order_list:
                    print('\nok barcode not exits')
                else:
                    if isorder_dertail(code,order_list[0]):
                        order_detail1 = Order_detail.objects.get(product_id = code)
                        if(order_detail1.quality > order_detail1.quality_wraped):
                            order_detail1.quality_wraped+=1
                            order_detail1.save()
                            print('ok \n wrap 1 product{}'.format(code))
                            order_video[0].write(frame)
                            time.sleep(3)
                        if order_list[0].check_wrap():
                            order_list[0].status = 'wrapped'
                            order_list[0].save()
                            order_list.remove(order_list[0])
                            order_video.remove(order_video[0])
                            order_video[0].release()
                            print('\nwrap 1 order')
        

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')

def record_video(request):
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()