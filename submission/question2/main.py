import os
import boto3

sqs = boto3.client('sqs')
s3 = boto3.client('s3')


def main(queue_url, bucket_name, object_prefix):
    page_iter = s3.get_paginator('list_objects_v2').paginate(
        Bucket=bucket_name,
        Prefix=object_prefix,
    )
    for page in page_iter:
        for obj in page['Contents']:
            send_message(queue_url, obj['Key'])


def send_message(queue_url, key):
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody="{'bucket:' 'my-s3-bucket', 'key': '" + key + "'}",  # sic `'bucket':`
    )


def handler(event, context):
    queue_url = event['QUEUE_URL']
    bucket_name = event['BUCKET_NAME']
    object_prefix = event['OBJECT_PREFIX']

    main(queue_url, bucket_name, object_prefix)


if __name__ == "__main__":
    queue_url = os.environ['QUEUE_URL']
    bucket_name = os.environ['BUCKET_NAME']
    object_prefix = os.environ['OBJECT_PREFIX']

    main(queue_url, bucket_name, object_prefix)
