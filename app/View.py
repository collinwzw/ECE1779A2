from app import app
from flask import render_template, redirect, url_for, request
from app.EC2 import EC2
from app.CloudWatch import CloudWatch
from operator import itemgetter
from app.S3FileManager import S3
import boto3
from datetime import datetime, timedelta
ToAddELBList = []
from flask import render_template, redirect, url_for, request, g,session
from app.login import Login
from app.database import dbManager
from app.form import ConfigForm
from app.AutoScaller import AutoScaler

@app.route('/')
@app.route('/index')
def index():
    """Controller will assert user status, if user is already login, it will redirect to /home,
    else Controller will return the mail.html"""
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template("main.html")
    # User is not loggedin redirect to login pa ge
    return render_template("main.html",title="Landing Page")


@app.route('/ec2_examples', methods=['GET', 'POST'])
# Display an HTML list of all ec2 instances
def ec2_list():

    if len(ToAddELBList) > 0:
        for instanceID in ToAddELBList:
            if EC2.checkStatus(instanceID):
                EC2.addToELB(instanceID)

    status = request.form.get('filter', "")

    if status == "" or status == "all":
        instances = EC2.getAllInstance()
    else:
        instances = EC2.getInstanceByStatus(status)

    for instance in instances:
        pass
    return render_template("ec2_examples/list.html", title="EC2 Instances", instances=instances)

@app.route('/ec2_examples/deleteAll/', methods=['POST'])
def ec2_deleteAllInstanceExceptUserManager():
    EC2.deleteAllInstanceExceptUserManager()

    return redirect(url_for('ec2_list'))

@app.route('/ec2_get_cpu_data/<id>', methods=['GET'])
def ec2GetCPUData(id):

    instance = EC2.getInstanceByID(id)

    cpu = CloudWatch.getEC2CPUUsageByID(id)

    cpu_stats = []

    for point in cpu['Datapoints']:
        #hour = point['Timestamp'].hour
        minute = point['Timestamp'].minute
        current_minute = datetime.now().minute
        if minute > current_minute:
            time = current_minute + 60 - minute
        else:
            time = current_minute - minute
        cpu_stats.append([-time, point['Average']])

    cpu_stats = sorted(cpu_stats, key=itemgetter(0))
    return {"data": cpu_stats}

@app.route('/ec2_get_request_data/<id>', methods=['GET'])
def ec2GetRequestData(id):
    httpRequest = CloudWatch.getHttpRequestRateByID(id)
    httpRequest_stats = []

    for point in httpRequest['Datapoints']:
        #hour = point['Timestamp'].hour
        minute = point['Timestamp'].minute
        current_minute = datetime.now().minute
        if minute > current_minute:
            time = current_minute + 60 - minute
        else:
            time = current_minute - minute
        httpRequest_stats.append([-time, point['Sum']])

    httpRequest_stats = sorted(httpRequest_stats, key=itemgetter(0),reverse=True)
    return {"data": httpRequest_stats}

    #return cpu_stats
    # return render_template("ec2_examples/view.html", title="Instance Info",
    #                        instance=instance,
    #                        cpu_stats=cpu_stats,
    #                        httpRequest_stats = httpRequest_stats)



@app.route('/ec2_examples/create', methods=['POST'])
# Start a new EC2 instance
def ec2_create():
    instanceID = EC2.createInstance()
    ToAddELBList.append(instanceID)
    return redirect(url_for('ec2_list'))


@app.route('/ec2_examples/delete/<id>', methods=['POST'])
# Terminate a EC2 instance
def ec2_destroy(id):
    # create connection to ec2
    EC2.deleteInstanceByID(id)

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

    S3.uploadFileFromBucket()

    return redirect(url_for('s3_view', id=id))


@app.route('/s3_examples/delete/<bucket_id>/<key_id>', methods=['POST'])
# Delete an object from a bucket
def s3_delete(bucket_id, key_id):
    S3.deleteFileFromBucket(bucket_id,key_id)

    return redirect(url_for('s3_view', id=bucket_id))





@app.route('/login', methods=['GET', 'POST'])
def login():
    Login.loginadmin()


@app.route('/logout')
def logout():
    Login.logout_user()
    """Controller pop the login status and user information in session, then redirect to index page"""
    return redirect(url_for('index'))




@app.route('/autoscaller', methods=['GET', 'POST'])
def autoscaller():
    if 'loggedin' in session:
        form = ConfigForm()
        AutoScaler.read_config()
        if form.validate_on_submit():
            cpu_up_threshold = form.cpu_up_threshold
            cpu_down_threshold = form.cpu_down_threshold
            cooling_time = form.cooling_time
            max_worker = form.max_worker
            min_worker = form.min_worker
            upper_ratio = form.upper_ratio
            lower_ratio = form.lower_ratio
            AutoScaler.write_config(cpu_up_threshold,cpu_down_threshold,cooling_time, max_worker,min_worker,upper_ratio,lower_ratio)
        return render_template("autoscaller.html", title="Auto Scaller", form=form)
    else:
        return redirect(url_for('login'))
    return render_template("autoscaller.html", title="Auto Scaller", form=form)


@app.route('/worker/deleta_all data')
def delete_all_data():
    dbManager.dbManager.delete_all_data("accounts","error.html")
    dbManager.dbManager.delete_all_data("images","error.html")
    redirect(url_for("index"))
