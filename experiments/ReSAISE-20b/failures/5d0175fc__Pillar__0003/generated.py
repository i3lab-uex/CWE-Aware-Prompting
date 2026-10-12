import re

# Regular expression to validate an http or https URL.
# It allows typical characters in the host, optional port,
# and a path that may contain alphanumerics, punctuation, and percent‑encoding.
_HTTP_URL_RE = re.compile(
    r"""
    ^(?P<scheme>https?)://                             # scheme
    (?:(?P<user>[^:@/\s]+)(?::(?P<pwd>[^@/\s]*))?@)?   # optional user:pwd@
    (?P<host>[a-zA-Z0-9.-]+)                           # host
    (?:\:(?P<port>\d{1,5}))?                           # optional port
    (?P<path>/[^\s]*)?$                                 # path (optional)
    """,
    re.VERBOSE,
)

def verify_path_format(address: str) -> bool:
    """
    Validate whether the given string is a well‑formed HTTP/HTTPS URL.

    Parameters
    ----------
    address : str
        The string to validate.

    Returns
    -------
    bool
        ``True`` if the address matches the expected pattern, otherwise ``False``.

    Notes
    -----
    The function never raises an exception; any parsing error or unexpected input
    simply results in ``False``.
    """
    if not isinstance(address, str):
        return False
    # Use fullmatch to ensure the entire string conforms to the pattern.
    try:
        match = _HTTP_URL_RE.fullmatch(address.strip())
        if not match:
            return False
        # Validate port number range if present.
        port = match.group("port")
        if port is not None:
            try:
                port_num = int(port)
                if not (0 <= port_num <= 65535):
                    return False
            except ValueError:
                return False
        return True
    except Exception:  # pragma: no cover
        # Any unexpected error results in a safe False.
        return False