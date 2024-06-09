from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Set the upload directory
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the request contains a file
        if 'dp' in request.files:
            img = request.files['dp']
            
            # Check if the file is present
            if img.filename != '':
                # Save the file to the upload directory
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
                img.save(img_path)
                
                # Perform any additional operations on the uploaded file
                # ...
                
                return f'File {img.filename} uploaded successfully!'
            else:
                return 'No file selected.'
        else:
            return 'No file part in the request.'
    
    # Render the HTML template for the upload form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return 'No file part'
        
#         file = request.files['file']
#         if file.filename == '':
#             return 'No selected file'
        
#         if file:
#             file.save(f"uploads/{file.filename}")
#             return 'File successfully uploaded'
    
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
