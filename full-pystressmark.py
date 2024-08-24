import multiprocessing
import time
import speedtest as speedtest_cli
import torch
import statistics

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def stress_cpu():
    num = 10**6
    while True:
        # Find the next prime number after `num` (CPU stress)
        num += 1
        is_prime(num)

def stress_gpu():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    while True:
        # Generate large random tensors and multiply them on the GPU (GPU stress)
        matrix_size = 5000
        A = torch.rand((matrix_size, matrix_size), device=device)
        B = torch.rand((matrix_size, matrix_size), device=device)
        torch.matmul(A, B)

def test_internet_speed():
    st = speedtest_cli.Speedtest()
    
    # Get best server based on ping
    print("Selecting best server based on ping...")
    best_server = st.get_best_server()
    print(f"Connected to server: {best_server['host']} located in {best_server['country']}")
    
    # Measure ping (latency)
    latency = best_server['latency']
    print(f"Ping: {latency:.2f} ms")
    
    # Measure download speed
    print("Testing download speed...")
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    print(f"Download speed: {download_speed:.2f} Mbps")

    # Measure upload speed
    print("Testing upload speed...")
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    print(f"Upload speed: {upload_speed:.2f} Mbps")

def benchmark_cpu():
    def cpu_benchmark(duration):
        """Perform CPU-intensive operations for a specific duration and return operations per second."""
        start_time = time.time()
        operations = 0
        while True:
            num = 10**6 + operations
            is_prime(num)
            operations += 1
            if time.time() - start_time >= duration:
                break
        elapsed_time = time.time() - start_time
        return operations / elapsed_time

    duration = 60  # Run the benchmark for 60 seconds
    print("Running CPU benchmark...")
    num_trials = 3
    results = [cpu_benchmark(duration) for _ in range(num_trials)]
    average_ops_per_sec = statistics.mean(results)
    print(f"Benchmark completed. Average operations per second over {num_trials} trials: {average_ops_per_sec:.2f}")

def main():
    while True:
        print("Select an option:")
        print("1. Internet Speed Test")
        print("2. CPU Stress Test")
        print("3. GPU Stress Test")
        print("4. CPU Benchmark")
        print("5. Run CPU and GPU Stress Test Simultaneously")
        print("6. Exit")

        choice = input("Enter the number of the option you want to run: ").strip()

        if choice == '1':
            print("Starting internet speed test...")
            test_internet_speed()

        elif choice == '2':
            cpu_count = multiprocessing.cpu_count()
            print(f"Starting CPU stress test with {cpu_count} CPU cores.")
            cpu_processes = [multiprocessing.Process(target=stress_cpu) for _ in range(cpu_count)]
            for p in cpu_processes:
                p.start()
            for p in cpu_processes:
                p.join()

        elif choice == '3':
            print("Starting GPU stress test...")
            gpu_process = multiprocessing.Process(target=stress_gpu)
            gpu_process.start()
            gpu_process.join()

        elif choice == '4':
            benchmark_cpu()

        elif choice == '5':
            print("Starting CPU and GPU stress tests simultaneously...")
            cpu_count = multiprocessing.cpu_count()
            cpu_processes = [multiprocessing.Process(target=stress_cpu) for _ in range(cpu_count)]
            gpu_process = multiprocessing.Process(target=stress_gpu)

            # Start CPU stress processes
            for p in cpu_processes:
                p.start()

            # Start GPU stress process
            gpu_process.start()

            # Wait for CPU stress processes to finish (which won't happen as the loops are infinite)
            for p in cpu_processes:
                p.join()

            # Wait for GPU stress process to finish (which won't happen as the loop is infinite)
            gpu_process.join()

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
