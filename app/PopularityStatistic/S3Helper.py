import boto3 as boto3
from botocore.exceptions import ClientError
from flask import logging

def create_presigned_url_expanded(objName):
    """Generate a presigned URL to invoke an S3.Client method

    Not all the client methods provided in the AWS Python SDK are supported.

    :param client_method_name: Name of the S3.Client method, e.g., 'list_buckets'
    :param method_parameters: Dictionary of parameters to send to the method
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param http_method: HTTP method to use (GET, etc.)
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 client method
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': 'ece1779-a3-bucket',
                                    'Key': objName,
                                },
                                ExpiresIn=30)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response