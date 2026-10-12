import re

# Regular expression for a basic HTTP/HTTPS URL.
# It matches:
#   - scheme: http or https
#   - host (IPv4, IPv6, domain name)
#   - optional port
#   - optional path/query/fragment (anything except whitespace)
_HTTP_URL_RE = re.compile(
    r"""^
    https?://                                 # http or https scheme
    (?:                                        # host part
        (?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+   # sub‑domains
        [A-Za-z]{2,63}                         # top level domain
    |
        \d{1,3}(?:\.\d{1,3}){3}                # IPv4
    |
        \[([A-Fa-f0-9:]+)\]                    # IPv6
    )
    (?::\d{1,5})?                              # optional port
    (?:/[^\s]*)?                               # optional path/query/fragment
    $""",
    re.VERBOSE | re.IGNORECASE,
)


def check_path(input_path: str) -> bool:
    """
    Return True if `input_path` is a valid HTTP or HTTPS URL, otherwise False.
    The function never raises an exception.

    Parameters
    ----------
    input_path : str
        The string to evaluate.

    Returns
    -------
    bool
        True if the input matches a typical HTTP/HTTPS URL pattern.
    """
    try:
        return bool(_HTTP_URL_RE.match(input_path))
    except Exception:  # pragma: no cover
        return False