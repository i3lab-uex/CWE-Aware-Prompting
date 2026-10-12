import re

# Regular expression that matches a valid http or https URL.
# It ensures the scheme is http or https, followed by "://",
# and then at least one non‑whitespace character.
_HTTP_URL_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)

def verify_link(link: str) -> bool:
    """
    Determine whether a given string is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if the input matches the HTTP/HTTPS pattern, False otherwise.
    """
    # Guard against non‑string inputs by returning False instead of raising an exception.
    if not isinstance(link, str):
        return False

    # Use the compiled regular expression to test the input.
    return bool(_HTTP_URL_RE.match(link))