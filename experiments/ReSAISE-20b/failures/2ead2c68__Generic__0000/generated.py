import re

# Regular expression to validate http or https URLs.
# It checks for the scheme, a non‑empty host, and optional path/query/fragment.
_URL_REGEX = re.compile(
    r'^https?://'                    # http:// or https://
    r'(?:[a-zA-Z0-9\-\.]+)'          # host (simplified, no IDN support)
    r'(?:\:\d+)?'                    # optional port
    r'(?:/[^\s]*)?$',                # optional path (no spaces)
    re.IGNORECASE
)

def path_verification(link: str) -> bool:
    """
    Check whether the given string is a valid http or https URL.

    Parameters
    ----------
    link : str
        The string to validate.

    Returns
    -------
    bool
        True if `link` matches the http/https pattern, False otherwise.
    """
    # Ensure input is a string to avoid type errors
    if not isinstance(link, str):
        return False

    # Return True only if the regex matches
    return bool(_URL_REGEX.match(link))