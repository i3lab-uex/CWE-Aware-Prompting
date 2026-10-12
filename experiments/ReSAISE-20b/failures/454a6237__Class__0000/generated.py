import re

# Pre‑compiled regex that matches a valid http or https URL.
# The pattern is intentionally simple and avoids nested quantifiers
# that could trigger catastrophic backtracking (CWE‑407).
_HTTP_URL_RE = re.compile(
    r"""
    \A                                  # start of string
    https?://                           # http or https scheme
    (?:                                 # host part: either IPv4, IPv6 or hostname
        (?:
            \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}   # IPv4
            |
            \[ [A-Fa-f0-9:]+\]                  # IPv6
            |
            (?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}    # hostname
        )
    )
    (?:\:\d{1,5})?                      # optional port
    (?:/[^ \t\n\r\f\v]*)?               # optional path and query fragment
    \Z                                  # end of string
    """,
    re.VERBOSE,
)

def check_path_validity(path_string: str) -> bool:
    """
    Verify if the supplied string is a syntactically valid http or https URL.

    Parameters
    ----------
    path_string : str
        The string to validate.

    Returns
    -------
    bool
        True if the string matches a valid http/https URL, False otherwise.
    """
    # Ensure input is a string; non‑string inputs are considered invalid.
    if not isinstance(path_string, str):
        return False

    # Use the pre‑compiled regex for a fast, constant‑time match.
    return bool(_HTTP_URL_RE.match(path_string))