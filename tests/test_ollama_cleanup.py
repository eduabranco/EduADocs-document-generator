#!/usr/bin/env python3
"""
Test script to verify that Ollama thinking tags are properly cleaned from responses.
"""

import sys
import os

# Add src directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from llm_handlers.api_handler import _clean_thinking_tags

def test_clean_thinking_tags():
    """Test the _clean_thinking_tags function with various inputs"""
    
    # Test case 1: Simple thinking tags
    text1 = """<think>
    Let me think about this problem step by step.
    First, I need to understand what's being asked.
    </think>
    
    Here is the exercise list for your students:
    
    1. What is the capital of France?
    2. Solve for x: 2x + 5 = 15"""
    
    expected1 = """Here is the exercise list for your students:
    
    1. What is the capital of France?
    2. Solve for x: 2x + 5 = 15"""
    
    result1 = _clean_thinking_tags(text1)
    print("Test 1 - Simple thinking tags:")
    print(f"Input: {repr(text1)}")
    print(f"Expected: {repr(expected1)}")
    print(f"Result: {repr(result1)}")
    print(f"Passed: {result1.strip() == expected1.strip()}")
    print()
    
    # Test case 2: Multiple thinking blocks
    text2 = """<think>Planning the exercise structure</think>
    
    Exercise 1: Multiple Choice
    
    <think>Now I need to create good distractors for the multiple choice</think>
    
    What is 2 + 2?
    A) 3
    B) 4
    C) 5
    D) 6
    
    <think>Let me add one more question</think>
    
    Exercise 2: True/False"""
    
    expected2 = """Exercise 1: Multiple Choice

What is 2 + 2?
    A) 3
    B) 4
    C) 5
    D) 6

Exercise 2: True/False"""
    
    result2 = _clean_thinking_tags(text2)
    print("Test 2 - Multiple thinking blocks:")
    print(f"Input: {repr(text2)}")
    print(f"Expected: {repr(expected2)}")
    print(f"Result: {repr(result2)}")
    print(f"Passed: {result2.strip() == expected2.strip()}")
    print()
    
    # Test case 3: Case insensitive
    text3 = """<THINK>
    This is uppercase thinking
    </THINK>
    
    Regular content here.
    
    <Think>Mixed case thinking</Think>
    
    More content."""
    
    expected3 = """Regular content here.

More content."""
    
    result3 = _clean_thinking_tags(text3)
    print("Test 3 - Case insensitive:")
    print(f"Input: {repr(text3)}")
    print(f"Expected: {repr(expected3)}")
    print(f"Result: {repr(result3)}")
    print(f"Passed: {result3.strip() == expected3.strip()}")
    print()
    
    # Test case 4: No thinking tags (should remain unchanged)
    text4 = """This is a normal response without any thinking tags.
    
    1. Question one
    2. Question two
    3. Question three"""
    
    result4 = _clean_thinking_tags(text4)
    print("Test 4 - No thinking tags:")
    print(f"Input: {repr(text4)}")
    print(f"Result: {repr(result4)}")
    print(f"Passed: {result4 == text4}")
    print()
    
    # Test case 5: Empty or None input
    result5 = _clean_thinking_tags("")
    result6 = _clean_thinking_tags(None)
    print("Test 5 - Empty/None input:")
    print(f"Empty string result: {repr(result5)}")
    print(f"None result: {repr(result6)}")
    print(f"Passed: {result5 == '' and result6 is None}")
    print()

if __name__ == "__main__":
    test_clean_thinking_tags()
    print("All tests completed!")
