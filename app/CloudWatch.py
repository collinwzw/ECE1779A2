import boto3
from datetime import datetime, timedelta
from app import config


class CloudWatch:

    @staticmethod
    def getEC2CPUUsageByID(id,past_minute):
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
    def getHttpRequestRateByID(id):
        metric_name = 'CPUUtilization'

        ##    CPUUtilization, NetworkIn, NetworkOut, NetworkPacketsIn,
        #    NetworkPacketsOut, DiskWriteBytes, DiskReadBytes, DiskWriteOps,
        #    DiskReadOps, CPUCreditBalance, CPUCreditUsage, StatusCheckFailed,
        #    StatusCheckFailed_Instance, StatusCheckFailed_System

        namespace = 'OpsNameSpace'
        statistic = 'Sum'  # could be Sum,Maximum,Minimum,SampleCount,Average
        client = boto3.client('cloudwatch')
        httpRequest = client.get_metric_statistics(
            Period=1 * 60,
            StartTime=datetime.utcnow() - timedelta(seconds=30 * 60),
            EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
            MetricName='HttpRequestCount',
            Namespace=namespace,  # Unit='Percent',
            Statistics=[statistic],
            Dimensions=[{'Name': 'instanceID', 'Value': id}]
        )
        return httpRequest

    @staticmethod
    def getWorkerNumber():
        namespace = 'AWS/ApplicationELB'
        statistic = 'Maximum'  # could be Sum,Maximum,Minimum,SampleCount,Average
        unit = 'Count'
        client = boto3.client('cloudwatch')
        response = client.get_metric_statistics(
            Period=1 * 60,
            StartTime=datetime.utcnow() - timedelta(seconds=30 * 60),
            EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
            MetricName = 'HealthyHostCount',
            Namespace = namespace,
            Unit = unit,
            Statistics=[statistic],
            Dimensions = [
                {
                    'Name': 'TargetGroup',
                    'Value': config.load_balancer_ARN,
                },

                {
                    'Name': 'LoadBalancer',
                    'Value': 'app/ece1779a2/61d07839336d9063',
                },
            ]

        )
        return response
