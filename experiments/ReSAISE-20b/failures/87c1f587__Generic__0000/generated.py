import re

def find_html_tags(html_content: str) -> list[str]:
    """
    Return a list of all substrings in `html_content` that match HTML tags.

    A tag is defined as a string starting with '<', ending with '>', and
    containing any characters except the closing angle bracket. The function
    does not raise exceptions for malformed input; it simply returns an empty
    list if no tags are found or the input is not a string.

    Parameters:
        html_content (str): The HTML content to search.

    Returns:
        list[str]: A list of matched tag strings, preserving their order
                   in the original input.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non-string inputs
        return []

    # Use a non-greedy pattern to match tags.
    tag_pattern = re.compile(r"<[^>]*>", flags=re.MULTILINE)
    return tag_pattern.findall(html_content)