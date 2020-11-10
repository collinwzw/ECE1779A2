import math
from datetime import datetime, timedelta, time
from app import EC2,CloudWatch
import sys
import schedule


cpu_up_threshold = 80
cpu_down_threshold = 25
cooling_time = 300
max_worker = 8
min_worker = 1
extend_ratio = 1.2
shrink_ratio = 0.8

class AutoScaler:

    @staticmethod
    def autoscaling():
        '''run the add worker procedure'''
        target_instances_id = EC2.ec2.getAllInstance()
        response_list = []
        current_worker = len(response_list)
        CPUutilization = CloudWatch.CloudWatch.average_cpu_utilization()
        ratio = AutoScaler.get_ratio(CPUutilization)
        delta_number = AutoScaler.get_target_number(current_worker,ratio)
        if delta_number == 0:
            return
        elif delta_number > 0:
            for i in delta_number:
                EC2.EC2.createInstance()
        elif delta_number < 0:
            for i in -(delta_number):
                EC2.EC2.retireInstance()
        if delta_number != 0:
            time.sleep(cooling_time)
        else:
            return


    @staticmethod
    def get_ratio(cup_load):
        '''calculate the ratio of expand or shrink workers by cpuload
        '''
        if cup_load >= cpu_up_threshold:
            ratio = extend_ratio
        elif cup_load <= cpu_down_threshold:
            ratio = shrink_ratio
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
            target = current_number - int(current_number * ratio)
        else:
            target = 0
        target_fix = max(min_worker,min(target,max_worker))
        delta_number = target_fix - current_number
        return delta_number


if __name__ == '__main__':
    # start auto-scaling
    schedule.every(1).minute.do(AutoScaler.auto_scaling)


