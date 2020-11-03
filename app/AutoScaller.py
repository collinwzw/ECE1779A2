import math
from datetime import datetime, timedelta


cpu_up_threshold = 80
cpu_down_threshold = 25
cooling_time = 300
max_worker = 8
min_worker = 1


class AutoScaler:

    @staticmethod
    def retire_instance(desire_number):
        '''run the retire worker procedure'''







    @staticmethod
    def add_instance(desire_number):
        '''run the add worker procedure'''
        for i in range(desire_number):
            instances = ec2.create_instances(ImageId=config.ami_id, InstanceType='t2.small', MinCount=1, MaxCount=1,
                                             Monitoring={'Enabled': True},
                                             Placement={'AvailabilityZone': 'us-east-1a', 'GroupName': 'A2_workerpool'},
                                             SecurityGroups=[
                                                 'launch-wizard-2',
                                             ],
                                             KeyName='keypair', TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'Additional_workers'
                            },
                        ]
                    }, ])


            #register in elb
        # for instance in instances:
        #     client.register_instances_with_load_balancer(
        #         LoadBalancerName='ece1779A2',
        #         Instances=[Instances = [{'InstanceId': instance.id}]
        #         )

        # wait until finish
        # waiter = client.get_waiter('instance_in_service')
        #     waiter.wait(
        #         LoadBalancerName='ece1779A2',
        #         Instances=[{'InstanceId': instance.id}])



    @staticmethod
    def auto_scaling(cup_load, buffer_time):
        '''calculate the ratio of expand or shrink workers by cpuload
        '''
        if cup_load >= cpu_up_threshold and buffer_time >= cooling_time:
            ratio = 1.2
        elif cup_load <= cpu_down_threshold and buffer_time >= cooling_time:
            ratio = 0.8
        else:
            ratio = 1
        return ratio


    @staticmethod
    def get_target_number(current_number, ratio):
        '''get the target worker number by input the current worker number and ratio
        limit the worker number within max and min value
        '''
        if ratio > 1:
            target = math.ceil(current_number * ratio)
        elif ratio < 1:
            target = int(current_number * ratio)
        else:
            target = current_number
        target_fix = max(min_worker,min(target,max_worker))
        return target_fix


AutoScaler = AutoScaler()

target = AutoScaler.get_target_number(1,0.8)
print(target)


cpu_average = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': 'i-1234abcd'
                },
            ],
            StartTime=datetime(2018, 4, 23) - timedelta(seconds=600),
            EndTime=datetime(2018, 4, 24),
            Period=86400,
            Statistics=[
                'Average',
            ],
            Unit='Percent'
)




