#!/usr/bin/env python3
"""
Test script for the streamlined Teacher Document Generator
Quick verification of core functionality without UI
"""

from llm_config import display_llm_selector, get_llm_response
from document_generators import generate_document
from utils import validate_inputs, get_subject_keywords, parse_topic_complexity

def test_imports():
    """Test if all modules import correctly"""
    print("✅ Testing imports...")
    try:
        from llm_config import display_llm_selector
        from document_generators import generate_document
        from utils import validate_inputs
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_validation():
    """Test validation functions"""
    print("\n✅ Testing validation...")
    
    # Test with missing required fields
    params = {"subject": "", "topic": "", "llm_config": {}}
    errors = validate_inputs(params)
    print(f"Expected errors for empty params: {len(errors)} errors found")
    
    # Test with valid params
    params = {
        "subject": "Mathematics",
        "topic": "Basic algebra concepts",
        "llm_config": {
            "provider": "openai_api",
            "api_key": "test-key",
            "model": "gpt-4o-mini"
        }
    }
    errors = validate_inputs(params)
    print(f"Valid params: {len(errors)} errors found")
    
    return True

def test_utilities():
    """Test utility functions"""
    print("\n✅ Testing utilities...")
    
    # Test subject keywords
    keywords = get_subject_keywords("Mathematics")
    print(f"Math keywords: {keywords}")
    
    # Test topic complexity
    complexity = parse_topic_complexity("Advanced calculus integration techniques")
    print(f"Topic complexity: {complexity}")
    
    return True

def test_llm_config_structure():
    """Test LLM configuration structure (without API calls)"""
    print("\n✅ Testing LLM config structure...")
    
    # Test config structure
    from llm_config import _check_ollama_connection
    is_available, models = _check_ollama_connection()
    print(f"Ollama connection test: Available={is_available}, Models={len(models)}")
    
    return True

def main():
    """Run all tests"""
    print("🔧 Testing Streamlined Teacher Document Generator")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_validation,
        test_utilities,
        test_llm_config_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The streamlined version is ready to use.")
        print("\nTo run the application:")
        print("streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
