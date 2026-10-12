#!/usr/bin/env python3
"""
Add a custom HTTP response header safely.

The function validates the user supplied value to ensure that it does not
contain CRLF characters or any other control sequences that could lead to
header injection (CWE‑74).  Only printable ASCII characters are allowed,
excluding CR (`\r`) and LF (`\n`).

Author: ChatGPT
"""

import re

# Regular expression that matches a string containing only printable ASCII
# characters (0x20‑0x7E) but no CR or LF.
_VALID_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]+$')

def add_response_header(response_header: str) -> str:
    """
    Construct a safe HTTP header line for the given user supplied value.

    Parameters
    ----------
    response_header : str
        The custom header value provided by the user.  It must be a string
        containing only printable ASCII characters and must not contain
        carriage return (`\r`) or line feed (`\n`).

    Returns
    -------
    str
        A fully formed header line including the header name, a colon,
        a space, the validated value, and a trailing CRLF.

    Raises
    ------
    ValueError
        If `response_header` contains disallowed characters.
    """
    if not isinstance(response_header, str):
        raise ValueError("Header value must be a string")

    # Ensure the header does not contain CR or LF and only printable ASCII
    if not _VALID_HEADER_VALUE_RE.match(response_header):
        raise ValueError(
            "Invalid header value: must contain only printable ASCII "
            "(excluding CR and LF)."
        )

    # Construct the header line.  The header name is hard‑coded to avoid
    # injection via the header name itself.
    return f"Custom-Header: {response_header}\r\n"