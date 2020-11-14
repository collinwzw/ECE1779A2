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
            buckets = s3.buckets.all()
            return buckets
        except:
            e = sys.exc_info()
            flash("S3 connection error, get all object failed")

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
            flash("S3 connection error, dekdete file failed")

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
            flash("S3 connection error, upload failed")

    @staticmethod
    def deleteAllFileFromBucket(bucket_id):
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        try:
            s3 = boto3.client('s3')
            files = s3.list_objects(Bucket=bucket_id)
            for file in files['Contents']:
                S3.deleteFileFromBucket(bucket_id,file['Key'])
        except:
            e = sys.exc_info()
            flash("S3 connection error")

