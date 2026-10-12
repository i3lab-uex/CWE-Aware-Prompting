import re

# Pre‑compiled, non‑capturing regex pattern for a basic URL validation.
# This pattern covers http/https schemes, optional www., domain names,
# optional port, path, query and fragment. It avoids nested quantifiers
# that could trigger catastrophic backtracking.
_URL_PATTERN = re.compile(
    r"""
    ^                                   # start of string
    (?:(?:http|https)://)?              # optional scheme
    (?:\w+(?:[-.]\w+)*\.\w{2,})         # domain
    (:\d{1,5})?                         # optional port
    (?:/[^\s?#]*)?                      # optional path
    (?:\?[^\s#]*)?                      # optional query
    (?:#[^\s]*)?                        # optional fragment
    $                                   # end of string
    """,
    re.IGNORECASE | re.VERBOSE,
)

def check_url_format(link: str) -> bool:
    """
    Validate whether the given string is a syntactically correct URL.

    Parameters
    ----------
    link : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.
    """
    # Defensive copy and strip whitespace to avoid accidental false negatives
    if not isinstance(link, str):
        return False
    link = link.strip()
    return bool(_URL_PATTERN.match(link))