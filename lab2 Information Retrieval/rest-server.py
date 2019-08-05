#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------                                                                                                                             
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
#-------------------------------------------------------------------------------------------------------------------------------                                                                                                                              
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil 
import numpy as np
from search import recommend
import tarfile
from datetime import datetime
from scipy import ndimage
from scipy.misc import imsave 
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile
app = Flask(__name__, static_url_path = "")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

#==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================
extracted_features=np.zeros((10000,2048),dtype=np.float32)
with open('saved_features_recom.txt') as f:
    		for i,line in enumerate(f):
        		extracted_features[i,:]=line.split()
print("loaded extracted_features") 


#global tagtxt_name
#==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
#==============================================================================================================================
@app.route('/imgUpload', methods=['GET', 'POST'])
def upload_img():
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):
          os.mkdir(result)
    shutil.rmtree(result)
 
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
           
            print('No selected file')
            return redirect(request.url)
        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/result"
            image_list =[os.path.join(image_path, file) for file in os.listdir(result)
                              if not file.startswith('.')]
            length = len(image_list)
            images = {
			'image0':image_list[0],
            'image1':image_list[1],	
			'image2':image_list[2],	
			'image3':image_list[3],	
			'image4':image_list[4],	
			'image5':image_list[5],	
			'image6':image_list[6],	
			'image7':image_list[7],	
			'image8':image_list[8],
                'num':length
		      }				
            return jsonify(images)

tag_list1=['animals','people','food','structures','transport']
#tag_list2=['/animals','/people','/food','/structures','/transport']
#for tagName in tag_list1:
@app.route('/animals',methods=['GET', 'POST'])
def animals():
    #global tagtxt_name
    #tagtxt_name = request.form.get('tagName','')
    print(tag_list1[0]+'@fwf')
    tag='static/'+tag_list1[0]
    print(tag + '@fff')
    if request.method == 'POST' or request.method == 'GET':
        print(request.method+'@23r')
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)

        if file.filename == '':
            print('No file part')
            return redirect(request.url)


        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/"+tag_list1[0]
            image_list = [os.path.join(image_path, file) for file in os.listdir(tag)
                          if not file.startswith('.')]
            length=len(image_list)

            images = {
                'image0': image_list[0],
                'image1': image_list[1],
                'image2': image_list[2],
                'image3': image_list[3],
                'image4': image_list[4],
                'image5': image_list[5],
                'image6': image_list[6],
                'image7': image_list[7],
                'image8': image_list[8],
                'nun':length
            }
            return jsonify(images)

@app.route('/people',methods=['GET', 'POST'])
def people():
    #global tagtxt_name
    #tagtxt_name = request.form.get('tagName','')
    print(tag_list1[1]+'@fwf')
    tag='static/'+tag_list1[1]
    print(tag + '@fff')
    if request.method == 'POST' or request.method == 'GET':
        print(request.method+'@23r')
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)

        if file.filename == '':
            print('No file part')
            return redirect(request.url)


        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/"+tag_list1[1]
            image_list = [os.path.join(image_path, file) for file in os.listdir(tag)
                          if not file.startswith('.')]
            length=len(image_list)

            images = {
                'image0': image_list[0],
                'image1': image_list[1],
                'image2': image_list[2],
                'image3': image_list[3],
                'image4': image_list[4],
                'image5': image_list[5],
                'image6': image_list[6],
                'image7': image_list[7],
                'image8': image_list[8],
                'nun':length
            }
            return jsonify(images)

@app.route('/food',methods=['GET', 'POST'])
def food():
    #global tagtxt_name
    #tagtxt_name = request.form.get('tagName','')
    print(tag_list1[2]+'@fwf')
    tag='static/'+tag_list1[2]
    print(tag + '@fff')
    if request.method == 'POST' or request.method == 'GET':
        print(request.method+'@23r')
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)

        if file.filename == '':
            print('No file part')
            return redirect(request.url)


        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/"+tag_list1[2]
            image_list = [os.path.join(image_path, file) for file in os.listdir(tag)
                          if not file.startswith('.')]
            length=len(image_list)

            images = {
                'image0': image_list[0],
                'image1': image_list[1],
                'image2': image_list[2],
                'image3': image_list[3],
                'image4': image_list[4],
                'image5': image_list[5],
                'image6': image_list[6],
                'image7': image_list[7],
                'image8': image_list[8],
                'nun':length
            }
            return jsonify(images)

@app.route('/structures', methods=['GET', 'POST'])
def structures():
    # global tagtxt_name
    # tagtxt_name = request.form.get('tagName','')
    print(tag_list1[3] + '@fwf')
    tag = 'static/' + tag_list1[3]
    print(tag + '@fff')
    if request.method == 'POST' or request.method == 'GET':
        print(request.method + '@23r')
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)

        if file.filename == '':
            print('No file part')
            return redirect(request.url)

        if file:  # and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/" + tag_list1[3]
            image_list = [os.path.join(image_path, file) for file in os.listdir(tag)
                          if not file.startswith('.')]
            length = len(image_list)

            images = {
                'image0': image_list[0],
                'image1': image_list[1],
                'image2': image_list[2],
                'image3': image_list[3],
                'image4': image_list[4],
                'image5': image_list[5],
                'image6': image_list[6],
                'image7': image_list[7],
                'image8': image_list[8],
                'nun': length
            }
            return jsonify(images)

@app.route('/transport',methods=['GET', 'POST'])
def transport():
    #global tagtxt_name
    #tagtxt_name = request.form.get('tagName','')
    print(tag_list1[0]+'@fwf')
    tag='static/'+tag_list1[4]
    print(tag + '@fff')
    if request.method == 'POST' or request.method == 'GET':
        print(request.method+'@23r')
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)

        if file.filename == '':
            print('No file part')
            return redirect(request.url)


        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/"+tag_list1[4]
            image_list = [os.path.join(image_path, file) for file in os.listdir(tag)
                          if not file.startswith('.')]
            length=len(image_list)

            images = {
                'image0': image_list[0],
                'image1': image_list[1],
                'image2': image_list[2],
                'image3': image_list[3],
                'image4': image_list[4],
                'image5': image_list[5],
                'image6': image_list[6],
                'image7': image_list[7],
                'image8': image_list[8],
                'nun':length
            }
            return jsonify(images)

#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/")
def main():
    
    return render_template("main.html")   
if __name__ == '__main__':
    #app.run(debug = True, host= '0.0.0.0')
    app.run(debug=True, host='127.0.0.1')
