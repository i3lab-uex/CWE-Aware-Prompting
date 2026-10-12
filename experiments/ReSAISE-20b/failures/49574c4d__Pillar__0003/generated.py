import re

def extract_html_elements(document: str) -> list[str]:
    """
    Extract all HTML tags from the provided document string.

    The function uses a simple regular expression that matches any
    substring starting with '<', followed by any characters except '>',
    and ending with '>'.  It returns a list of these substrings.
    No exceptions are raised; if the input is not a string, it will
    be coerced to one.

    Parameters:
        document (str): The input HTML content as a string.

    Returns:
        list[str]: A list containing all matched HTML tag strings.
    """
    if not isinstance(document, str):
        document = str(document)

    # Non-greedy match for tags; ignore self-closing and comment variations.
    tag_pattern = re.compile(r'<[^>]+?>')
    return tag_pattern.findall(document)