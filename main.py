from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os
import numpy as np

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    if operation == "cartoonize":
        cartoon_img = cartoonize(img)
        newFilename = f"static/{filename.split('.')[0]}_cartoonized.jpg"
        cv2.imwrite(newFilename, cartoon_img)
        return newFilename
    else:
        # Process other operations like grayscale, webp, jpg, png
        match operation:
            case "cgray":
                imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                newFilename = f"static/{filename}"
                cv2.imwrite(newFilename, imgProcessed)
                return newFilename
            case "cwebp": 
                newFilename = f"static/{filename.split('.')[0]}.webp"
                cv2.imwrite(newFilename, img)
                return newFilename
            case "cjpg": 
                newFilename = f"static/{filename.split('.')[0]}.jpg"
                cv2.imwrite(newFilename, img)
                return newFilename
            case "cpng": 
                newFilename = f"static/{filename.split('.')[0]}.png"
                cv2.imwrite(newFilename, img)
                return newFilename
    
        pass

def cartoonize(img):
    def color_quantization(img, k):
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        return result

    line_size = 3
    blur_value = 7
    grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    greyblur = cv2.medianBlur(grey, blur_value)
    edges = cv2.adaptiveThreshold(greyblur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    qimg = color_quantization(img, k=4)
    cartoon_img = cv2.bitwise_and(qimg, qimg, mask=edges)
    return cartoon_img

@app.route("/")
def home():
    return render_template("index2.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index2.html")

    return render_template("index2.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
