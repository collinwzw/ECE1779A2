import math
from datetime import datetime, timedelta, time
from app import EC2,CloudWatch
import sys
import schedule
from app.database.dbManager import dbManager
from app.LoadBalancer import LoadBalancer


cpu_up_threshold = 80
cpu_down_threshold = 25
cooling_time = 300
max_worker = 8
min_worker = 1
extend_ratio = 1.2
shrink_ratio = 0.8

class AutoScaler:

    @staticmethod
    def read_config():
        scaling_config = dbManager.fetch_autoscaling_parameter("config")
        return  scaling_config

    @staticmethod
    def average_cpu_utilization(instanceIDs):
        average_cpu = []
        for instanceID in instanceIDs:
            cpu = CloudWatch.getEC2CPUUsageByID(instanceID, 2)
            cpu_stats = []
            for point in cpu['Datapoints']:
                cpu_stats.append(point['Average'])
            average_cpu.append(sum(cpu_stats) / len(cpu_stats))

        return sum(average_cpu) / len(average_cpu)


    @staticmethod
    def autoscaling():
        '''run the add worker procedure'''
        # target_instances_id = EC2.ec2.getAllInstanceID()
        # response_list = []# ELB target group worker
        # AutoScaler.read_config()
        # current_worker = len(response_list)
        # CPUutilization = AutoScaler.average_cpu_utilization(target_instances_id)
        target_instances_id = LoadBalancer.get_valid_target_instances()
        scaling_config = dbManager.fetch_autoscaling_parameter()
        current_worker = len(target_instances_id)
        CPUutilization = CloudWatch.CloudWatch.average_cpu_utilization()
        ratio = AutoScaler.get_ratio(CPUutilization)
        delta_number = AutoScaler.get_target_number(current_worker,ratio)
        if delta_number == 0:
            return
        elif delta_number > 0:
            for i in range(delta_number):
                EC2.EC2.createInstance()
        else:
            for i in range(abs(delta_number)):
                AutoScaler.retire_worker()
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


    @staticmethod
    def retire_worker():
        """
        shrink one instance into the self.TargetGroupArn
        :return: msg: str
        """
        target_instances_id = LoadBalancer.get_valid_target_instances()
        flag, msg = True, ''
        if len(target_instances_id) > 1:
            retire_instance_id = target_instances_id[0]
            # unregister instance from target group
            response = LoadBalancer.removeELB(retire_instance_id)
            status = -1
            if response and 'ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata']:
                status = response['ResponseMetadata']['HTTPStatusCode']
            if int(status) == 200:
                status_2 = -1
                response_2 = EC2.EC2.deleteInstanceByID(retire_instance_id)
                if response_2 and 'ResponseMetadata' in response_2 and 'HTTPStatusCode' in response_2['ResponseMetadata']:
                    status2 = response_2['ResponseMetadata']['HTTPStatusCode']
                if int(status2) != 200:
                    flag = False
                    msg = "Unable to stop the unregistered instance"
            else:
                flag = False
                msg = "Unable to unregister from target group"

        else:
            flag = False
            msg = "No workers to unregister"

        return [flag, msg]


    @staticmethod
    def register_workers():
        pass









if __name__ == '__main__':
    # start auto-scaling
    schedule.every(1).minute.do(AutoScaler.autoscaling)


