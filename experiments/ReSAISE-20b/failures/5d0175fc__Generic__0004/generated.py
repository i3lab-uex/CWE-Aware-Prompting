import re

# Regular expression pattern that matches a basic HTTP/HTTPS URL.
# It requires the scheme (http or https), followed by :// and at least one non‑space character.
# This is intentionally simple to avoid complex parsing logic while still validating typical URLs.
_HTTP_URL_PATTERN = re.compile(r'^(https?://[^\s]+)$', re.IGNORECASE)


def verify_path_format(address: str) -> bool:
    """
    Verify if the provided string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    address : str
        The input string to validate as a path.

    Returns
    -------
    bool
        True if the address matches the HTTP/HTTPS URL pattern, False otherwise.

    Notes
    -----
    - The function does not raise any exceptions; it simply returns False for invalid inputs.
    - It uses a straightforward regular expression that checks the scheme and ensures
      there are no whitespace characters in the URL.  More elaborate validation (e.g.
      checking hostnames, ports, query strings) is outside the scope of this function
      and can be added if needed.
    """
    # Ensure address is a string; otherwise return False without raising
    if not isinstance(address, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    return bool(_HTTP_URL_PATTERN.fullmatch(address))