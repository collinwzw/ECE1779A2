import boto3
from app import config
from flask import flash
import sys


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

            return instances
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
            ec2 = boto3.resource('ec2')
            ec2.create_instances(ImageId=config.ami_id, MinCount=1, MaxCount=1,
                                 InstanceType='t2.small', SubnetId=config.subnet_id)
        except:
            e = sys.exc_info()
            flash("AWS connection error")

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
                if instance.id == 'i-098e454f6b1f916e0' or instance.id == "i-0aa12d6d91bd44178":
                    pass
                else:
                    EC2.stopInstanceByID(instance.id)

        except:
            e = sys.exc_info()
            flash("AWS connection error")