#!/usr/bin/env python3

from aws_cdk import core

from cognito_alb_fargate_demo.cognito_alb_fargate_demo_stack import CognitoAlbFargateDemoStack


app = core.App()
CognitoAlbFargateDemoStack(app, "cognito-alb-fargate-demo")

app.synth()
