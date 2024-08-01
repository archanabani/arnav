# Program to Upload Color Image and convert into Black & White image
import os
from flask import  Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
import cv2

app = Flask(__name__)

# Write load_form function below to Open and redirect to default upload webpage
@app.route('/')
def load_form():
    return render_template('upload.html')




# Write upload_image Function to upload image and redirect to new webpage
@app.route('/gray',methods=['POST'])
def upload_image():
    operation_selection = request.form['image_type_selection']
    file=request.files['file']
    filename=secure_filename(file.filename)
    file_data=file.read()
    displaymessage='image succesfully uploaded and displayed below.'
    image_array=np.fromstring(file_data,dtype='uint8')
    print('image array=',image_array)
    decode_array_to_image=cv2.imdecode(image_array,cv2.IMREAD_UNCHANGED)
    print('decode array to image',decode_array_to_image)
    
    if operation_selection == 'gray':
        file_data = make_greyscale(decode_array_to_image)
    elif operation_selection == 'sketch':
        file_data = image_sketch(decode_array_to_image)
    elif operation_selection == 'oil':
        file_data = oil_effect(decode_array_to_image)
    elif operation_selection == 'rgb':
        file_data = rgb_effect(decode_array_to_image)
    elif operation_selection == 'water':
        file_data = water_color_effect(decode_array_to_image)
    elif operation_selection == 'invert':
        file_data = invert(decode_array_to_image)
    elif operation_selection == 'hdr':
        file_data = hdr_effect(decode_array_to_image)



    else:
        print('No image')

    with open(os.path.join('static/', filename),'wb') as f:
        f.write(file_data)
    

    return render_template('upload.html', filename=filename)


def make_greyscale(input_image):
    convert_gray_image=cv2.cvtColor(decode_array_to_image,cv2.COLOR_RGB2GRAY)
    status,output_image=cv2.imencode('.PNG',convert_gray_image)
    print('staus',status)
    return output_image

def image_sketch(decode_array_to_image):
    convert_gray_img = cv2.cvtColor(decode_array_to_image, cv2.COLOR_RGB2GRAY)
    sharping_gray_img = cv2.bitwise_not(convert_gray_img)
    blur_img = cv2.GaussianBlur(sharping_gray_img, (111,111), 0)
    sharping_blur_img = cv2.bitwise_not(blur_img)
    sketch_img = cv2.divide(convert_gray_img, sharping_blur_img, scale=256.0)
    status, output_image = cv2.imencode('.PNG', sketch_img)

    return output_image

def oil_effect(decode_array_to_image):
    oil_effect_img = cv2.xphoto.oilPainting(decode_array_to_image, 7, 1)
    status, output_image = cv2.imencode('.PNG', oil_effect_img)

    return output_image

def rgb_effect(decode_array_to_image):
    rgb_effect_img = cv2.cvtColor(decode_array_to_image, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', rgb_effect_img)

    return output_image

def water_color_effect(decode_array_to_image):
    water_effect = cv2.stylization(decode_array_to_image, sigma_s=60, sigma_r=0.6)
    staus, output_image = cv2.imencode('.PNG', water_effect)

    return output_image

def invert(decode_array_to_image):
    invert_effect = cv2.bitwise_not(decode_array_to_image)
    staus, output_image = cv2.imencode('.PNG', invert_effect)

    return output_image

def hdr_effect(decode_array_to_image):
    water_effect = cv2.detailEnhance(decode_array_to_image, sigma_s=12, sigma_r=0.15)
    staus, output_image = cv2.imencode('.PNG', hdr_effect)

    return output_image









# Write display_image Function to display the uploaded image
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static',filename=filename))






if __name__ == "__main__":
    app.run()
