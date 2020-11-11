import boto3

class LoadBalancer:
    @staticmethod
    def register_instance(instance_id):
        client = boto3.client('elb')
        client.register_instances_with_load_balancer(



        )