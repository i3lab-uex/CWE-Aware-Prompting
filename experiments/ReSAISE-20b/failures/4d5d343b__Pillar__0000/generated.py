import re

# Compile the regex once at module load time to avoid repeated compilation overhead.
_TAG_RE = re.compile(r"<[^>]+>", flags=re.IGNORECASE | re.DOTALL)

def grab_html_tags(html_code: str) -> list:
    """
    Return a list of all HTML tags found in *html_code*.

    The function is resilient: if any exception occurs (e.g. invalid input type),
    it will catch the error and return an empty list instead of propagating
    the exception. This prevents resource leaks or crashes in calling code.

    Parameters
    ----------
    html_code : str
        A string containing HTML content to be scanned.

    Returns
    -------
    list
        A list of tag strings (e.g., '<div>', '</p>', '<img src="...">').
    """
    try:
        if not isinstance(html_code, str):
            # Non‑string input: treat as empty string.
            html_code = ""

        # Find all matches; the regex captures anything that looks like an HTML tag.
        return _TAG_RE.findall(html_code)
    except Exception:
        # In case of any unexpected error, return an empty list to avoid raising.
        return []