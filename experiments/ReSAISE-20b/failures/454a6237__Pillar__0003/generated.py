import re

# Regular expression pattern for a valid HTTP or HTTPS URL.
# This is a simplified version that checks the scheme, host, optional port,
# and optional path/query/fragment components. It does not validate the
# actual existence of the host or resource.
_HTTP_URL_REGEX = re.compile(
    r"""
    ^                                   # start of string
    (https?)://                         # http or https scheme and ://
    (?:
        [A-Za-z0-9\-._~%]+              # hostname or IP part
        (?:\.[A-Za-z0-9\-._~%]+)*      # optional additional subdomains
        |
        \[[A-Fa-f0-9:]+\]              # IPv6 literal
    )
    (?::\d{1,5})?                       # optional port number (0-65535)
    (?:
        /[^ \t\r\n]*                   # optional path and query/fragment
    )?                                  # path is optional
    $                                   # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_path_validity(path_string: str) -> bool:
    """
    Verify if a given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    path_string : str
        The input string to validate as a URL.

    Returns
    -------
    bool
        True if the path_string matches the HTTP/HTTPS pattern, False otherwise.

    Notes
    -----
    - The function uses a precompiled regular expression for efficiency.
    - It does not attempt to resolve the host or check network connectivity,
      only syntactic validity.
    - No exceptions are raised; malformed input simply results in False.
    """
    if not isinstance(path_string, str):
        return False

    # Use fullmatch to ensure the entire string matches the pattern.
    return bool(_HTTP_URL_REGEX.fullmatch(path_string.strip()))