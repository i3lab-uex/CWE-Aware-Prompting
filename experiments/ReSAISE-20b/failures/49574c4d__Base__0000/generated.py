import re

def extract_html_elements(document: str) -> list[str]:
    """
    Extracts all HTML tags from the input document.

    The regex pattern used is intentionally simple and non-greedy:
        <[^>]+?>

    This pattern matches an opening '<', followed by one or more characters that are not
    '>' (the closing bracket), and then the closing '>'.  The non-greedy quantifier
    (`+?`) ensures that each match stops at the nearest '>' character, preventing
    catastrophic backtracking even for large inputs.

    Parameters:
        document (str): The HTML content to search.

    Returns:
        list[str]: A list of all matched tags.
    """
    # Compile the regex once for efficiency
    tag_pattern = re.compile(r"<[^>]+?>")
    # Find all non-overlapping matches
    return tag_pattern.findall(document)