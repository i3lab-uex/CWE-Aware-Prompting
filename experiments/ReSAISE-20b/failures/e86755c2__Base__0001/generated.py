import re

# Pre‑compiled regex that matches typical http/https URLs.
# It is intentionally simple to avoid catastrophic backtracking
# and to keep the complexity linear in the input length.
_HTTP_URL_RE = re.compile(
    r'^https?://'                # http:// or https://
    r'(?:[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?)'  # domain (no leading/trailing . or -)
    r'(?:\:\d+)?'                # optional port
    r'(?:/[^\s]*)?$'             # optional path, query or fragment (no whitespace)
)

def verify_link(link: str) -> bool:
    """
    Determine whether *link* is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to test as a potential URL.

    Returns
    -------
    bool
        ``True`` if *link* matches the expected structure, otherwise ``False``.

    Notes
    -----
    - The function performs only a lightweight syntax check; it does not resolve the URL
      or verify network accessibility.
    - The regular expression is deliberately simple to avoid excessive backtracking
      and potential denial‑of‑service vulnerabilities (CWE‑1333).
    """
    if not isinstance(link, str):
        return False
    return bool(_HTTP_URL_RE.match(link))