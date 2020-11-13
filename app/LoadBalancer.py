import boto3
from app import config


class LoadBalancer:
    @staticmethod
    def get_target_worker():
        elb = boto3.resource('elbv2')
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
        target_instances = LoadBalancer.get_target_worker()
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
