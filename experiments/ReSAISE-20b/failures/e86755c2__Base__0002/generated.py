import re

# Compile a simple, non‑backtracking regex for http/https URLs.
# The pattern ensures the string starts with "http://" or "https://",
# followed by at least one non‑space character.
_HTTP_URL_RE = re.compile(r'^https?://\S+$', flags=re.IGNORECASE)


def verify_link(link: str) -> bool:
    """
    Determine whether a string is a valid HTTP/HTTPS URL.

    Parameters
    ----------
    link : str
        The string to evaluate.

    Returns
    -------
    bool
        True if the input matches a simple HTTP/HTTPS URL pattern,
        False otherwise.

    Notes
    -----
    * The function performs a single full‑match operation, which is O(n)
      in the length of `link`.  No backtracking or catastrophic
      exponential complexity is possible.
    * No exceptions are raised; the function returns False for any
      input that does not match the pattern.
    """
    if not isinstance(link, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_HTTP_URL_RE.fullmatch(link))