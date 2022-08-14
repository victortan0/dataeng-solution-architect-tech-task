# Speed up the bucket listing process
Specify a prefix inside the list objects command:
```
PREFIX='a'
page_iter = s3.get_paginator('list_objects_v2').paginate(
    Bucket=BUCKET_NAME,
    Prefix=PREFIX,
)
```
Which can be injected via environment variable. Then the script can be run on each prefix.
The script could also be run on multiple instances (with a different prefix) to parallelise the execution, such as on EC2, Batch, or Lambda.


# Make the process idempotent
[https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html]

Use a FIFO SQS queue, and enable message deduplication. 
By default, this is based on the hashed message content which will be unique per object in the bucket.
The deduplication ID could also be specified explicitly as the object key itself:
```
sqs.send_message(
    MessageDeduplicationId=key,
)
```
