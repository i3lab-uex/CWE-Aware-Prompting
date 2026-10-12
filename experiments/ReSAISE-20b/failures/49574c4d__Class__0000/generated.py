import re

def extract_html_elements(document: str) -> list[str]:
    """
    Extracts all HTML tags from the given document string.

    Parameters
    ----------
    document : str
        The input HTML content to be analyzed.

    Returns
    -------
    list[str]
        A list of strings, each representing an HTML tag found in the input.
        The order of tags matches their appearance in the document.

    Notes
    -----
    - This function uses a non‑greedy, character class based regular expression that
      avoids catastrophic backtracking. The pattern matches any substring that starts
      with '<', contains zero or more characters other than '>', and ends with '>'.
    - No exceptions are raised; if the input is not a string, it will be coerced to
      a string using ``str(document)``. If the input is empty or contains no tags,
      an empty list is returned.
    """
    if not isinstance(document, str):
        document = str(document)

    # Pattern explanation:
    #   <         - literal opening angle bracket
    #   [^>]*     - any number of characters that are not '>'
    #   >         - literal closing angle bracket
    #
    # This pattern is efficient and does not exhibit exponential backtracking.
    tag_pattern = re.compile(r'<[^>]*>', re.DOTALL)

    return tag_pattern.findall(document)