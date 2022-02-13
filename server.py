import os
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_cors import CORS
import face_classification

app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg', '.mp4']
app.config['UPLOAD_PATH'] = 'static/uploads'
CORS(app)


@app.route('/')
def index():
    # return render_template('index.html', filename= 'uploads/endgame_trailer_final.mp4')
    return render_template('index.html')


@app.route('/', methods=['GET','POST'])
def upload_files():

    uploaded_video = request.files.getlist("video")[0]
    uploaded_image = request.files.getlist("image")[0]

    video_filename = uploaded_video.filename
    image_filename = uploaded_image.filename
    if video_filename != '' and image_filename != '':
        _, video_file_ext = os.path.splitext(video_filename)
        _, image_file_ext = os.path.splitext(image_filename)
        if image_file_ext not in app.config['UPLOAD_EXTENSIONS'] or video_file_ext not in app.config[
            'UPLOAD_EXTENSIONS']:
            abort(400)
        video_filename = os.path.join(app.config['UPLOAD_PATH'], video_filename)
        image_filename = os.path.join(app.config['UPLOAD_PATH'], image_filename)
        uploaded_video.save(video_filename)
        uploaded_image.save(image_filename)
        filename = face_classification.edit_video(video_path =video_filename, face_image_path=image_filename)
        relative_path = 'static'
        filename = os.path.relpath(filename, relative_path)
        print(filename)
        return render_template('index.html', filename=filename)

@app.route('/display/<filename>')
def display_video(filename):
    print('display_video filename: ' + filename)
    return redirect('static', filename='uploads/' + filename, code=301)

if __name__ == "__main__":
    app.run()



