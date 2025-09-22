import requests
import time

def test_cache_performance():
    """Test cache performance by solving the same problem multiple times"""
    print("Testing Cache Performance...")
    
    problem = {
        "expression": "sin(ξ) * exp(-ξ^2)",
        "description": "Test function for cache performance"
    }
    
    times = []
    
    for i in range(5):
        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/api/v1/solve",
            json={
                "problem_data": problem,
                "problem_type": "mathematical"
            },
            timeout=20
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            times.append(end_time - start_time)
            print(f"Run {i+1}: {result.get('computation_time', 0):.4f}s (total: {end_time - start_time:.4f}s)")
        else:
            print(f"Error in run {i+1}")
            return False
    
    # Check if subsequent runs are faster (indicating cache)
    if len(times) >= 2 and times[1] < times[0] * 0.5:
        print("✓ Cache is working effectively!")
    else:
        print("⚠ Cache may not be working optimally")
    
    return True

if __name__ == "__main__":
    test_cache_performance()
