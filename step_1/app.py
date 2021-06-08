from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_efs as efs,
    aws_logs,
    core
)

from os import getenv


class ECSLoggingDemo(core.Stack):

    def __init__(self, scope: core.Stack, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ## VPC and ECS Cluster ##
        self.vpc = ec2.Vpc(self, "VPC", max_azs=2)

        self.ecs_cluster = ecs.Cluster(
            self, "ECSCluster",
            cluster_name="ECS-Logging-Demo",
            vpc=self.vpc
        )
        ## End VPC and ECS Cluster ##

        ## Load balancer for ECS service ##
        self.frontend_sec_grp = ec2.SecurityGroup(
            self, "FrontendIngress",
            vpc=self.vpc,
            allow_all_outbound=True,
            description="Frontend Ingress All port 80",
        )

        # Task execution role
        self.task_execution_role = iam.Role(
            self, "TaskExecutionRole",
            assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
            description="Task execution role for ecs services",
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(self, 'arn', managed_policy_arn='arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy')
            ]
        )

        ## END IAM ##
        self.service_log_group = aws_logs.LogGroup(self, "ECSLoggingDemoLogGrp")
        ## Logging ##
        
        
        ## ##

        # Cloudformation Outputs
        core.CfnOutput(
            self, "ExecutionRoleARN",
            value=self.task_execution_role.role_arn,
            export_name="ECSLoggingDemoTaskExecutionRoleARN"
        )

        core.CfnOutput(
            self, "VPCPrivateSubnets",
            value=",".join([x.subnet_id for x in self.vpc.private_subnets]),
            export_name="ECSLoggingDemoPrivSubnets"
        )

        
        core.CfnOutput(
            self, "LogGroupName",
            value=self.service_log_group.log_group_name,
            export_name="ECSLoggingDemoLogGroupName"
        )


app = core.App()

ECSLoggingDemo(app, "ecsworkshop-logging-demo")

app.synth()
