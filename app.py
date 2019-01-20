from keras.models import load_model
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os
from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

model=load_model('my_model.h5')  
model._make_predict_function()
app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>Photo Upload</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=photo>
         <input type=submit value=Upload>
    </form>
    '''

def pre( filename ):
	img = Image.open( filename )
	width, height = img.size 
	print(width)
	print(height)
	img = img.resize((width, width))  
	width, height = img.size 
	print(width)
	print(height)
	img = img.resize((32,32))  
	width, height = img.size 
	print(width)
	print(height)
	a = np.array(img)
	plt.imshow(a, cmap='gray')
	print(a.shape)
	i= a.reshape(1,32,32,3)
	t=model.predict_classes(i)
	print("prediction: ",t)
	if t==0:
	  print("airplane")
	  na="airplane"
	if t==1:
	  na="automobile"
	if t==2:
	  na="bird"
	  print(a)
	if t==3:
	  na="cat"
	if t==4:
	  na="deer"
	if t==5:
	  na="dog"  
	if t==6:
	  na="frog"
	if t==7:
	  na="horse"  
	if t==8:
	  na="ship"
	if t==9:
	  na="truck"
	print(na)  
	return na

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'])
		file_url = photos.url(filename) 
		t=pre(filename)
		return html +'<p style="color:red;font-size:50px;">It is a ' + t + ' .</p>'+ '<br><img src=' + file_url + ' style="width:500px;"><p></p>' 
	return html


if __name__ == '__main__':
    app.run()



# img = Image.open("c.jpg") 
# width, height = img.size 
# print(width)
# print(height)
# img = img.resize((width, width))  
# width, height = img.size 
# print(width)
# print(height)
# img = img.resize((32,32))  
# width, height = img.size 
# print(width)
# print(height)
# a = np.array(img)
# plt.imshow(a, cmap='gray')
# print(a.shape)
# i= a.reshape(1,32,32,3)
# t=model.predict_classes(i)
# print("prediction: ",t)
# if t==0:
#   print("airplane")
# if t==1:
#   print("automobile")
# if t==2:
#   print("bird")
# if t==3:
#   print("cat")
# if t==4:
#   print("deer")
# if t==5:
#   print("dog")  
# if t==6:
#   print("frog")
# if t==7:
#   print("horse")  
# if t==8:
#   print("ship")
# if t==9:
#   print("truck")