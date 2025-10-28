# src/job_script.py

import os
import torch
import argparse

if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', type=str, required=True, help='Path to input directory')
    parser.add_argument('--output-path', type=str, required=True, help='Path to output directory')
    parser.add_argument('--input-filename', type=str, default='input_file.txt', help='Name of input file')
    args = parser.parse_args()
    print(f"Input path: {args.input_path}")
    print(f"Output path: {args.output_path}")
    print(f"Input filename: {args.input_filename}")

    # Read input file
    input_file_path = os.path.join(args.input_path, args.input_filename)
    print(f"Reading input file: {input_file_path}")
    with open(input_file_path, 'r') as f:
        file_content = f.read()
    print(f"=== INPUT FILE CONTENT ===")
    print(file_content)
    print(f"=== END OF INPUT FILE ===")

    # check GPU
    if torch.cuda.is_available():
        # GPU device info
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
    os.makedirs(args.output_path, exist_ok=True)
    output_file_path = os.path.join(args.output_path, 'results.txt')
    with open(output_file_path, 'w') as f:
        f.write(f"Processing complete\n")
        f.write(f"Input file content:\n{file_content}\n")
        f.write(f"GPU available: {torch.cuda.is_available()}\n")
        f.write(f"Input path used: {args.input_path}\n")
        f.write(f"Output path used: {args.output_path}\n")
    print(f"Results written to: {output_file_path}")
    
print("Script finished successfully.")