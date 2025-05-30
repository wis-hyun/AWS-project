import boto3
import json

# def query_sagemaker(endpoint_name, payload, region="ap-northeast-2"):
#     runtime = boto3.client("sagemaker-runtime", region_name=region)
#     response = runtime.invoke_endpoint(
#         EndpointName=endpoint_name,
#         ContentType="application/json",
#         Body=json.dumps(payload)
#     )
#     result = json.loads(response["Body"].read().decode())
#     return result
    


# utils/sagemaker_util.py

import boto3
import json
from botocore.config import Config

def query_sagemaker(endpoint_name, payload):
    runtime = boto3.client(
        "sagemaker-runtime",
        region_name="ap-northeast-2",
        config=Config(connect_timeout=60, read_timeout=180)
    )

    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload)
    )

    result = json.loads(response["Body"].read().decode())
    return result
