from app import app
from flask import render_template, redirect, url_for, request, g
from app.EC2 import EC2
from app.CloudWatch import CloudWatch
from app import config
from datetime import datetime, timedelta
from operator import itemgetter
import boto3
@app.route('/')
@app.route('/index')
def index():
    """Controller will assert user status, if user is already login, it will redirect to /home,
    else Controller will return the mail.html"""

        # User is loggedin show them the home page

    # User is not loggedin redirect to login pa ge
    return render_template("main.html",title="Landing Page")


@app.route('/ec2_examples', methods=['GET', 'POST'])
# Display an HTML list of all ec2 instances
def ec2_list():

    status = request.form.get('filter', "")

    if status == "" or status == "all":
        instances = EC2.getAllInstance()
    else:
        instances = EC2.getInstanceByStatus(status)

    return render_template("ec2_examples/list.html", title="EC2 Instances", instances=instances)


@app.route('/ec2_examples/<id>', methods=['GET'])
# Display details about a specific instance.
def ec2_view(id):

    instance = EC2.getInstanceByID(id)

    cpu = CloudWatch.getEC2CPUUsageByID(id)

    cpu_stats = []

    for point in cpu['Datapoints']:
        hour = point['Timestamp'].hour
        minute = point['Timestamp'].minute
        time = hour + minute / 60
        cpu_stats.append([time, point['Average']])

    cpu_stats = sorted(cpu_stats, key=itemgetter(0))


    return render_template("ec2_examples/view.html", title="Instance Info",
                           instance=instance,
                           cpu_stats=cpu_stats)


@app.route('/ec2_examples/create', methods=['POST'])
# Start a new EC2 instance
def ec2_create():
    EC2.createInstance()
    return redirect(url_for('ec2_list'))


@app.route('/ec2_examples/delete/<id>', methods=['POST'])
# Terminate a EC2 instance
def ec2_destroy(id):
    # create connection to ec2
    EC2.getDeleteInstanceByID(id)

    return redirect(url_for('ec2_list'))


@app.route('/s3_examples', methods=['GET'])
# Display an HTML list of all s3 buckets.
def s3_list():
    # Let's use Amazon S3
    s3 = boto3.resource('s3')

    # Print out bucket names
    buckets = s3.buckets.all()

    for b in buckets:
        name = b.name

    buckets = s3.buckets.all()

    return render_template("s3_examples/list.html", title="s3 Instances", buckets=buckets)


@app.route('/s3_examples/<id>', methods=['GET'])
# Display details about a specific bucket.
def s3_view(id):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(id)

    for key in bucket.objects.all():
        k = key

    keys = bucket.objects.all()

    return render_template("s3_examples/view.html", title="S3 Bucket Contents", id=id, keys=keys)


@app.route('/s3_examples/upload/<id>', methods=['POST'])
# Upload a new file to an existing bucket
def s3_upload(id):
    # check if the post request has the file part
    if 'new_file' not in request.files:
        return redirect(url_for('s3_view', id=id))

    new_file = request.files['new_file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if new_file.filename == '':
        return redirect(url_for('s3_view', id=id))

    s3 = boto3.client('s3')

    s3.upload_fileobj(new_file, id, new_file.filename)

    return redirect(url_for('s3_view', id=id))


"""
    Part 2

    Complete the function s3_examples.delete so that it removes an object
    from an S3 bucket.

    Documentation for the S3 available at:

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object

    Search in the above URL for the string "client.delete_object"


"""


@app.route('/s3_examples/delete/<bucket_id>/<key_id>', methods=['POST'])
# Delete an object from a bucket
def s3_delete(bucket_id, key_id):
    s3 = boto3.client('s3')

    ## your code start here
    s3.delete_object(Bucket=bucket_id, Key=key_id)

    ## your code ends here

    return redirect(url_for('s3_view', id=bucket_id))

