import re

# Regular expression that matches a well‑formed HTTP or HTTPS URL path.
# It allows the scheme (http/https), an optional host, and a path
# that may contain alphanumeric characters, hyphens, underscores,
# periods, slashes, question marks, ampersands, equals signs,
# percent‑encoding, and fragments.
_PATH_RE = re.compile(
    r"""^
        (?:https?://)?                                 # optional scheme
        (?:
            [a-zA-Z0-9.-]+(?::\d+)?                    # hostname with optional port
            (?:/[^\s]*)?                               # optional path component
        )
        $""",
    re.VERBOSE,
)

def check_path(input_path: str) -> bool:
    """
    Determine whether `input_path` is a valid HTTP/HTTPS path.

    Parameters
    ----------
    input_path : str
        The string to be evaluated as a potential valid path.

    Returns
    -------
    bool
        True if the string matches the expected pattern, False otherwise.
    """
    try:
        # Use fullmatch to ensure the entire string conforms to the pattern.
        return bool(_PATH_RE.fullmatch(input_path.strip()))
    except Exception:
        # Any unexpected error (e.g., non-string input) is treated as invalid.
        return False