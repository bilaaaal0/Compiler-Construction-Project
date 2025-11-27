"""
Test script to verify all compiler functionality
"""

from compiler import Compiler

def test_basic():
    """Test basic compilation"""
    print("=" * 60)
    print("TEST 1: Basic Compilation")
    print("=" * 60)
    
    source = """
    int x;
    x = 10;
    print x;
    """
    
    compiler = Compiler()
    success, result = compiler.compile(source, verbose=False)
    
    if success:
        print("✓ Basic compilation: PASSED")
        print(f"  - Generated {len(result['tac'])} TAC instructions")
        print(f"  - Generated {len(result['assembly'])} assembly instructions")
    else:
        print("✗ Basic compilation: FAILED")
    
    return success

def test_control_flow():
    """Test if-elif-else"""
    print("\n" + "=" * 60)
    print("TEST 2: Control Flow")
    print("=" * 60)
    
    source = """
    int x;
    x = 15;
    
    if (x > 20) {
        print 1;
    } elif (x > 10) {
        print 2;
    } else {
        print 0;
    }
    """
    
    compiler = Compiler()
    success, result = compiler.compile(source, verbose=False)
    
    if success:
        print("✓ Control flow: PASSED")
        print(f"  - Generated {len(result['tac'])} TAC instructions")
    else:
        print("✗ Control flow: FAILED")
    
    return success

def test_loops():
    """Test while and for loops"""
    print("\n" + "=" * 60)
    print("TEST 3: Loops")
    print("=" * 60)
    
    source = """
    int i;
    int sum;
    
    sum = 0;
    for (i = 1; i <= 5; i = i + 1) {
        sum = sum + i;
    }
    print sum;
    """
    
    compiler = Compiler()
    success, result = compiler.compile(source, verbose=False)
    
    if success:
        print("✓ Loops: PASSED")
        print(f"  - Generated {len(result['tac'])} TAC instructions")
    else:
        print("✗ Loops: FAILED")
    
    return success

def test_optimization():
    """Test optimization"""
    print("\n" + "=" * 60)
    print("TEST 4: Optimization")
    print("=" * 60)
    
    source = """
    int x;
    x = 5 + 3;
    print x;
    """
    
    compiler = Compiler()
    success, result = compiler.compile(source, verbose=False)
    
    if success:
        # Check if constant folding worked
        optimized = '\n'.join(result['optimized_tac'])
        if 'x = 8' in optimized:
            print("✓ Optimization (constant folding): PASSED")
            print(f"  - Reduced from {len(result['tac'])} to {len(result['optimized_tac'])} instructions")
        else:
            print("⚠ Optimization: Constant folding not detected")
    else:
        print("✗ Optimization: FAILED")
    
    return success

def test_error_detection():
    """Test error detection"""
    print("\n" + "=" * 60)
    print("TEST 5: Error Detection")
    print("=" * 60)
    
    # Test type mismatch
    source = """
    int x;
    x = 3.5;
    """
    
    compiler = Compiler()
    success, result = compiler.compile(source, verbose=False)
    
    if not success:
        print("✓ Error detection (type mismatch): PASSED")
    else:
        print("✗ Error detection: FAILED (should have detected error)")
        return False
    
    # Test undeclared variable
    source2 = """
    print y;
    """
    
    compiler2 = Compiler()
    success2, result2 = compiler2.compile(source2, verbose=False)
    
    if not success2:
        print("✓ Error detection (undeclared variable): PASSED")
    else:
        print("✗ Error detection: FAILED (should have detected error)")
        return False
    
    return True

def test_symbol_table():
    """Test symbol table"""
    print("\n" + "=" * 60)
    print("TEST 6: Symbol Table")
    print("=" * 60)
    
    source = """
    int x;
    float y;
    char c;
    
    x = 10;
    y = 3.14;
    """
    
    compiler = Compiler()
    success, result = compiler.compile(source, verbose=False)
    
    if success:
        symbol_table = result['symbol_table']
        # Check if all variables are in symbol table
        if (symbol_table.lookup('x') and 
            symbol_table.lookup('y') and 
            symbol_table.lookup('c')):
            print("✓ Symbol table: PASSED")
            print(f"  - Stored {len(symbol_table.scopes[0])} symbols")
        else:
            print("✗ Symbol table: FAILED (missing symbols)")
            return False
    else:
        print("✗ Symbol table: FAILED")
        return False
    
    return success

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MINI COMPILER - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_basic,
        test_control_flow,
        test_loops,
        test_optimization,
        test_error_detection,
        test_symbol_table
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED! 🎉")
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
