from flask import Flask, request, redirect, render_template, json
import boto3, botocore
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
#print(os.environ.get('password'))

app.config['S3_BUCKET'] = os.environ.get('bucketname')
app.config['S3_KEY'] = os.environ.get('AWSAccessKeyId')
app.config['S3_SECRET'] = os.environ.get('AWSSecretKey')
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(os.environ.get('bucketname'))

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

@app.route("/", methods=["GET"])
def main():
    #print(app.config['S3_BUCKET'])
    return render_template("Index.html")

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     if "user_file" not in request.files:
#         return "No user_file key in request.files"
#     file = request.files["user_file"]
#     if file.filename == "":
#         return "Please select a file"
#     if file:
#         #file.filename = secure_filename(file.filename)
#         #output = send_to_s3(file, app.config["S3_BUCKET"])
#         #return str(output)
#         return str("submited")
#     else:
#         return redirect("/")

# @app.route('/sign_s3/')
# def sign_s3():

#   #S3_BUCKET = os.environ.get('S3_BUCKET')
#   print(app.config['S3_BUCKET'])
#   S3_BUCKET = app.config['S3_BUCKET']
#   file_name = request.args.get('file_name')
#   file_type = request.args.get('file_type')
#   s3 = boto3.client('s3')
#   presigned_post = s3.generate_presigned_post(
#     Bucket = S3_BUCKET,
#     Key = file_name,
#     Fields = {"acl": "public-read", "Content-Type": file_type},
#     Conditions = [
#       {"acl": "public-read"},
#       {"Content-Type": file_type}
#     ],
#     ExpiresIn = 3600
#   )
#   return json.dumps({
#     'data': presigned_post,
#     'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
#   })

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = app.config['S3_BUCKET'],
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "
    return render_template("index.html",msg =msg)

app.run(port=3000, debug=True)