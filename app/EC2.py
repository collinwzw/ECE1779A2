import boto3
from app import config
from flask import flash
import sys,os
basedir = os.path.abspath(os.path.dirname(__file__))

class EC2:

    @staticmethod
    def getAllInstance():
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        try:
            ec2 = boto3.resource('ec2')

            instances = ec2.instances.all()
            result = []
            for instance in instances:
                if instance.id == 'i-03d46ce71ce9f19c7' :
                    pass
                else:
                    result.append(instance)
            return result
        except:
            e = sys.exc_info()
            flash("AWS connection error")

    @staticmethod
    def getAllInstanceID():
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        try:
            ec2 = boto3.resource('ec2')

            instances = ec2.instances.all()
            result = []
            for instance in instances:
                if instance.id == 'i-03d46ce71ce9f19c7' :
                    pass
                else:
                    result.append(instance.id)
            return result
        except:
            e = sys.exc_info()
            flash("AWS connection error")

    @staticmethod
    def getInstanceByStatus(filters):
        '''
        get ec2 instance by status
        :param filters:
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        try:
            ec2 = boto3.resource('ec2')
            instances = ec2.instances.filter(Filters=filters)
            return instances
        except:
            e = sys.exc_info()
            flash("AWS connection error")
    @staticmethod
    def getInstanceByID(id):
        '''
        get instance by ID
        :param id:
        :return: ec2 instance
        '''
        try:
            ec2 = boto3.resource('ec2')
            instance = ec2.Instance(id)
            return instance
        except:
            e = sys.exc_info()
            flash("AWS connection error")

    @staticmethod
    def createInstance():
        '''
        create one instance of pre-defined imageID with pre-defined subnet_id
        :return: void
        '''
        try:
            with open(basedir + '/UserData.txt', 'r') as myfile:
                data = myfile.read()
            ec2 = boto3.resource('ec2')
            instance = ec2.create_instances(ImageId=config.ami_id,
                                 MinCount=1,
                                 MaxCount=1,
                                 InstanceType=config.instanceType,
                                 SecurityGroupIds=[
                                     config.securityGroupIds,
                                 ],
                                 SubnetId=config.subnet_id,
                                 #UserData=f"\n#!/bin/bash\ncd Desktop\nchmod u+x start.sh\n./start.sh \n",
                                 #UserData=f"\n#!/bin/bash\ncd Desktop\n./start.sh \n",
                                 UserData=data,
                                 KeyName=config.keyname,
                                 IamInstanceProfile={
                                     'Arn': config.instanceProfileARN,
                                 },
            )
            return instance[0].id
        except:
            e = sys.exc_info()
            flash(e)

    @staticmethod
    def checkStatus(instanceID):
        ec2 = boto3.client('ec2')
        r = ec2.describe_instance_status(InstanceIds=[instanceID])
        if len(r['InstanceStatuses']) < 1 or r['InstanceStatuses'][0]['InstanceState']['Name'] != 'running':
            return False
        else:
            return True

    @staticmethod
    def addToELB(instanceID):
        try:
            # ec2c = boto3.client('ec2')
            # r = ec2c.describe_instance_status(InstanceIds=[instanceID])
            # while len(r['InstanceStatuses']) < 1 :
            #     r = ec2c.describe_instance_status(InstanceIds=[instanceID])
            # while r['InstanceStatuses'][0]['InstanceState']['Name'] != 'running':
            #     r = ec2c.describe_instance_status(InstanceIds=[instanceID])
            #     print(r['InstanceStatuses'][0]['InstanceState']['Name'])
            client = boto3.client('elbv2')
            response = client.register_targets(
                TargetGroupArn=config.load_balancer_ARN,
                Targets=[
                    {
                        'Id': instanceID,
                        'Port': 5000
                    },
                ]
            )
            #return instanceID
            # ec2.wait_until_running()
            # ec2.load()
            # print("Waiting for the checks to finish..")
            # time.sleep(45)

        except:
            e = sys.exc_info()
            flash(e)

    @staticmethod
    def deleteInstanceByID(id):
        '''
        delete instance by ID
        :param id:
        :return: void
        '''
        try:
            ec2 = boto3.resource('ec2')
            ec2.instances.filter(InstanceIds=[id]).terminate()

        except:
            e = sys.exc_info()
            flash("AWS connection error")

    @staticmethod
    def stopInstanceByID(id):
        '''
        stop instance by ID
        :param id:
        :return: void
        '''
        try:
            ec2 = boto3.resource('ec2')
            ec2.instances.filter(InstanceIds=[id]).stop()
        except:
            e = sys.exc_info()
            flash("AWS connection error")

    @staticmethod
    def deleteAllInstanceExceptUserManager():
        '''
        delete instance by ID
        :param id:
        :return: void
        '''
        try:
            instances = EC2.getAllInstance()
            for instance in instances:
                if instance.id == 'i-03d46ce71ce9f19c7' or instance.id == "i-09bf2c7e50e2e7a50":
                    #EC2.stopInstanceByID(instance.id)
                    pass
                else:
                    EC2.deleteInstanceByID(instance.id)

        except:
            e = sys.exc_info()
            flash("AWS connection error")