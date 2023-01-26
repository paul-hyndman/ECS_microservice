#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from resource_stacks.ecs_stack import EcsStack

app = cdk.App()
EcsStack(app, "EcsStack")
app.synth()
