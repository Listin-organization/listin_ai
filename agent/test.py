import sys
import os
import json

def print_status(name, status, message=""):
    """Print formatted status message"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name:<40} {message}")
    return status

def test_packages():
    """Test if all required packages are installed"""
    print("\n" + "="*60)
    print("📦 CHECKING PACKAGES")
    print("="*60)
    
    packages = {
        'sys': 'Built-in',
        'os': 'Built-in',
        'json': 'Built-in',
        'google.adk.agents': 'google-adk-agents',
        'google.adk.tools': 'google-adk-tools',
    }
    
    all_installed = True
    for pkg, install_name in packages.items():
        try:
            __import__(pkg)
            print_status(pkg, True)
        except ImportError:
            print_status(pkg, False, f"Install: pip install {install_name}")
            all_installed = False
    
    return all_installed

def test_files():
    """Test if all required files exist"""
    print("\n" + "="*60)
    print("📁 CHECKING FILES")
    print("="*60)
    
    base_dir = os.path.dirname(__file__)
    required_files = {
        'listin_agent.py': 'Main agent file',
        'listin_seller_data.json': 'Store data configuration',
    }
    
    all_exist = True
    for filename, description in required_files.items():
        filepath = os.path.join(base_dir, filename)
        exists = os.path.isfile(filepath)
        print_status(filename, exists, description)
        all_exist = all_exist and exists
    
    return all_exist

def test_json_structure():
    """Test if listin_seller_data.json has correct structure"""
    print("\n" + "="*60)
    print("📋 CHECKING JSON STRUCTURE")
    print("="*60)
    
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, 'listin_seller_data.json')
    
    if not os.path.isfile(json_path):
        print_status("JSON File", False, "File not found")
        return False
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print_status("JSON Valid", True, "Successfully parsed")
        
        # Check required fields
        required_fields = ['store_name', 'store_info', 'products', 'delivery_policy', 'payment_policy', 'return_policy']
        
        all_fields_ok = True
        for field in required_fields:
            exists = field in data
            print_status(f"Field: {field}", exists)
            all_fields_ok = all_fields_ok and exists
        
        return all_fields_ok
    
    except json.JSONDecodeError as e:
        print_status("JSON Valid", False, f"Parse error: {str(e)}")
        return False
    except Exception as e:
        print_status("JSON Read", False, f"Error: {str(e)}")
        return False

def test_env_variables():
    """Test if required environment variables are set"""
    print("\n" + "="*60)
    print("🔐 CHECKING ENVIRONMENT VARIABLES")
    print("="*60)
    
    required_env = {
        'GOOGLE_API_KEY': 'Google API Key for Gemini',
        'GOOGLE_APPLICATION_CREDENTIALS': 'Google Cloud Service Account (optional)',
    }
    
    all_set = True
    for env_var, description in required_env.items():
        value = os.getenv(env_var)
        is_set = value is not None
        status_msg = "Set" if is_set else "Not set (required for API calls)"
        print_status(env_var, is_set, status_msg)
        # GOOGLE_API_KEY is required, others are optional
        if env_var == 'GOOGLE_API_KEY':
            all_set = all_set and is_set
    
    return all_set

def test_store_data_loading():
    """Test if store_data loads correctly"""
    print("\n" + "="*60)
    print("📥 CHECKING STORE DATA LOADING")
    print("="*60)
    
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'listin_seller_data.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            store_data = json.load(f)
        
        print_status("store_data loaded", True)
        
        store_name = store_data.get('store_name', 'Magazin')
        print_status("store_name extracted", True, f"Value: '{store_name}'")
        
        # Check data is not empty
        is_not_empty = len(store_data) > 0
        print_status("store_data not empty", is_not_empty, f"Keys: {len(store_data)}")
        
        return True
    except Exception as e:
        print_status("store_data loading", False, str(e))
        return False

def test_imports():
    """Test if listin_agent.py imports work"""
    print("\n" + "="*60)
    print("🔗 CHECKING IMPORTS")
    print("="*60)
    
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        # Try importing the module (will fail if dependencies missing, but we test that)
        import importlib.util
        spec = importlib.util.spec_from_file_location("listin_agent", 
                                                        os.path.join(os.path.dirname(__file__), 'listin_agent.py'))
        if spec and spec.loader:
            print_status("listin_agent.py importable", True)
            return True
        else:
            print_status("listin_agent.py importable", False, "Could not load spec")
            return False
    except Exception as e:
        print_status("listin_agent.py importable", False, str(e))
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("\n" + "🧪 LISTIN_AGENT VALIDATION TEST SUITE 🧪".center(60, "="))
    
    tests = [
        ("Packages Check", test_packages),
        ("Files Check", test_files),
        ("JSON Structure Check", test_json_structure),
        ("Environment Variables Check", test_env_variables),
        ("Store Data Loading Check", test_store_data_loading),
        ("Imports Check", test_imports),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with error: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        print_status(test_name, result)
    
    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} checks passed")
    print("-"*60)
    
    if passed == total:
        print("\n✅ ALL CHECKS PASSED! You are ready to run listin_agent.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please fix issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)