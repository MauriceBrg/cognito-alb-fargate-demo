#!/usr/bin/env python3
"""Entrypoint to the cognito alb fargate demo CDK app"""

from aws_cdk import core

from infrastructure.demo_stack import DemoStack
from infrastructure.configuration import get_config

def main():
    """Wrapper for the CDK app"""
    app = core.App()

    DemoStack(
        app,
        "cognito-alb-fargate-demo",
        config=get_config()
    )

    app.synth()


if __name__ == "__main__":
    main()
