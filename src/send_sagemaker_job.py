# src/sagemaker_job.py

import os
import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput

# aws config
sess = sagemaker.Session()
role = os.getenv("SAGEMAKER_ROLE") 

# instance
GPU_INSTANCE_TYPE = 'ml.g4dn.xlarge'

# image
image_uri = os.getenv("AWS_ECR_ENDPOINT") + ":latest"

# script file & input file
script_uri = "/app/src/job_script.py"
local_input_file = "/app/src/input_file.txt"

# script processor
processor = ScriptProcessor(
    role=role,
    image_uri=image_uri,
    command=['python3'],
    instance_type=GPU_INSTANCE_TYPE, 
    instance_count=1,
    sagemaker_session=sess,
    base_job_name="poc-sagemaker-processing"
)

# processing job
processor.run(
    # script file
    code=script_uri, 
    # input files
    inputs=[
        ProcessingInput(
            source=local_input_file,
            destination='/opt/ml/processing/input',
            input_name='input_file'
        )
    ],
    # output files
    outputs=[
        ProcessingOutput(
            source='/opt/ml/processing/output', 
            destination=None,
            output_name='output_results'
        )
    ],
    # arguments
    arguments=[
        '--input-path', '/opt/ml/processing/input',
        '--output-path', '/opt/ml/processing/output',
        '--input-filename', 'input_file.txt'
    ]
)

print(f"Processing job completed")