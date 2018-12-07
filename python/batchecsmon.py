import boto3
import json
import logging
import time
 
ecs = boto3.client('ecs')
ec2 = boto3.client('ec2')
batch = boto3.client('batch')

logging.basicConfig(filename='batch.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
while True: 
 compute_environments = batch.describe_compute_environments()
 logging.info('getting compute environments')
 logging.info(compute_environments)
 for ce in compute_environments['computeEnvironments']:
        compute_environment_name = ce['computeEnvironmentName']
        ecs_clusters = ecs.list_clusters()
        for ecs_cluster in ecs_clusters['clusterArns']:
                     if compute_environment_name in ecs_cluster:
 
                           ci_list_response = ecs.list_container_instances(
                            cluster= ecs_cluster
                           )
                           logging.info('starting ecs cluster name' + ecs_cluster)
                           logging.info('list ecs container instances response')
                           logging.info(ci_list_response)
 
 
                           # Describe those ARNs
                           ci_descriptions_response = ecs.describe_container_instances(
                           cluster= ecs_cluster,
                            containerInstances=ci_list_response['containerInstanceArns']
                           )
                           logging.info(ci_descriptions_response)
 
 
                           # go through instances and log tasks
                           for ci in ci_descriptions_response['containerInstances']:
                                   # List tasks on this container instance
                                   t_list_response = ecs.list_tasks(
                                   cluster= ecs_cluster,
                                   containerInstance=ci['containerInstanceArn']
                                   )
				   logging.info('container instance: ' + ci['ec2InstanceId'])
                                   logging.info('list task response')
                                   logging.info(t_list_response)
 				   
				   if not t_list_response['taskArns']:
					continue;

                                   #Describe tasks
                                   t_descriptions_response = ecs.describe_tasks(
                                   cluster= ecs_cluster,
                                   tasks=t_list_response['taskArns']
                                   )
                                   logging.info('describe task response')
                                   logging.info(t_list_response)
 time.sleep(60)
