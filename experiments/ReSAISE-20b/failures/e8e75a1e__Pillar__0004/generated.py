import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detect whether a string contains a potentially malicious URL scheme.

    A URL is considered dangerous if it starts with one of the following
    schemes (case‑insensitive):

        * javascript:
        * vbscript:

    The function also checks for `data:` URLs, but it treats them as safe
    only when the media type is an image (e.g. `data:image/png,...`).  Any
    other `data:` URL is considered dangerous.

    Parameters
    ----------
    url_string : str
        The string to inspect.  It may contain an entire URL or just a
        fragment that includes a scheme.

    Returns
    -------
    bool
        ``True`` if the string contains a malicious scheme, otherwise
        ``False``.

    Notes
    -----
    The function uses regular expressions with the ``re.IGNORECASE`` flag.
    It does not raise exceptions for normal inputs; any malformed regular
    expressions will propagate the usual ``re.error`` exception.
    """
    if not isinstance(url_string, str):
        # Gracefully handle non‑string inputs by treating them as safe
        return False

    # Pattern for known dangerous schemes.
    dangerous_schemes = re.compile(r'(?i)\b(?:javascript|vbscript):')

    if dangerous_schemes.search(url_string):
        return True

    # Detect data: URLs that are NOT image/*, which we treat as dangerous.
    # We use a negative look‑ahead to exclude image media types.
    data_not_image = re.compile(r'(?i)\bdata:(?!image/)', flags=re.IGNORECASE)

    if data_not_image.search(url_string):
        return True

    return False