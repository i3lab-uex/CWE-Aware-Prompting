import re

# Compile the regular expression once for efficiency.
# The pattern matches a URL that starts with http:// or https://,
# followed by at least one non-space character.
_URL_RE = re.compile(
    r"""
    ^                           # start of string
    (https?)://                 # scheme http or https followed by ://
    [^\s/$.?#].[^\s]*           # at least one non-space character
    $                           # end of string
    """,
    re.IGNORECASE | re.VERBOSE,
)

def verify_link(link: str) -> bool:
    """
    Return True if the given string is a syntactically valid HTTP or HTTPS URL,
    otherwise return False.

    Parameters
    ----------
    link : str
        The string to evaluate as a potential HTTP/HTTPS URL.

    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.

    Notes
    -----
    The function performs a simple structural check; it does not attempt to resolve
    the URL or verify that the host exists.  No exceptions are raised for invalid
    input; an empty string or non-string value will simply return False.
    """
    if not isinstance(link, str):
        return False
    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(link))