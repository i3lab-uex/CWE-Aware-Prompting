import re

# Compile a simple, non‑backtracking regex that matches HTTP/HTTPS URLs.
# The pattern allows the standard set of characters used in URLs while
# avoiding any nested quantifiers that could lead to exponential
# backtracking (CWE‑1333).
_URL_RE = re.compile(
    r'^https?://'                     # http:// or https://
    r'[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]*$',  # allowed URL characters
    re.ASCII,
)

def check_path(input_path: str) -> bool:
    """
    Return True if *input_path* is a syntactically valid HTTP/HTTPS URL,
    otherwise False.  No exceptions are raised for malformed input.

    Parameters
    ----------
    input_path : str
        The string to validate as a URL path.

    Returns
    -------
    bool
        True if the input matches the expected HTTP/HTTPS format, False otherwise.
    """
    # Use fullmatch to ensure the entire string conforms to the pattern
    return bool(_URL_RE.fullmatch(input_path))