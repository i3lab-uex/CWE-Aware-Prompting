import re

# Compile the regular expression once for efficiency and security.
_URL_REGEX = re.compile(
    r'^https?://'                 # http:// or https://
    r'(?:[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?\.)+'  # domain (one or more labels)
    r'[A-Za-z]{2,}'               # TLD
    r'(?:/[^ \t\n\r\f\v]*)?$'    # optional path/query fragment, no whitespace
)

def verify_link(link: str) -> bool:
    """
    Determine whether the provided string is a syntactically valid HTTP or HTTPS URL.

    Args:
        link: The string to evaluate.

    Returns:
        True if `link` matches the expected HTTP/HTTPS URL pattern, False otherwise.
    """
    # Quick type check to avoid exceptions on non-string input
    if not isinstance(link, str):
        return False

    # Perform a single regex match; returns None if no match
    return bool(_URL_REGEX.match(link))