import re

def grab_html_tags(html_code: str):
    """
    Scan the provided HTML string for tags using a regular expression
    and return a list of all detected tags.

    Parameters:
        html_code (str): The HTML string to parse.

    Returns:
        list[str]: A list containing all tag strings found in the input.
                   If no tags are present or an error occurs, returns an empty list.
    """
    # Regular expression to match HTML tags (e.g., <div>, </a>, <img src="..."/>)
    tag_pattern = re.compile(r'<[^>]+>', flags=re.IGNORECASE | re.DOTALL)

    try:
        # Find all non-overlapping matches of the pattern
        tags = tag_pattern.findall(html_code)
    except Exception:
        # In case of any unexpected error, return an empty list
        tags = []

    return tags