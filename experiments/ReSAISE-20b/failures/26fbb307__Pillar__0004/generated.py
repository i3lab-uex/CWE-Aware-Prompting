import re
import html

def display_comment(comment: str) -> str:
    """
    Sanitize a user‑generated comment for safe rendering on a web page.
    
    The function performs the following steps:
    1. Removes any <script> tags (and their content) to prevent script injection.
    2. Escapes all remaining HTML special characters, ensuring that the comment
       cannot break out of the intended text context.
    
    Args:
        comment: The raw user‑generated string.
    
    Returns:
        A sanitized string safe for inclusion in HTML output.
    """
    # 1. Remove <script> tags and their content (case‑insensitive)
    # This pattern matches opening <script>, optional attributes, any content,
    # and the closing </script>. It is non‑greedy to avoid spanning multiple
    # script blocks.
    cleaned = re.sub(
        r'<script\b[^>]*?>.*?</script\s*>',
        '',
        comment,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # 2. Escape the remaining string to neutralize HTML entities.
    safe = html.escape(cleaned, quote=True)
    
    return safe