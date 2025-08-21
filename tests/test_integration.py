#!/usr/bin/env python3
"""
Integration test for the PowerPoint generation in the main app
"""

import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from components.document_generator import generate_document

def test_powerpoint_integration():
    """Test PowerPoint generation through the main document generator"""
    print("🧪 Testing PowerPoint generation integration...")
    
    # Mock LLM response function
    def mock_llm_response(prompt, config):
        return """
        SLIDE 1: Introduction to Photosynthesis
        - What is photosynthesis?
        - Why is it important for life?
        - Plants as food producers
        NOTES: Start with showing a green leaf and ask students what makes it green
        IMAGE: Green leaf with sunlight shining on it
        
        SLIDE 2: The Photosynthesis Equation
        - Carbon dioxide + Water + Light → Glucose + Oxygen
        - 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂
        - Chlorophyll captures light energy
        NOTES: Write the equation on the board step by step
        
        SLIDE 3: Where Does Photosynthesis Happen?
        - In the leaves of plants
        - Inside tiny structures called chloroplasts
        - Chloroplasts contain chlorophyll
        NOTES: Show microscopic images if available
        
        SLIDE 4: What Plants Need for Photosynthesis
        - Sunlight (energy source)
        - Carbon dioxide (from air)
        - Water (from roots)
        NOTES: Discuss how plants get each of these requirements
        
        SLIDE 5: What Plants Produce
        - Glucose (food for the plant)
        - Oxygen (released into air)
        - We breathe the oxygen plants make!
        NOTES: Emphasize the connection to human life
        """
    
    # Mock the LLM response temporarily
    try:
        from llm_handlers import api_handler
        original_get_llm_response = api_handler.get_llm_response
        api_handler.get_llm_response = mock_llm_response
        
        # Test parameters matching what the app would send
        params = {
            "doc_type": "PowerPoint Presentation",
            "subject": "Science",
            "grade_level": "Elementary (K-5)",
            "topic": "Introduction to Photosynthesis - how plants make their own food and produce oxygen",
            "llm_config": {
                "provider": "mock",
                "model": "test-model",
                "temperature": 0.7
            },
            "num_slides": 5,
            "include_images": True,
            "presentation_style": "Educational"
        }
        
        # Generate document
        result = generate_document(params)
        
        # Restore original function
        api_handler.get_llm_response = original_get_llm_response
        
        if result["success"]:
            print("✅ Integration test successful!")
            print(f"✅ Content generated: {len(result['content'])} characters")
            print(f"✅ PowerPoint file created: {len(result['pptx_file'])} bytes")
            
            # Save the result
            with open("integration_test_presentation.pptx", "wb") as f:
                f.write(result['pptx_file'])
            print("✅ Integration test PowerPoint saved as 'integration_test_presentation.pptx'")
            
            # Print a preview of the content
            print("\n📄 Content Preview:")
            print("=" * 50)
            preview = result['content'][:500] + "..." if len(result['content']) > 500 else result['content']
            print(preview)
            print("=" * 50)
            
            return True
        else:
            print(f"❌ Integration test failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting PowerPoint Integration Test\n")
    
    success = test_powerpoint_integration()
    
    if success:
        print("\n🎉 Integration test passed! The PowerPoint generation is working correctly with the main app.")
        print("\n💡 You can now use the PowerPoint generation feature in Streamlit:")
        print("   1. Run the app: streamlit run src/app.py")
        print("   2. Select 'PowerPoint Presentation' as document type")
        print("   3. Fill in your subject, grade level, and topic")
        print("   4. Configure your preferred AI model")
        print("   5. Click 'Generate Document'")
    else:
        print("\n⚠️  Integration test failed. Please check the errors above.")
