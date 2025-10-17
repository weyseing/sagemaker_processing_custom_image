# proces_data.py

import os
import argparse

# input/output path
INPUT_DATA_PATH = "/opt/ml/processing/input/data/"
OUTPUT_DATA_PATH = "/opt/ml/processing/output/"

if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument('--arg1', type=str, default='default_value')
    args = parser.parse_args()
    print(f"Arguments: {args}")

    # check GPU
    num_gpus = os.environ.get('SM_NUM_GPUS', 0)
    print(f"Number of GPUs available: {num_gpus}")

    # output result
    os.makedirs(OUTPUT_DATA_PATH, exist_ok=True)
    with open(os.path.join(OUTPUT_DATA_PATH, 'results.txt'), 'w') as f:
        f.write(f"Processing complete on {num_gpus} GPUs.")

    print("Script finished successfully.")