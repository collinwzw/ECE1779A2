from flask import render_template, redirect, url_for, request
from app import app

import boto3
from app import config
from datetime import datetime, timedelta
from operator import itemgetter



class EC2:

    @staticmethod
    def getAllInstance():
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        ec2 = boto3.resource('ec2')
        instances = ec2.instances.all()
        return instances

    @staticmethod
    def getInstanceByStatus(filters):
        '''
        get ec2 instance by status
        :param filters:
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        ec2 = boto3.resource('ec2')
        instances = ec2.instances.filter(Filters=filters)
        return instances

    @staticmethod
    def getInstanceByID(id):
        '''
        get instance by ID
        :param id:
        :return: ec2 instance
        '''
        ec2 = boto3.resource('ec2')

        instance = ec2.Instance(id)
        return instance

    @staticmethod
    def createInstance():
        '''
        create one instance of pre-defined imageID with pre-defined subnet_id
        :return: void
        '''
        ec2 = boto3.resource('ec2')
        ec2.create_instances(ImageId=config.ami_id, MinCount=1, MaxCount=1,
                             InstanceType='t2.small', SubnetId=config.subnet_id)

    @staticmethod
    def getDeleteInstanceByID(id):
        '''
        delete instance by ID
        :param id:
        :return: void
        '''
        ec2 = boto3.resource('ec2')

        ec2.instances.filter(InstanceIds=[id]).terminate()

