import json
import threading
import time

from app import app
from flask import render_template, redirect, url_for, request
from app.EC2 import EC2
from app.CloudWatch import CloudWatch

from operator import itemgetter
from app.S3FileManager import S3
import boto3
from datetime import datetime, timedelta
ToAddELBList = []
from flask import render_template, redirect, url_for, request, g,session,flash
from app.login import Login
from app.database import dbManager
from app.form import ConfigForm,LoginForm

from werkzeug.security import check_password_hash

from app.LoadBalancer import LoadBalancer
@app.route('/')
@app.route('/index')
def index():
    """Controller will assert user status, if user is already login, it will redirect to /home,
    else Controller will return the mail.html"""
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template("main.html")
    # User is not loggedin redirect to login pa ge
    return render_template("welcome.html",title="Landing Page")

'''
@app.route('/get_worker_count_graph',methods=['POST','GET'])
def get_worker_count_graph():
    monitor = worker_count.get_worker_count_monitor()
    return render_template('worker_count_graph.html',
    worker_count_by_time = monitor.get_record())
'''

@app.route('/get_worker_count_graph',methods=['POST','GET'])
def get_worker_count_graph():
    record = []
    period = 60
    time_range = 1800
    record_max = time_range/period
    started = False
    running_thread = threading.Thread(target = get_worker_count_graph,daemon = True)
    if not started:
        started = True
        #running_thread.start()
        while True:
            record.append({
                "Timestamp": datetime.now().strftime("%H:%M"),
                "Count": LoadBalancer.get_number_of_worker()
            })
            if (len(record) > record_max):
                record.pop(0)
            #time.sleep(period)
            return render_template('worker_count_graph.html',
                           worker_count_by_time = record)




@app.route('/ec2_list', methods=['GET', 'POST'])
@app.route('/ec2_examples', methods=['GET', 'POST'])
# Display an HTML list of all ec2 instances
def ec2_list():

    if len(ToAddELBList) > 0:
        for instanceID in ToAddELBList:
            if EC2.checkStatus(instanceID):
                EC2.addToELB(instanceID)



    # # if status == "" or status == "all":
    # #     instances = EC2.getAllInstance()
    # # else:
    #     instances = EC2.getInstanceByStatus(status)
    instances = EC2.getInstanceByStatus('running')

    for instance in instances:
        pass
    return render_template("ec2_examples/list.html", title="EC2 Instances", instances=instances)

@app.route('/ec2_examples/deleteAllInstance/', methods=['POST'])
def ec2_deleteAllInstanceExceptUserManager():
    EC2.deleteAllInstanceExceptUserManager()
    return redirect(url_for('ec2_list'))

@app.route('/ec2_examples/deleteAllData/', methods=['POST'])
def ec2_deleteAllData():

    buckets = S3.getAlls3Bucket()
    for bucket in buckets:
        S3.deleteAllFileFromBucket(bucket.name)

    return redirect(url_for('ec2_list'))

@app.route('/ec2_get_cpu_data/<id>', methods=['GET'])
def ec2GetCPUData(id):

    instance = EC2.getInstanceByID(id)

    cpu = CloudWatch.getEC2CPUUsageByID(id,30)

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







@app.route('/login', methods=['GET', 'POST'])
def login():
    """Controller that display the login page.controller that display the imageView page.
    This controller will assert if user is already logged in or not.
    If yes, it will redirect to home page.
    If no, it will show the login page and let user input username and password.
    Once user submit the username and password, it will go to dababase and verify them.
    If login success, user id, username, admin_auth will be save in session
    account: assert if username is in database.
    """
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', title='Sign In', form=form)
    if request.method == "POST":
        if 'loggedin' in session:
            return redirect(url_for('index'))
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            account = dbManager.dbManager.checkuser(username)
            if account:
                if check_password_hash(str(account['password_hash']), password):
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    session['admin_auth'] = bool(account['admin_auth'])
                    flash('Login successfully!')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid password')
                    return redirect(url_for('login'))
            flash('Invalid username')
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    Login.logout_user()
    """Controller pop the login status and user information in session, then redirect to index page"""
    return redirect(url_for('login'))




@app.route('/autoscaller/config', methods=['GET', 'POST'])
def autoscaller_config():
    if 'loggedin' in session:
        form = ConfigForm()
        if form.validate_on_submit():
            max_worker = int(form.max_worker)
            min_worker = form.min_worker
            cooling_time = form.cooling_time
            cpu_up_threshold = form.cpu_up_threshold
            cpu_down_threshold = form.cpu_down_threshold
            extend_ratio = form.extend_ratio
            shrink_ratio = form.shrink_ratio
            # if cpu_up_threshold < cpu_down_threshold or max_worker < min_worker or extend_ratio < shrink_ratio:
            #     flash("wrong config, please make sure max greater than min")
            #     return render_template("scalingconfig.html", title="Auto Scaller", form=form)
            # else:
            dbManager.dbManager.updata_autoscaling_parameter(max_worker,
                                                                 min_worker, cooling_time, cpu_up_threshold,
                                                                 cpu_down_threshold,extend_ratio, shrink_ratio )
            return redirect(url_for('index'))
    else:
        flash('Please Login')
        return redirect(url_for('login'))
    return render_template("scalingconfig.html", title="Auto Scaller", form=form)


@app.route('/autoscaller', methods=['GET', 'POST'])
def autoscaller():
    if 'loggedin' in session:
        config_table = dbManager.dbManager.fetch_autoscaling_parameter()
        return render_template("autoscaller.html", title="Auto Scaller", config=config_table[0])
    else:
        flash('Please Login')
        return redirect(url_for('login'))


@app.route('/worker/deleta_all_data')
def delete_all_data():
    dbManager.dbManager.delete_all_data("accounts")
    dbManager.dbManager.delete_all_data("images")
    dbManager.dbManager.write_admin()
    redirect(url_for("index"))


@app.route('/expandpool', methods=['GET', 'POST'])
def expand_pool():
    if 'loggedin' in session:
        config_table = dbManager.dbManager.fetch_autoscaling_parameter()
        pool_size = config_table[0]["max_worker"]
        if pool_size <8:
            new_pool_size = pool_size + 1
            dbManager.dbManager.write_pool_size(new_pool_size)
            flash("The worker pool size expanded")
            return redirect(url_for("autoscaller"))
        else:
            flash("Your pool size has reached the upper limit")
            return redirect(url_for("autoscaller"))


@app.route('/shrinkpool', methods=['GET', 'POST'])
def shrink_pool():
    if 'loggedin' in session:
        config_table = dbManager.dbManager.fetch_autoscaling_parameter()
        pool_size = config_table[0]["max_worker"]
        if pool_size >1:
            new_pool_size = pool_size - 1
            dbManager.dbManager.write_pool_size(new_pool_size)
            flash("The worker pool size shrinked")
            return redirect(url_for("autoscaller"))
        else:
            flash("Your pool size has reached the lower limit")
            return redirect(url_for("autoscaller"))



