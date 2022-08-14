# Transition object storage class
[https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html]

Configure a bucket lifecycle policy to transition the objects into GLACIER Storage Class.
While there are minimum object age rules and charges for transitioning to Infrequent Access classes, there are none for Glacier classes.
The policy would be applied in the usual way the bucket is managed e.g. manually, terraform etc.

The lifecycle policy will have:
* Scope: all objects
* Transition period: 0 days
* Storage class: GLACIER (S3 Glacier Flexible Retrieval)

This way, no scripts for iterating the bucket are needed, which would take too long for so many objects.
It may take a few days to actually transition all objects.
