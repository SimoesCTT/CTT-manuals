#!/usr/bin/env python3
"""
Quick test of quantum-exclusive problem solving
"""

from quantum_exclusive_problem import QuantumExclusiveProblem

def quick_quantum_test():
    """Quick test of quantum capabilities"""
    print("Quick Quantum-Exclusive Test")
    print("=" * 40)
    
    solver = QuantumExclusiveProblem()
    
    # Test Shor's algorithm (the most famous quantum algorithm)
    result = solver.shors_algorithm_simulation(15)
    
    if result:
        print(f"✓ Quantum factorization successful!")
        print(f"  Result: {result.get('solution', 'No details')}")
        return True
    else:
        print("✗ Quantum test failed")
        return False

if __name__ == "__main__":
    quick_quantum_test()
