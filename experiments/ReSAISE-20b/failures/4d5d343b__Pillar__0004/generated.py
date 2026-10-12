import re

def grab_html_tags(html_code: str) -> list[str]:
    """
    Scan the given HTML string for tags and return a list of all matched tags.
    
    The function uses a simple regular expression that matches opening and closing
    tags, including those with attributes. It is deliberately conservative to avoid
    matching malformed constructs or script code that might contain angle brackets.
    
    Parameters:
        html_code (str): The HTML source to parse.
        
    Returns:
        list[str]: A list of strings, each containing a full tag as it appears in
                   the input. The order matches the order of appearance.
    """
    # Regular expression to match:
    #   <tag ...>
    #   </tag>
    #   <tag/>
    #
    # It does not attempt to validate nested structure or self‑closing syntax.
    tag_pattern = re.compile(r'<\s*/?\s*[a-zA-Z][^\s/>]*[^>]*?>', re.IGNORECASE)

    try:
        # Find all non‑overlapping matches
        tags = tag_pattern.findall(html_code)
    except Exception:
        # In case the input is not a string or regex fails, return empty list
        tags = []

    # Ensure the result is always a list (not None)
    return list(tags)

# Example usage
if __name__ == "__main__":
    sample = "<html><body><h1>Hello</h1><!-- comment --></body></html>"
    print(grab_html_tags(sample))