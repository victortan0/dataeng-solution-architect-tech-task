# Import existing bucket
To manage an existing bucket, Terraform needs to import that resource and create state.
```
terraform import aws_s3_bucket.this annalise-ai-datalake
```
Then we can create the relevant files for management going forward.

## Suggested improvements
* Enable object versioning, to prevent loss of data by overwriting (depends on the data)
* KMS encryption with customer managed key, to prevent an "admin" role with permissions like `s3:*` from having default access - they will also need permission to the Key (docs)[https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration]

# Copying data
(docs)[https://aws.amazon.com/premiumsupport/knowledge-center/copy-s3-objects-account/]

The relevant Role will have a Policy allowing READ on `annalise-ai-datalake` bucket and WRITE on `harrison-ai-landing` bucket.
Since this is a cross account action, the `harrison-ai-landing` bucket also needs to allow WRITE to the specific Role, in its own bucket Policy.

## aws s3 sync
(aws s3 sync)[https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/sync.html]

This is only supported through AWS CLI, not boto3, so it can't be done through a "standard" lambda. Instead it must be done through a human (not ideal), or in a docker container which could be on EC2, Batch, or Lambda container.
In either case, a dedicated Role should be created, with ONLY the required permissions for the task. In the case of a human, they should have permission to assume the Role, and use it for the duration of the task.

The command is essentially:
```
aws s3 sync s3://annalise-ai-datalake s3://harrison-ai-landing \
--recursive \
--acl bucket-owner-full-control
```

For bucket to bucket sync, the command will copy an object if:
* The s3 object does not exist in the specified bucket and prefix destination.
* The sizes of the two s3 objects differ.
* The last modified time of the source is newer than the last modified time of the destination.

Which should be reasonable enough for avoiding unnecessary re-copying. 

One issue is the large number of objects, which may overwhelm the command while it tries to enumerate objects (out of memory). This can be managed by batching the objects by their keys, using filters e.g.
```
--exclude "*" --include "a*"
```
Which will only process objects starting with 'a'. The sync command would then be run multiple times i.e.
```
aws s3 sync --exclude "*" --include "a*"
aws s3 sync --exclude "*" --include "b*"
aws s3 sync --exclude "*" --include "c*"
```
Which could potentially be parallelised by running multiple instances.
The number of batches needed might need to be determined experimentally or through research. Especially if the key prefixes are not distributed evenly.
