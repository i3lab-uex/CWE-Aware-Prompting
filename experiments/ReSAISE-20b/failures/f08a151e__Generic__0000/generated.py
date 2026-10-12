import re

def get_html_tags(html_input: str) -> list:
    """
    Extracts all HTML tag names from the provided string.

    Parameters
    ----------
    html_input : str
        A string containing HTML markup.

    Returns
    -------
    list[str]
        A list of tag names (without angle brackets or attributes) in the order
        they appear in ``html_input``.  The list is empty if no tags are found.
    """
    # Regex explanation:
    #   <\s*         : opening '<' followed by optional whitespace
    #   /?           : optional '/' for closing tags
    #   \s*          : optional whitespace after '/'
    #   ([a-zA-Z0-9]+): capture group for the tag name (alphanumeric)
    #   [^>]*?       : non-greedy match of any characters that are not '>'
    #   >            : closing '>' of the tag
    pattern = r'<\s*/?\s*([a-zA-Z0-9]+)[^>]*?>'
    # Use re.IGNORECASE to handle tags like <DIV> and <div>
    return re.findall(pattern, html_input, flags=re.IGNORECASE)