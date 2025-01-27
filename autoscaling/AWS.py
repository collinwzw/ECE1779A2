from datetime import datetime, timedelta
import boto3
from app import config

class aws:


    @staticmethod
    def getEC2CPUUsageByID(id, past_minute):
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        metric_name = 'CPUUtilization'

        ##    CPUUtilization, NetworkIn, NetworkOut, NetworkPacketsIn,
        #    NetworkPacketsOut, DiskWriteBytes, DiskReadBytes, DiskWriteOps,
        #    DiskReadOps, CPUCreditBalance, CPUCreditUsage, StatusCheckFailed,
        #    StatusCheckFailed_Instance, StatusCheckFailed_System

        namespace = 'AWS/EC2'
        statistic = 'Average'  # could be Sum,Maximum,Minimum,SampleCount,Average
        client = boto3.client('cloudwatch')
        cpu = client.get_metric_statistics(
            Period=1 * 60,
            StartTime=datetime.utcnow() - timedelta(seconds=past_minute * 60),
            EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
            MetricName=metric_name,
            Namespace=namespace,  # Unit='Percent',
            Statistics=[statistic],
            Dimensions=[{'Name': 'InstanceId', 'Value': id}]
        )

        return cpu

    @staticmethod
    def get_target_worker():
        elb = boto3.client('elbv2')
        response = elb.describe_target_health(
            TargetGroupArn=config.load_balancer_ARN,
        )
        instances = []
        if 'TargetHealthDescriptions' in response:
            for target in response['TargetHealthDescriptions']:
                instances.append({
                    'Id': target['Target']['Id'],
                    'Port': target['Target']['Port'],
                    'State': target['TargetHealth']['State']
                })
        return instances

    @staticmethod
    def get_valid_target_instances():
        target_instances = aws.get_target_worker()
        target_instances_id = []
        for item in target_instances:
            if item['State'] != 'draining':
                target_instances_id.append(item['Id'])
        return target_instances_id

    @staticmethod
    def removeELB(instanceID):
        try:
            client = boto3.client('elbv2')
            response = client.deregister_targets(
                TargetGroupArn=config.load_balancer_ARN,
                Targets=[
                    {
                        'Id': instanceID,
                        'Port': 5000,
                    },
                ]
            )
            return response
        except:
            e = sys.exc_info()
            flash(e)

    @staticmethod
    def addToELB(instanceID):
        try:
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
            return response
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
                                            # UserData=f"\n#!/bin/bash\ncd Desktop\nchmod u+x start.sh\n./start.sh \n",
                                            # UserData=f"\n#!/bin/bash\ncd Desktop\n./start.sh \n",
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
