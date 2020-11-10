import boto3
from datetime import datetime, timedelta



class CloudWatch:

    @staticmethod
    def getEC2CPUUsageByID(id):
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
            StartTime=datetime.utcnow() - timedelta(seconds=60 * 60),
            EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
            MetricName=metric_name,
            Namespace=namespace,  # Unit='Percent',
            Statistics=[statistic],
            Dimensions=[{'Name': 'InstanceId', 'Value': id}]
        )
        return cpu


    @staticmethod
    def average_cpu_utilization():
        valid_instances_id = ec2.getAllInstance()
        l = len(valid_instances_id)
        logging.warning('valid_instances_id:{}'.format(valid_instances_id))
        start_time, end_time = get_time_span(600)
        cpu_sum = 0
        for i in range(l):
            response = CloudWatch.getEC2CPUUsageByID(valid_instances_id[i], start_time, end_time)
            response = json.loads(response)
            logging.warning(response)
            if response and response[0]:
                cpu_sum += response[0][1]
        return cpu_sum / l if l else -1


    @staticmethod
    def getHttpRequestRateByID(id):
        pass


