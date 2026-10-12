import re
from typing import List

# Compile the regex once at module load time to avoid repeated compilation overhead.
# The pattern captures any sequence that starts with '<', followed by an optional '/' (for closing tags),
# then a tag name consisting of letters, digits, hyphens or underscores, and ends with '>'.
# It also allows optional attributes and whitespace before the closing '>' character.
_TAG_PATTERN = re.compile(
    r'<\s*/?\s*([a-zA-Z0-9:_-]+)[^>]*?>',
    flags=re.IGNORECASE | re.DOTALL
)

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_content : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of strings, each representing a tag found in the input.
        Tags are returned exactly as they appear in the source (including
        angle brackets and any attributes). If no tags are found, an empty
        list is returned.

    Notes
    -----
    - The function is defensive: it catches any unexpected errors and returns an empty list.
      This prevents accidental crashes in callers that rely on the function's robustness.
    - The regular expression is intentionally permissive to capture a wide range of valid
      HTML tags while avoiding catastrophic backtracking. It does not attempt to parse
      malformed or nested tags; for complex parsing, a dedicated HTML parser should be used.
    """
    if not isinstance(html_content, str):
        # If the input is not a string, we cannot proceed safely.
        return []

    try:
        # Find all non-overlapping matches; each match corresponds to a tag.
        tags = [match.group(0) for match in _TAG_PATTERN.finditer(html_content)]
        return tags
    except Exception:
        # In the unlikely event of a regex failure or other unexpected error,
        # return an empty list to maintain the contract that no exception is raised.
        return []

# Example usage (for manual testing only; remove or comment out in production):
if __name__ == "__main__":
    sample = "<div class='test'><p>Hello <a href='#'>world</a></p><!-- comment --></div>"
    print(extract_html_tags(sample))