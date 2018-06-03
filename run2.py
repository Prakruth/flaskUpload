import os,subprocess
from flask import Flask, request, redirect, url_for,flash
from werkzeug.utils import secure_filename




imax = 0
jmax = 0
kmax = 0

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def getparams():
    ilist = [0.001,0.01,0.1]
    jlist = [1,2,4]
    klist = [1000,2000,4000]
    global imax
    global jmax
    global kmax
    if imax or jmax or kmax :
        return True
    maxx = float(-1.0)
    for i in ilist :
        for j in jlist :
            for k in klist :
                s = subprocess.check_output ("python train.py --i "+str(i)+ "--j "+str(j) +"--k " +str(k) +"--images ./images",shell=True)
                fs = float(s)
                if (fs > maxx) :
                    maxx = fs
                    imax =i
                    jmax=j
                    kmax=k
    
    return True



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploaded_file')
def uploaded_file():
    getparams()
    res = float(subprocess.check_output ("python train.py --i "+str(imax)+ "--j "+str(jmax) +"--k " +str(kmax) +"--images ./images",shell=True))
    return str(res)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
if __name__ == '__main__':
    app.run(debug=True)
