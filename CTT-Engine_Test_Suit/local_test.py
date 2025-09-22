import requests
import json
import time
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any

class CTTEngineLocalTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.results = {}
        
        # Test data for the temporal resonance decay problem
        self.temporal_decay_problem = {
            "system_id": "TDS-42",
            "resonance_readings": [
                [0.15, 0.22, 0.18, 0.31, 0.29, 0.24, 0.19, 0.26],
                [0.18, 0.25, 0.21, 0.28, 0.32, 0.27, 0.23, 0.30],
                [0.22, 0.29, 0.25, 0.34, 0.36, 0.31, 0.28, 0.33],
                [0.26, 0.33, 0.30, 0.37, 0.39, 0.35, 0.32, 0.37],
                [0.31, 0.38, 0.35, 0.41, 0.43, 0.39, 0.36, 0.41]
            ],
            "time_intervals": [0, 2.5, 5.0, 7.5, 10.0],
            "decay_equation": "∂²ξ/∂t² + 0.15 * sin(2π * 587000 * t) * ξ = 0.05 * exp(-0.1*t)",
            "critical_threshold": 0.75,
            "prediction_horizon": 15.0
        }
    
    def check_server_status(self) -> bool:
        """Check if the server is running"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Server is running: {data}")
                return True
            else:
                print(f"✗ Server returned status code: {response.status_code}")
                return False
        except requests.ConnectionError:
            print("✗ Cannot connect to server. Is it running?")
            print(f"  Try running: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
            return False
        except Exception as e:
            print(f"✗ Error checking server status: {e}")
            return False
    
    def test_temporal_decay_problem(self) -> bool:
        """Test the temporal decay problem"""
        print("\nTesting Temporal Decay Problem...")
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/api/v1/solve",
                json={
                    "problem_data": self.temporal_decay_problem,
                    "problem_type": "physics"
                },
                timeout=30
            )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Problem solved successfully in {data.get('computation_time', 0):.3f}s")
                print(f"  Solution: {data.get('solution', 'No solution')}")
                print(f"  Status: {data.get('status', 'unknown')}")
                
                # Save the detailed response
                self.results['temporal_decay'] = {
                    'status': 'success',
                    'response': data,
                    'computation_time': end_time - start_time,
                    'engine_time': data.get('computation_time', 0)
                }
                return True
            else:
                print(f"✗ Server returned status code: {response.status_code}")
                print(f"  Response: {response.text}")
                self.results['temporal_decay'] = {
                    'status': 'error',
                    'response': f"Status code: {response.status_code}",
                    'computation_time': end_time - start_time
                }
                return False
                
        except Exception as e:
            print(f"✗ Error solving problem: {e}")
            self.results['temporal_decay'] = {
                'status': 'exception',
                'response': str(e),
                'computation_time': 0
            }
            return False
    
    def visualize_resonance_patterns(self):
        """Visualize the resonance patterns from the test data"""
        print("\nVisualizing Resonance Patterns...")
        
        resonance_readings = self.temporal_decay_problem["resonance_readings"]
        time_intervals = self.temporal_decay_problem["time_intervals"]
        
        plt.figure(figsize=(10, 6))
        
        for i, readings in enumerate(resonance_readings):
            plt.plot(readings, 'o-', label=f"t={time_intervals[i]}", linewidth=2, markersize=6)
        
        plt.title("Temporal Resonance Patterns", fontsize=14, fontweight='bold')
        plt.xlabel("Resonance Channel", fontsize=12)
        plt.ylabel("Amplitude", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save the plot
        plt.savefig("resonance_patterns.png", dpi=150, bbox_inches='tight')
        print("✓ Resonance patterns visualization saved as 'resonance_patterns.png'")
        
        # Show the plot
        plt.show()
    
    def run_basic_tests(self):
        """Run basic tests to verify the server is working"""
        print("Running Basic CTT Engine Tests...")
        print("=" * 50)
        
        # First check if server is running
        if not self.check_server_status():
            print("\nPlease start your server first with:")
            print("uvicorn main:app --reload --host 0.0.0.0 --port 8000")
            return False
        
        # Test the temporal decay problem
        success = self.test_temporal_decay_problem()
        
        # Visualize the resonance patterns
        self.visualize_resonance_patterns()
        
        # Save results
        with open("local_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        print("✓ Test results saved to 'local_test_results.json'")
        
        return success

# Simple test without classes
def quick_test():
    """Quick test function for simple validation"""
    print("Quick CTT Engine Test")
    print("=" * 30)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✓ Server is healthy")
            data = response.json()
            print(f"  Status: {data.get('status')}")
            print(f"  Engine ready: {data.get('engine_ready')}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
        
        # Test equations endpoint
        response = requests.get("http://localhost:8000/api/v1/equations", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Loaded {len(data.get('equations', []))} CTT equations")
        else:
            print(f"✗ Equations endpoint failed: {response.status_code}")
        
        return True
        
    except requests.ConnectionError:
        print("✗ Cannot connect to server. Please start it with:")
        print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"✗ Error during quick test: {e}")
        return False

if __name__ == "__main__":
    # Run quick test first
    if quick_test():
        # If quick test passes, run comprehensive test
        tester = CTTEngineLocalTester()
        tester.run_basic_tests()
    else:
        print("\nPlease start your server first, then run this test again.")
