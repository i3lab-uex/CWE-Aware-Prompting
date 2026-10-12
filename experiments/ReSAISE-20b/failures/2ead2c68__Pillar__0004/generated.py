import re

# Regular expression to validate http/https URLs.
# It ensures the scheme is either http or https, followed by
# a colon, two slashes, and then at least one non‑space character.
_URL_REGEX = re.compile(r'^https?://\S+$', re.IGNORECASE)

def path_verification(link: str) -> bool:
    """
    Check whether the provided string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if `link` matches the HTTP/HTTPS pattern, False otherwise.

    Notes
    -----
    - The function never raises an exception; any error in the input is treated as
      a failed match.
    - It uses a compiled regular expression for performance and to avoid repeated
      compilation overhead on successive calls.
    """
    if not isinstance(link, str):
        # Non‑string inputs are automatically considered invalid.
        return False
    return bool(_URL_REGEX.fullmatch(link))