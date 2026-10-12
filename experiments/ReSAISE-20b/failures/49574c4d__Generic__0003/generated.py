import re

def extract_html_elements(document: str) -> list[str]:
    """
    Return a list of all substrings in *document* that match HTML tags.
    
    Parameters
    ----------
    document : str
        The input string containing potential HTML content.

    Returns
    -------
    list[str]
        A list of matched tag strings.  The function never raises an exception.
    """
    # Regular expression that matches anything that starts with '<',
    # contains any characters except '>' (non-greedy), and ends with '>'.
    tag_pattern = re.compile(r'<[^>]+>', flags=re.DOTALL)

    try:
        return tag_pattern.findall(document)
    except Exception:
        # In case of any unforeseen error, return an empty list
        return []