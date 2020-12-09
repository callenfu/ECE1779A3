from app import app
from flask import render_template, g, request, session, redirect, url_for, send_file, flash
import os, sys,shutil
from werkzeug.utils import secure_filename
import requests
import random
import string
from app.database import DynamoDB
from time import sleep
from app.S3 import clear_s3,upload_file,get_image
app.config["IMAGE_UPLOADS"]="./app/static/img/uploads"
#app.config["IMAGE_PROCESSED"]="./app/static/img/processed"
app.config["ALLOWED_IMAGE_EXETENSIONS"] = ["JPEG","JPG","PNG"]
app.config['MAX_IMAGE_FILESIZE'] = 1024*1024
db = DynamoDB()



def generate_filename():
    '''
    method to get filename that have not been saved in the database
    :return: integer that store number of files stored in database
    '''
    while 1:
        chars = string.ascii_letters + string.digits
        key = random.sample(chars, 10)
        keys = "".join(key)
        return keys


def allowedImageType(filename):
    '''
    method to check the type of file uploaded by user
    :param filename: the uploaded filename by user
    :return: boolean. True if the image is one of allowed type, else False.
    '''
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXETENSIONS"]:
        return True

def processImage(filename):
    filename = generate_filename()
    filename = filename + '.' + filename.rsplit(".", 1)[0]
    return  filename

def allowedImageFilesize(filesize):
    '''
    method to check the filesize of the image uploaded by user
    :param filesize: the uploaded filename by user
    :return: boolean. True if the image size is under limit, else False.
    '''
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


def deleteAllImages():
    folder = app.config["IMAGE_PROCESSED"]
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

@app.route('/showResult/<filename>', methods=['GET', 'POST'])
def showResult(filename):
    response = db.check_image("imagename", filename)
    if "textresult" in response:
        textResult = response['textresult']
        textResultList = textResult.split(";")[:-1]
    else:
        textResultList = "No text detected in image"
    return render_template("showResult.html", recognition_result=textResultList, filename = filename)

@app.route("/sendRequest/<string:aQuery>",methods=['GET'])
def sendRequest(aQuery):
    return redirect("https://www.google.com/maps/search/?api=1&query=" + aQuery)


@app.route('/imageUpload', methods=['GET', 'POST'])
def imageUpload():
    if 'loggedin' in session:
        username = session["username"]
        if request.method == "POST":
            if request.files:
                if "filesize" in request.cookies:
                    if not allowedImageFilesize(request.cookies["filesize"]):
                        print("Filesize exceeded maximum limit")
                        return render_template("imageUpload.html", message="Filesize exceeded maximum limit")
                    # get the image object
                    image = request.files['image']
                    # check image name
                    if image.filename == '':
                        print("Image must have a file name")
                        return render_template("imageUpload.html", message="Image must have a file name")
                    if not allowedImageType(image.filename):
                        print("Image is not in valid type")
                        return render_template("imageUpload.html", message="Image is not in valid type")
                    else:
                        filename = secure_filename(image.filename)
                        filename = getImageName(filename)
                        finalfilename = generate_filename()
                        finalfilename = finalfilename + '.' + filename.rsplit(".", 1)[1]
                        upload_file(image, finalfilename)
                        db.add_image(username,finalfilename)
                    result = None
                    loop = 0
                    while result is None and loop < 10:
                        loop += 1
                        response = db.check_image("imagename", finalfilename)
                        if "testresult" in response:
                            result = response['textresult']
                        else:
                            result = None
                            sleep(1)
                    return redirect(url_for("showResult",filename=finalfilename))
            else:
                flash('No file or url selected.')
                return render_template("imageUpload.html", message='No file or url selected')
        return render_template("imageUpload.html")
    return redirect(url_for('login'))

@app.route('/getImageName', methods=['GET', 'POST'])
def getImageName(filename):
    return filename


@app.route('/uploadhistory',methods=['GET','POST'])
def upload_history():
    if 'loggedin' in session:
        username = session["username"]
        historytable = db.get_history(username)
        return render_template("uploadhistory.html",historytable = historytable)
    return redirect(url_for("login"))


@app.route('/sendImages/<filename>/', methods=["GET", "POST"])
def sendImages(filename):
    picture = get_image(filename)
    return send_file(picture)