import math


class AutoScaler:
    cpu_up_threshold = 80
    cpu_down_threshold = 25
    cooling_time = 300
    max_worker = 8
    min_worker = 1

    def retire_instance(self, target_number):
        '''run the retire worker procedure'''
        pass

    def add_instance(self, target_number):
        '''run the add worker procedure'''
        pass

    def auto_scaling(self, cup_load, buffer_time):
        '''calculate the ratio of expand or shrink workers by cpuload
        '''
        if cup_load >= self.cpu_up_threshold and buffer_time >= self.cooling_time:
            ratio = 1.2
        elif cup_load <= self.cpu_down_threshold and buffer_time >= self.cooling_time:
            ratio = 0.8
        else:
            ratio = 1
        return ratio

    def get_target_number(self,current_number, ratio):
        '''get the target worker number by input the current worker number and ratio
        limit the worker number within max and min value
        '''
        if ratio > 1:
            target = math.ceil(current_number * ratio)
        elif ratio < 1:
            target = int(current_number * ratio)
        else:
            target = current_number
        target_fix = max(self.min_worker,min(target,self.max_worker))
        return target_fix


AutoScaler = AutoScaler()

target = AutoScaler.get_target_number(1,0.8)
print(target)






