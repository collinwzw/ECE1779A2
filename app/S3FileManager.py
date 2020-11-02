from flask import render_template, redirect, url_for, request
from app import app

import boto3


class S3:

    @staticmethod
    def getAllInstance():
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        s3 = boto3.resource('s3')
        instances = s3.instances.all()
        return instances
