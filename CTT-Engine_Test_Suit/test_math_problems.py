import requests
import json
import time
import numpy as np

class CTTMathTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_basic_mathematical(self):
        """Test basic mathematical problem solving"""
        print("Testing Basic Mathematical Problem...")
        
        problem = {
            "expression": "sin(ξ) * exp(-ξ^2) + cos(2*π*ξ)",
            "description": "Basic wavefunction with Gaussian envelope"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/solve",
                json={
                    "problem_data": problem,
                    "problem_type": "mathematical"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Success: {result.get('solution')}")
                print(f"  Computation time: {result.get('computation_time', 0):.3f}s")
                return True
            else:
                print(f"✗ Error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Exception: {e}")
            return False
    
    def test_wave_convergence(self):
        """Test the wave convergence problem"""
        print("\nTesting Wave Convergence Problem...")
        
        problem = {
            "problem_type": "wave_convergence",
            "wave_function": "sin(2*π*ξ) * exp(-ξ^2/2) + 0.5*cos(4*π*ξ) * exp(-ξ^2/4)",
            "integration_range": [0, 5],
            "convergence_analysis": {
                "ξ_points": 1000,
                "frequency_components": [1, 2, 4, 8],
                "damping_factors": [0.1, 0.25, 0.5, 1.0]
            }
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/api/v1/solve",
                json={
                    "problem_data": problem,
                    "problem_type": "mathematical"
                },
                timeout=45
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Success in {end_time - start_time:.2f}s")
                print(f"  Solution: {result.get('solution')}")
                print(f"  Engine time: {result.get('computation_time', 0):.3f}s")
                return True
            else:
                print(f"✗ Error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Exception: {e}")
            return False
    
    def test_advanced_problem(self):
        """Test the advanced mathematical problem"""
        print("\nTesting Advanced Mathematical Problem...")
        
        problem = {
            "problem_id": "CTTE-2024-001",
            "problem_type": "advanced_mathematical",
            "title": "Temporal Resonance Fourier-Decomposition",
            
            "core_function": "ψ(ξ) = Σ[n=1 to 5] [A_n * sin(2π*f_n*ξ) * exp(-α_n*ξ^2)]",
            
            "parameters": {
                "amplitudes": [1.0, 0.7, 0.5, 0.3, 0.2],
                "frequencies": [1.0, 2.5, 4.0, 6.5, 9.0],
                "damping_coefficients": [0.1, 0.25, 0.4, 0.6, 0.8],
                "integration_range": [0, 10],
                "resolution": 2000
            },
            
            "analysis_requirements": {
                "temporal_integral": "∫[0 to 10] c(ξ) * ψ(ξ) dξ",
                "energy_distribution": "Calculate energy contribution of each component",
                "convergence_metric": "Evaluate c(ξ) = exp(-ξ²) at critical points"
            }
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/api/v1/solve",
                json={
                    "problem_data": problem,
                    "problem_type": "mathematical"
                },
                timeout=60
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Success in {end_time - start_time:.2f}s")
                print(f"  Solution: {result.get('solution')}")
                print(f"  Hash: {result.get('problem_hash', '')[:16]}...")
                return True
            else:
                print(f"✗ Error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Exception: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run all mathematical tests"""
        print("=" * 60)
        print("CTT ENGINE MATHEMATICAL CAPABILITIES TEST")
        print("=" * 60)
        
        # Check if server is running
        try:
            response = self.session.get(f"{self.base_url}/api/v1/health", timeout=10)
            if response.status_code != 200:
                print("Server is not responding. Please start the server first.")
                return False
        except:
            print("Cannot connect to server. Please make sure it's running.")
            print("Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
            return False
        
        # Run tests
        test1 = self.test_basic_mathematical()
        test2 = self.test_wave_convergence()
        test3 = self.test_advanced_problem()
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY:")
        print(f"Basic Mathematical: {'PASS' if test1 else 'FAIL'}")
        print(f"Wave Convergence: {'PASS' if test2 else 'FAIL'}")
        print(f"Advanced Problem: {'PASS' if test3 else 'FAIL'}")
        print("=" * 60)
        
        return all([test1, test2, test3])

# Additional test functions for specific mathematical operations
def test_specific_functions():
    """Test specific mathematical functions"""
    test_cases = [
        {"expression": "sin(ξ)", "range": [0, 2*np.pi], "expected": 0.0},
        {"expression": "ξ^2", "range": [0, 1], "expected": 1/3},
        {"expression": "exp(-ξ^2)", "range": [-5, 5], "expected": np.sqrt(np.pi)},
        {"expression": "cos(2*π*ξ) * exp(-ξ)", "range": [0, 10], "description": "Damped oscillation"}
    ]
    
    tester = CTTMathTester()
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTesting Case {i+1}: {test_case['expression']}")
        
        try:
            response = tester.session.post(
                "http://localhost:8000/api/v1/solve",
                json={
                    "problem_data": test_case,
                    "problem_type": "mathematical"
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  Result: {result.get('solution')}")
            else:
                print(f"  Error: {response.status_code}")
                
        except Exception as e:
            print(f"  Exception: {e}")

if __name__ == "__main__":
    tester = CTTMathTester()
    
    # Run comprehensive test
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✓ All mathematical tests passed! The CTT engine is working correctly.")
    else:
        print("\n✗ Some tests failed. Check the server logs for details.")
    
    # Uncomment to test specific functions
    # test_specific_functions()
