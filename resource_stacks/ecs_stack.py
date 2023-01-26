from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_ecs as _ecs,
    aws_ecs_patterns as _ecs_patterns
)

class EcsStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        app = core.App()
        vpc = _ec2.Vpc(
            self,
            "ecsVpc",
            max_azs=2,
            nat_gateways=1
        )
        
        # Cluster
        ecs_cluster = _ecs.Cluster(
            self,
            "ecsCluster",
            cluster_name="ecs-cluster",
            vpc=vpc
        )
        
        # Minimal ASG
        ecs_cluster.add_capacity(
            "EcsASG",
            auto_scaling_group_name="ecs-asg",
            instance_type=_ec2.InstanceType("t2.micro")
        )
        
        # Load balancer, Container Definition, Service, and Task
        ecs_load_balancer = _ecs_patterns.ApplicationLoadBalancedEc2Service(
            self,
            "ecsLoadBalancer",
            cluster=ecs_cluster,
            memory_reservation_mib=512,
            memory_limit_mib=2048,
            listener_port=80,
            load_balancer_name="ecs-load-balancer",
            task_image_options={
                # Use canned Amazon demo image
                "image":_ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                # How to pass environment vars to your image
                "environment": {
                    "ENVIRONMENT":"Test"
                }
            },
            service_name="ecs-service",
            desired_count=1
        )

        # Echo URL
        output=core.CfnOutput(
            self,
            "ecsURL",
            value=f"{ecs_load_balancer.load_balancer.load_balancer_dns_name}"
        )