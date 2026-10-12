import re

def grab_html_tags(html_code: str) -> list[str]:
    """
    Scan the supplied HTML string and return a list of all tags found.

    The function uses a non‑greedy regular expression to match:
        * Opening tags: <tag ...>
        * Self‑closing tags: <tag .../>
        * Closing tags: </tag>

    It is tolerant of malformed input and will never raise an exception.
    """
    if not isinstance(html_code, str):
        # If the input is not a string we return an empty list rather than raising
        return []

    # Regular expression to capture tag names, ignoring attributes.
    # It matches:
    #   <tag ...>          -> group 1: tag name
    #   </tag>             -> group 1: tag name
    #   <tag .../>         -> group 1: tag name
    tag_pattern = re.compile(r'<\s*/?\s*([a-zA-Z0-9]+)[^>]*?>', re.IGNORECASE)

    try:
        tags = tag_pattern.findall(html_code)
        # Normalize to lower case for consistency (optional)
        return [tag.lower() for tag in tags]
    except Exception:
        # In the unlikely event of a regex error or other issue, return empty list
        return []