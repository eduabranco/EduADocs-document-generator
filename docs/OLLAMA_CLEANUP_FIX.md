# Ollama Thinking Models Cleanup Fix

## Problem
Ollama's thinking models (like deepseek-r1, qwen2.5-coder:32b-instruct, and other reasoning models) include their internal reasoning process wrapped in `<think>` and `</think>` tags in their responses. This thinking content was being included in the generated Word documents (.docx files), making them contain unwanted internal reasoning text along with the actual exercise content.

## Solution
Added a cleanup function `_clean_thinking_tags()` to the `api_handler.py` that:

1. **Removes thinking tags and content**: Strips out `<think>...</think>` blocks and their entire contents
2. **Case-insensitive matching**: Handles `<think>`, `<THINK>`, `<Think>`, etc.
3. **Multiple blocks**: Removes multiple thinking blocks from the same response
4. **Self-closing tags**: Also handles `<think/>` format if encountered
5. **Whitespace cleanup**: Cleans up extra whitespace left behind after tag removal

## Implementation Details

### Modified Files
- `src/llm_handlers/api_handler.py`: Added `_clean_thinking_tags()` function and integrated it into `_get_ollama_response()`

### Function Signature
```python
def _clean_thinking_tags(text):
    """Remove <think> and </think> tags and content between them from text"""
```

### How it Works
1. Uses regex pattern `<think>.*?</think>` with IGNORECASE and DOTALL flags
2. Removes all matching thinking blocks from the response
3. Cleans up resulting whitespace and formatting
4. Returns clean text ready for document generation

### Integration Point
The cleanup is applied in `_get_ollama_response()` before returning the response:

```python
result = response.json()
raw_response = result.get("response", "No response generated")

# Clean thinking tags from Ollama response
cleaned_response = _clean_thinking_tags(raw_response)

return cleaned_response
```

## Benefits
- **Automatic**: Works for all document types (exercises, summaries, PowerPoint)
- **Transparent**: No changes needed to generators or UI components
- **Safe**: Only removes thinking content, preserves all actual educational content
- **Robust**: Handles various tag formats and multiple thinking blocks

## Testing
Created comprehensive tests in `test_additional_tags.py` that verify:
- Basic thinking tag removal
- Multiple thinking blocks in one response
- Case-insensitive tag matching
- Content structure preservation
- Edge cases (empty/None input)

## Usage
The fix is automatic - no configuration or user action required. When using Ollama thinking models:

1. Model generates response with `<think>` content
2. API handler automatically cleans the response
3. Clean content goes to document generators
4. Final .docx files contain only the educational content

## Compatibility
- Works with all Ollama models (thinking and non-thinking)
- Non-thinking models are unaffected (no `<think>` tags to remove)
- Other LLM providers (OpenAI, Hugging Face) are unaffected
- All existing functionality preserved
