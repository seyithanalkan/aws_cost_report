import json
import boto3
import os 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

os.chdir('/tmp')

def lambda_handler(event, context):
    

    

    ce = boto3.client('ce', aws_access_key_id='YOUR_AWS_KEY', aws_secret_access_key='YOUR_AWS_SECRET')

    # set the time range for the report (in this example, we are getting the report for the previous day)
    start_time = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    end_time = datetime.today().strftime('%Y-%m-%d')

    # set the filters for the report
    response = ce.get_cost_and_usage(
    TimePeriod={
        'Start': start_time,
        'End':  end_time
    },
    Granularity='DAILY',
    Metrics=['BlendedCost', 'UnblendedCost'],
    GroupBy=[
        {
            'Type': 'TAG',
            'Key': 'Cost_Center'
        },
        

    ]
    )




    # print the report data
    print(response)
    os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"
    # Prepare the data
    cost_centers = []
    blended_costs = []
    unblended_costs = []

    for item in response['ResultsByTime'][0]['Groups']:
        cost_center = item['Keys'][0].replace('Cost_Center$', '')
        cost_centers.append(cost_center)
        blended_costs.append(float(item['Metrics']['BlendedCost']['Amount']))
        unblended_costs.append(float(item['Metrics']['UnblendedCost']['Amount']))

    df = pd.DataFrame({'Cost Center': cost_centers, 'Blended Cost': blended_costs, 'Unblended Cost': unblended_costs})

    # Create the horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 8))

    bar1 = ax.barh(df['Cost Center'], df['Blended Cost'], color='blue', label='Blended cost')
    bar2 = ax.barh(df['Cost Center'], df['Unblended Cost'], color='orange', label='Unblended cost')

    ax.set_xlabel("Cost in USD")
    ax.set_title("Blended and Unblended Cost by Cost Center")
    ax.legend()

    # Format the value labels
    def format_value(val):
        return f'${val:,.2f}'

    for p in bar1.patches:
        width = p.get_width()
        ax.text(width+0.2, p.get_y()+p.get_height()/2, format_value(width), ha="left", va="center", fontsize=10)
    for p in bar2.patches:
        width = p.get_width()
        ax.text(width+0.2, p.get_y()+p.get_height()/2, format_value(width), ha="left", va="center", fontsize=10)

    # Add Cost Center labels inside the bars
    for p, cost_center in zip(bar1.patches, cost_centers):
        width = p.get_width()
        ax.text(width/2, p.get_y()+p.get_height()/2, cost_center, ha="center", va="center", color='white', fontsize=10)

    plt.tight_layout()

    df.to_excel('graph_data.xlsx', index=False, float_format='%.2f')

    #plt.show()

    # Save the chart as a file

    plt.savefig('cost_report.png', dpi=300)

    # Set up the email parameters
    email_from = "abc@abc.com"
    email_to = "abc@abc.com"
    email_subject = "AWS Daily Cost Report"
    email_body = "Please find attached the AWS daily cost report."

    # Attach the image file
    with open('cost_report.png', 'rb') as f:
        img_data = f.read()
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = COMMASPACE.join([email_to])
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_body, 'html'))
    image = MIMEBase('application', 'octet-stream')
    image.set_payload(img_data)
    encoders.encode_base64(image)
    image.add_header('Content-Disposition', 'attachment', filename='cost_report.png')
    msg.attach(image)

    # Attach the Excel file
    with open('graph_data.xlsx', 'rb') as f:
        excel_data = f.read()
    excel = MIMEBase('application', 'octet-stream')
    excel.set_payload(excel_data)
    encoders.encode_base64(excel)
    excel.add_header('Content-Disposition', 'attachment', filename='graph_data.xlsx')
    msg.attach(excel)

    # Create SMTP object
    smtp_obj = smtplib.SMTP_SSL("YOUR_SMTP_SERVER", YOUR_SMTP_SERVER_PORT)
    # Login to the server
    user = "YOUR_SMTP_USER"
    # Replace smtp_password with your Amazon SES SMTP password.
    password = 'YOUR_SMTP_USER_PASSWORD'
    smtp_obj.login(user, password)
    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
