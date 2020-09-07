# User Management With Cognito, Fargate, Python and the CDK

This is the repository that belongs to my talk on the topic above.
The code in this repo sets up the following architecture:

- A VPC across 2 AZs with internet connectivity for both kinds of subnets (this means NAT Gateways that aren't shown on the diagram are provisioned as well)
- A backend application running inside a Docker container which gets provisioned by the CDK and runs in an ECS Service on top of Fargate
- A Cognito user pool to hold users and let users authenticate against
  - A lambda function that automatically confirms all users (Pre-Sign-Up hook)
- An Application Load Balancer that sits in front of the backend application and authenticates users against Cognito before traffic may pass to the backend
- Several entries in a hosted Zone of your choice, which route traffic to the ALB and confirm a certificate for the endpoint in that zone

![Architecture](architecture.png)

## Prerequisites

- Your own Hosted Zone

## Deployment Steps

TODO
