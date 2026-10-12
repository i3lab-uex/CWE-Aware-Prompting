import re

def detect_html_tags(html_str: str) -> list[str]:
    """
    Detect all HTML tags in the given string using a regular expression.

    Parameters
    ----------
    html_str : str
        The input string containing HTML content.

    Returns
    -------
    list[str]
        A list of strings, each representing an HTML tag found in the input.
    """
    # The regex matches '<', followed by any characters except '>' (non-greedy),
    # and ends with '>'. It captures tags like <div>, </p>, or <img src="..."/>.
    tag_pattern = re.compile(r'<[^>]+>')
    
    # Find all non-overlapping matches of the pattern.
    tags = tag_pattern.findall(html_str)

    # Ensure we return a list even if no tags are found.
    return tags