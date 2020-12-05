import shutil

from app import app
from flask import render_template, g, request, session, redirect, url_for, send_file
import os, sys,shutil
from werkzeug.utils import secure_filename
import requests
import random
import string


from app.S3 import clear_s3,upload_file
app.config["IMAGE_UPLOADS"]="./app/static/img/uploads"
#app.config["IMAGE_PROCESSED"]="./app/static/img/processed"
app.config["ALLOWED_IMAGE_EXETENSIONS"] = ["JPEG","JPG","PNG"]
app.config['MAX_IMAGE_FILESIZE'] = 1024*1024
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

@app.route('/imageUpload', methods=['GET', 'POST'])
def imageUpload():
    if 'loggedin' in session:
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
                        filename = processImage(filename)
                        savePath = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
                        image.save(savePath)
                        upload_file(savePath, filename)
                        os.remove(savePath)

                    return redirect("imageUpload")
            elif request.form['url'] != "":
                url = request.form['url']
                if not allowedImageType(url):
                    print("Image is not in valid type")
                    return render_template("imageUpload.html", message="Image is not in valid type")
                filename = os.path.join(app.config["IMAGE_UPLOADS"], 'temp.jpeg')
                try:
                    with open(filename, 'wb') as f:
                        response = requests.get(url, stream=True)
                        for block in response.iter_content(1024):
                            if not block:
                                break
                            f.write(block)
                    print('Image sucessfully Downloaded: ')
                except:
                    e = sys.exc_info()
                    return render_template("imageUpload.html",
                                           message="Image could not be downloaded from url. Error: " + str(e))
                filename = processImage(filename)
                os.remove(filename)

                return redirect("imageView")
            else:
                print('No file or url selected.')
                return render_template("imageUpload.html", message='No file or url selected')
        return render_template("imageUpload.html", message="please select image")
    return redirect(url_for('login'))