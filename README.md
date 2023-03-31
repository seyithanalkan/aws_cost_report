# Daily Cost Report for AWS Resources

This is an AWS Lambda project that generates a daily cost report for your AWS resources based on the `Cost_Center` tag that you specify. The report is sent to your email address using the Simple Mail Transfer Protocol (SMTP).

## Getting Started

To use this project, you will need an AWS account and the following information:

- AWS Access Key ID and Secret Access Key
- SMTP server information (host, port, username, and password)

## Prerequisites

You will need the following software installed on your local machine:

- Python 3.8
- AWS CLI

## Installation

1. Clone this repository to your local machine.
2. Open the `lambda_function.py` file and change the following parameters:
   - `YOUR_AWS_KEY`: Replace with your AWS Access Key ID.
   - `YOUR_AWS_SECRET`: Replace with your AWS Secret Access Key.
   - `YOUR_SMTP_SERVER`: Replace with your SMTP server hostname.
   - `YOUR_SMTP_SERVER_PORT`: Replace with your SMTP server port number.
   - `YOUR_SMTP_USER`: Replace with your SMTP username.
   - `YOUR_SMTP_USER_PASSWORD`: Replace with your SMTP password.
3. Zip all files in the repository using the following command: `zip -r function.zip .`.
4. Upload the `function.zip` file to an S3 bucket.
5. Create a new Lambda function in your AWS account.
6. Configure the Lambda function to use the `function.zip` file from the S3 bucket.
7. Create a CloudWatch Event rule to trigger the Lambda function daily.

## Usage

To use this project, follow these steps:

1. Add a `Cost_Center` tag to your AWS resources and set its value to your desired cost center.
2. Wait for the Lambda function to run (either triggered by the CloudWatch Event rule or manually).
3. Check your email for the daily cost report.
