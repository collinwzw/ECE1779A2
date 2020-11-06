import math
from datetime import datetime, timedelta
from app import EC2

cpu_up_threshold = 80
cpu_down_threshold = 25
cooling_time = 300
max_worker = 8
min_worker = 1
upper_ratio = 1.2
lower_ratio = 0.8

class AutoScaler:
    cpu_up_threshold = 80
    cpu_down_threshold = 25
    cooling_time = 300
    max_worker = 8
    min_worker = 1
    upper_ratio = 1.2
    lower_ratio = 0.8

    @staticmethod
    def retire_instance(retire_number):
        '''run the retire worker procedure'''
        #ids_to_delete = ids[:(retire_number]
        # resize ELB
        # for id in ids_to_delete:
        #     client.deregister_instances_from_load_balancer(
        #         LoadBalancerName='ece1779A2',
        #         Instances=[Instances = [{'InstanceId': instance.id}])
        #     # wait until finish
        #     waiter = client.get_waiter('instance_deregistered')
        #     waiter.wait(
        #         LoadBalancerName='ece1779A2',
        #         Instances=[{'InstanceId': id}])
        #     # drop instances
        #     for id in ids_to_delete:
        #         ec2.instances.filter(InstanceIds=[id]).terminate()







    @staticmethod
    def add_instance(add_number):
        '''run the add worker procedure'''
        for i in range(add_number):
            id = EC2.createInstance()

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
            ratio = upper_ratio
        elif cup_load <= cpu_down_threshold and buffer_time >= cooling_time:
            ratio = 0.8
        else:
            ratio = lower_ratio
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




