#!/usr/bin/env python3
"""
Test script for PowerPoint generation functionality
"""

import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from generators.powerpoint_generator import generate_powerpoint, _parse_powerpoint_content, _create_powerpoint_pptx

def test_powerpoint_parsing():
    """Test the content parsing function"""
    print("🧪 Testing PowerPoint content parsing...")
    
    sample_content = """
    SLIDE 1: Introduction to Mathematics
    - Welcome to our math class
    - Today we'll learn about fractions
    - Get ready for an exciting journey
    NOTES: Start with enthusiasm and engage students
    IMAGE: Colorful math symbols
    
    SLIDE 2: What are Fractions?
    - A fraction represents parts of a whole
    - The top number is the numerator
    - The bottom number is the denominator
    NOTES: Use visual examples like pizza slices
    
    SLIDE 3: Types of Fractions
    - Proper fractions (numerator < denominator)
    - Improper fractions (numerator ≥ denominator)
    - Mixed numbers (whole number + fraction)
    NOTES: Show examples of each type
    """
    
    slides = _parse_powerpoint_content(sample_content)
    
    print(f"✅ Parsed {len(slides)} slides")
    for i, slide in enumerate(slides, 1):
        print(f"  Slide {i}: {slide['title']}")
        print(f"    Bullets: {len(slide['bullets'])}")
        print(f"    Notes: {'Yes' if slide['notes'] else 'No'}")
        print(f"    Image: {'Yes' if slide['image'] else 'No'}")
    
    return len(slides) == 3

def test_powerpoint_creation():
    """Test PowerPoint file creation"""
    print("\n🧪 Testing PowerPoint file creation...")
    
    # Mock parameters
    params = {
        'subject': 'Mathematics',
        'grade_level': 'Elementary (K-5)',
        'doc_type': 'PowerPoint Presentation',
        'num_slides': 3,
        'include_images': True,
        'presentation_style': 'Educational'
    }
    
    # Sample content that should parse correctly
    sample_content = """
    SLIDE 1: Introduction to Fractions
    - What is a fraction?
    - Why do we need fractions?
    - Real-world examples
    NOTES: Start with familiar examples like pizza and cake
    IMAGE: Pizza divided into slices
    
    SLIDE 2: Parts of a Fraction
    - Numerator (top number)
    - Denominator (bottom number)
    - The fraction bar
    NOTES: Use visual diagrams to explain each part
    
    SLIDE 3: Practice Time
    - Let's identify fractions
    - Try some examples
    - Questions and discussion
    NOTES: Interactive session with student participation
    """
    
    try:
        pptx_data = _create_powerpoint_pptx(sample_content, params)
        
        if pptx_data and len(pptx_data) > 0:
            print(f"✅ Successfully created PowerPoint file ({len(pptx_data)} bytes)")
            
            # Save test file
            with open("test_presentation.pptx", "wb") as f:
                f.write(pptx_data)
            print("✅ Test PowerPoint saved as 'test_presentation.pptx'")
            return True
        else:
            print("❌ PowerPoint creation returned empty data")
            return False
            
    except Exception as e:
        print(f"❌ PowerPoint creation failed: {e}")
        return False

def test_full_generation_mock():
    """Test full generation with mock LLM response"""
    print("\n🧪 Testing full PowerPoint generation (mocked)...")
    
    # We'll mock the LLM response by temporarily replacing the get_llm_response function
    def mock_llm_response(prompt, config):
        return """
        SLIDE 1: Introduction to Basic Algebra
        - Welcome to algebra class
        - What is algebra?
        - Variables and constants
        NOTES: Start with simple examples students can relate to
        IMAGE: Math equations on a chalkboard
        
        SLIDE 2: Understanding Variables
        - A variable is an unknown value
        - Usually represented by letters like x, y, z
        - Can represent different numbers
        NOTES: Use examples like "x apples" or "y students"
        
        SLIDE 3: Basic Operations
        - Addition and subtraction
        - Multiplication and division
        - Order of operations
        NOTES: Remember PEMDAS or BODMAS
        """
    
    # Mock parameters
    params = {
        'subject': 'Mathematics',
        'grade_level': 'Middle School (6-8)',
        'topic': 'Introduction to Basic Algebra',
        'doc_type': 'PowerPoint Presentation',
        'num_slides': 3,
        'include_images': True,
        'presentation_style': 'Educational',
        'llm_config': {
            'provider': 'mock',
            'model': 'test-model'
        }
    }
    
    try:
        # Temporarily replace the import
        import generators.powerpoint_generator as ppg
        original_get_llm_response = ppg.get_llm_response
        ppg.get_llm_response = mock_llm_response
        
        result = generate_powerpoint(params)
        
        # Restore original function
        ppg.get_llm_response = original_get_llm_response
        
        if result['success']:
            print("✅ Full generation test successful")
            print(f"✅ Generated content length: {len(result['content'])} characters")
            print(f"✅ PowerPoint file size: {len(result['pptx_file'])} bytes")
            
            # Save the test file
            with open("test_full_presentation.pptx", "wb") as f:
                f.write(result['pptx_file'])
            print("✅ Full test PowerPoint saved as 'test_full_presentation.pptx'")
            return True
        else:
            print(f"❌ Full generation failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Full generation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting PowerPoint Generator Tests\n")
    
    test_results = []
    
    # Run tests
    test_results.append(test_powerpoint_parsing())
    test_results.append(test_powerpoint_creation())
    test_results.append(test_full_generation_mock())
    
    # Summary
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! PowerPoint generation should work correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("\n💡 If all tests passed, you can now use the PowerPoint generation feature in the main app.")
