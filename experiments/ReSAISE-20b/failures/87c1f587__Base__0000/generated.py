import re

# Pre‑compile a simple, efficient pattern that matches HTML tags.
# The pattern:
#   <            - literal '<'
#   [^>]+?       - one or more characters that are not '>', non‑greedy
#   >            - literal '>'
TAG_PATTERN = re.compile(r'<[^>]+?>', flags=re.IGNORECASE)

def find_html_tags(html_content: str) -> list[str]:
    """
    Return a list of all substrings in *html_content* that look like HTML tags.

    The function uses a simple regular expression to find tag-like
    constructs.  It does not attempt to validate the tags or parse
    nested structures; it merely returns every match of the pattern.

    Parameters:
        html_content (str): The input string containing HTML content.

    Returns:
        list[str]: A list of matched tag strings.  If no tags are found,
                   an empty list is returned.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non‑string inputs by returning an empty list.
        return []

    # Find all matches of the pattern in the input string.
    tags = TAG_PATTERN.findall(html_content)
    return tags