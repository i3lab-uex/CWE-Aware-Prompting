import urllib.parse

def check_url_format(link: str) -> bool:
    """
    Validate whether a given string is a properly formatted URL.

    The function uses urllib.parse.urlparse to decompose the URL and then
    performs minimal checks on the scheme and network location (netloc).
    This approach avoids the pitfalls of complex regular expressions
    (e.g., catastrophic backtracking) and is efficient even on long or
    maliciously crafted input.

    Parameters:
        link (str): The string to validate as a URL.

    Returns:
        bool: True if the input is a valid URL, False otherwise.
    """
    try:
        parsed = urllib.parse.urlparse(link)
        # A valid URL must have a scheme (http, https, ftp, etc.) and a non-empty netloc.
        if not parsed.scheme or not parsed.netloc:
            return False

        # Accept common schemes; extend the set if needed.
        allowed_schemes = {"http", "https", "ftp"}
        if parsed.scheme.lower() not in allowed_schemes:
            return False

        # Ensure the netloc does not contain spaces or control characters.
        if any(c.isspace() for c in parsed.netloc):
            return False

        # Additional basic checks: the URL should not be just a scheme.
        if link.strip().startswith(parsed.scheme + "://"):
            return True

        return False
    except Exception:
        # No exceptions should propagate; any error results in a False outcome.
        return False