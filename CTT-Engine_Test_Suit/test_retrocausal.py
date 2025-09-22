#!/usr/bin/env python3
"""
Quick test of retrocausal computation
"""

from retrocausal_demo import RetrocausalDemo

def quick_test():
    """Quick test function"""
    print("Quick Retrocausal Test")
    print("=" * 30)
    
    demo = RetrocausalDemo()
    
    # Just test basic functionality
    sample_data = [0.1, 0.3, 0.5, 0.4, 0.6, 0.8, 0.7, 0.9, 1.1, 1.0]
    result = demo.retrocausal_prediction(sample_data, prediction_points=5)
    
    if result:
        print(f"Success! Solution: {result.get('solution', 'No solution details')}")
        return True
    else:
        print("Test failed")
        return False

if __name__ == "__main__":
    quick_test()
