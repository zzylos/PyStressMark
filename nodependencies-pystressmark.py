import time
import multiprocessing
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
    """Continuously perform CPU-intensive operations."""
    num = 10**6
    while True:
        num += 1
        is_prime(num)

def benchmark_cpu():
    """Benchmark CPU by performing CPU-intensive operations for a set duration."""
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
        print("1. CPU Stress Test")
        print("2. CPU Benchmark")
        print("3. Exit")

        choice = input("Enter the number of the option you want to run: ").strip()

        if choice == '1':
            cpu_count = multiprocessing.cpu_count()
            print(f"Starting CPU stress test with {cpu_count} CPU cores.")
            cpu_processes = [multiprocessing.Process(target=stress_cpu) for _ in range(cpu_count)]
            for p in cpu_processes:
                p.start()
            for p in cpu_processes:
                p.join()

        elif choice == '2':
            benchmark_cpu()

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
