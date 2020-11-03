from flask import flash
import sys
import boto3


class S3:

    @staticmethod
    def getAlls3Bucket():
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        try:
            s3 = boto3.resource('s3')
            instances = s3.instances.all()
            return instances
        except:
            e = sys.exc_info()
            flash("AWS connection error")

    @staticmethod
    def deleteFileFromBucket(bucket_id, key_id):
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        try:
            s3 = boto3.client('s3')
            s3.delete_object(Bucket=bucket_id, Key=key_id)
        except:
            e = sys.exc_info()
            flash("AWS connection error")

    @staticmethod
    def uploadFileFromBucket(bucket_id, file, filename ):
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        try:
            s3 = boto3.client('s3')
            s3.upload_fileobj(file, bucket_id, filename)
        except:
            e = sys.exc_info()
            flash("AWS connection error")