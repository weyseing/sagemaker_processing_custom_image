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
input_data_uri = f"s3://{bucket}/path/to/your/input/data/" 
output_data_uri = f"s3://{bucket}/path/for/output/results/"
script_uri = "process_data.py"

# image
image_uri = sagemaker.image_uris.retrieve(
    framework='pytorch', 
    region=region,
    version='2.0.1',  
    py_version='py310',
    instance_type='ml.p3.2xlarge',
    image_scope='training'
)

# script processor
processor = ScriptProcessor(
    role=role,
    image_uri=image_uri,
    command=['python3'],
    instance_type='ml.g4dn.xlarge', 
    instance_count=1,
    sagemaker_session=sess
)

# processing job
processor.run(
    code=script_uri, 
    inputs=[
        ProcessingInput(
            source=input_data_uri,
            destination='/opt/ml/processing/input/data',
            input_name='input_data'
        )
    ],
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