# sagemaker_job.py

import os
import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput

# aws config
sess = sagemaker.Session()
region = os.getenv("AWS_DEFAULT_REGION")
role = os.getenv("SAGEMAKER_ROLE") 
bucket = sess.default_bucket()

# S3 paths
output_data_uri = f"s3://{bucket}/sagemaker-gpu-processing/output/"
script_uri = "process_data.py"

# instance
GPU_INSTANCE_TYPE = 'ml.g4dn.xlarge'

# image
image_uri = sagemaker.image_uris.retrieve(
    framework='pytorch', 
    region=region,
    version='2.0.1',  
    py_version='py310',
    instance_type=GPU_INSTANCE_TYPE,
    image_scope='training'
)

# script processor
processor = ScriptProcessor(
    role=role,
    image_uri=image_uri,
    command=['python3'],
    instance_type=GPU_INSTANCE_TYPE, 
    instance_count=1,
    sagemaker_session=sess
)

# processing job
processor.run(
    code=script_uri, 
    outputs=[
        ProcessingOutput(
            source='/opt/ml/processing/output', 
            destination=output_data_uri,
            output_name='output_results'
        )
    ],
    arguments=['--arg1', 'custom_value'] 
)

print(f"Processing job completed. Results in: {output_data_uri}")