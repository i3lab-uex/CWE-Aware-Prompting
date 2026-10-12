import urllib.parse

def check_url_format(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid HTTP/HTTPS URL,
    otherwise return False. No exception is raised.
    """
    if not isinstance(link, str):
        return False

    # Strip surrounding whitespace
    link = link.strip()
    if not link:
        return False

    # Parse the URL
    parsed = urllib.parse.urlparse(link)

    # Must have http or https scheme and a non-empty network location
    if parsed.scheme not in ("http", "https"):
        return False
    if not parsed.netloc:
        return False

    # Reject URLs containing whitespace or control characters
    if any(c.isspace() for c in link):
        return False

    # Basic check: the URL must be fully parsed
    if not parsed.path and not parsed.params and not parsed.query and not parsed.fragment:
        # e.g. "http://example.com" is fine
        pass

    return True