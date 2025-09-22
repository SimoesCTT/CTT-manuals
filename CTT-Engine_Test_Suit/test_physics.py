import requests
import json

def test_physics_problems():
    """Test physics-related problems"""
    print("Testing Physics Problems...")
    
    # Mass-temporal relation problem
    physics_problem = {
        "problem_type": "mass_temporal",
        "temporal_acceleration": 0.15,
        "description": "Calculate mass from temporal acceleration using m = (ħ/c²) * (∂²ξ/∂t²)"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/solve",
            json={
                "problem_data": physics_problem,
                "problem_type": "physics"
            },
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Physics Solution: {result.get('solution')}")
            return True
        else:
            print(f"Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Exception: {e}")
        return False

def test_resonance_frequency():
    """Test resonance frequency calculation"""
    print("\nTesting Resonance Frequency...")
    
    resonance_problem = {
        "problem_type": "resonance_calculation",
        "parameters": {
            "fine_structure_constant": 1/137.035999,
            "temporal_mass": 0.0,
            "energy_scale": 1.956e9
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/solve",
            json={
                "problem_data": resonance_problem,
                "problem_type": "physics"
            },
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Resonance Solution: {result.get('solution')}")
            return True
        else:
            print(f"Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    test_physics_problems()
    test_resonance_frequency()
