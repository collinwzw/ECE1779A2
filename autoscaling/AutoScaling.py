import math
from time import sleep
from AWS import aws
from database import database

class AutoScaling:

    @staticmethod
    def read_config():
        db = database.get_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM autoscaling "
        cursor.execute(query)
        result = cursor.fetchall()
        scaling_config = result
        return  scaling_config

    @staticmethod
    def average_cpu_utilization(instanceIDs):
        if len(instanceIDs) != 0:
            average_cpu = []
            for instanceID in instanceIDs:
                cpu = aws.getEC2CPUUsageByID(instanceID,2)
                cpu_stats = []
                for point in cpu['Datapoints']:
                    cpu_stats.append(point['Average'])
                    average_cpu.append(sum(cpu_stats) / len(cpu_stats))
            if len(average_cpu) != 0:
                return sum(average_cpu) / len(average_cpu)
            else:
                return 0
        else:
            return 0

    @staticmethod
    def autoscaling():
        '''run the add worker procedure'''
        # scaling_config = AutoScaling.read_config()
        # cpu_up_threshold = scaling_config[0]["cpu_up_threshold"]
        # cpu_down_threshold = scaling_config[0]["cpu_down_threshold"]
        # cooling_time = scaling_config[0]["cooling_time"]
        # max_worker = scaling_config[0]["max_worker"]
        # min_worker = scaling_config[0]["min_worker"]
        # extend_ratio = scaling_config[0]["extend_ratio"]
        # shrink_ratio = scaling_config[0]["shrink_ratio"]
        print("autoscaler running")
        # AutoScaling.register_idle_worker()
        cpu_up_threshold = 20
        cpu_down_threshold = 10
        cooling_time = 300
        max_worker = 8
        min_worker = 1
        extend_ratio = 1.2
        shrink_ratio = 0.7
        target_instances_id = aws.get_valid_target_instances()
        current_worker = len(target_instances_id)
        print("current worker: " + str(current_worker))
        CPU_average = AutoScaling.average_cpu_utilization(target_instances_id)
        print("CPU usage: " + str(CPU_average))
        ratio = AutoScaling.get_ratio(CPU_average, cpu_up_threshold, cpu_down_threshold, extend_ratio, shrink_ratio)
        delta_number = AutoScaling.get_target_number(current_worker, ratio, max_worker, min_worker)
        print("delta_number: " + str(delta_number))
        if delta_number == 0:
            print("No change")
            sleep(60)
            return
        elif delta_number > 0:
            print("add worker")
            target_ids = []
            for i in range(delta_number):
                new_id = aws.createInstance()
                target_ids.append(new_id)
                print("add worker success")
            sleep(40)
            for instance_id in target_ids:
                aws.addToELB(instance_id)
                print("register success")
            sleep(cooling_time)
        else:
            for i in range(abs(delta_number)):
                AutoScaling.retire_worker()
            print("retire sucess")
            sleep(60)


    @staticmethod
    def get_ratio(cup_load,cpu_up_threshold, cpu_down_threshold,extend_ratio, shrink_ratio):
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
    def get_target_number(current_number, ratio, max_worker, min_worker):
        '''get the target worker number by input the current worker number and ratio
        limit the worker number within max and min value
        '''
        if ratio > 1:
            target = math.ceil(current_number * ratio)
        elif ratio < 1:
            target = int(current_number * ratio)
        else:
            target = 0
        target_fix = max(min_worker,min(target,max_worker))
        delta_number = target_fix - current_number
        return delta_number


    @staticmethod
    def retire_worker():
        """
        Retire one worker from target group and delete it"""
        target_instances_id = aws.get_valid_target_instances()
        print(target_instances_id)
        if len(target_instances_id) > 1:
            retire_instance_id = target_instances_id[-1]
            print(retire_instance_id)
            # unregister instance from target group
            aws.removeELB(retire_instance_id)
            sleep(10)
            aws.deleteInstanceByID(retire_instance_id)
        else:
            return False

    @staticmethod
    def register_idle_worker():
        worker_list = aws.getAllInstanceID()
        target_list = aws.get_valid_target_instances()
        idle_list = list(set(worker_list) - set(target_list))
        if len(idle_list) != 0:
            for instance_id in idle_list:
                aws.addToELB(instance_id)
        else:
            print("all worker in target group")







while True:
    AutoScaling.autoscaling()













