from flask import Flask, request, render_template, redirect, url_for
import os
import uuid


app = Flask(__name__)


# Define upload folder path (modify as needed)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Get uploaded image
        img = request.files['image']

        # Check if image is valid
        if img and allowed_file(img.filename):
            # Generate unique filename
            key = uuid.uuid1()
            img_filename = f"{key}{img.filename}"

            # Save the image
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))

            # Success message (modify as needed)
            message = "Image uploaded successfully!"
            return render_template('upload.html', message=message)
        else:
            # Error message (modify as needed)
            message = "Invalid image format. Please upload JPG, JPEG, PNG or GIF files."
            return render_template('upload.html', message=message)

    return render_template('upload.html')

def allowed_file(filename):
    # Allowed extensions for image files
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)


