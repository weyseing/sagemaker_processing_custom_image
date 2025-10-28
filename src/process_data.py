import os
import torch
import argparse

# input/output path
OUTPUT_DATA_PATH = "/opt/ml/processing/output/"

if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument('--arg1', type=str, default='default_value')
    args = parser.parse_args()
    print(f"Arguments: {args}")

    # check GPU
    if torch.cuda.is_available():
        device = torch.device('cuda')
        gpu_index = torch.cuda.current_device()
        print(f"\n--- CUDA Status ---")
        print(f"Using device: {device}")
        print(f"Device Name: {torch.cuda.get_device_name(gpu_index)}")

        # get total GPU memory
        props = torch.cuda.get_device_properties(gpu_index)
        total_gpu_memory_gb = props.total_memory / (1024**3)
        print(f"Total GPU Memory Capacity: {total_gpu_memory_gb:.2f} GB")
        print(f"-------------------")

        # initial check gpu (should still be 0 )
        allocated_gb_init = torch.cuda.memory_allocated(gpu_index) / (1024**3)
        reserved_gb_init = torch.cuda.memory_reserved(gpu_index) / (1024**3)
        print(f"Initial Memory Allocated: {allocated_gb_init:.2f} GB")
        print(f"Initial Memory Reserved: {reserved_gb_init:.2f} GB")
        
        # perform gpu allocation (create tensor requires gpu memory)
        print("\n--- Performing Allocation to GPU ---")
        tensor_size = 25_000_000
        gpu_tensor = torch.randn(tensor_size, device=device)
        print(f"Created a tensor of size: {gpu_tensor.numel()} elements.")
        
        # check gpu
        print("--- Memory Check After Allocation ---")
        allocated_gb = torch.cuda.memory_allocated(gpu_index) / (1024**3)
        reserved_gb = torch.cuda.memory_reserved(gpu_index) / (1024**3)
        print(f"Memory Allocated: {allocated_gb:.2f} GB")
        print(f"Memory Reserved: {reserved_gb:.2f} GB")
        print("------------------------------------")
        
        # cleanup
        del gpu_tensor
        torch.cuda.empty_cache()
    else:
        print("CUDA not available. Using CPU.")

    # output result
    os.makedirs(OUTPUT_DATA_PATH, exist_ok=True)
    with open(os.path.join(OUTPUT_DATA_PATH, 'results.txt'), 'w') as f:
        f.write(f"Processing complete")

    print("Script finished successfully.")
