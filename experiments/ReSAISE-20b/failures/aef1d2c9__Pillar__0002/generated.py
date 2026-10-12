import re

def has_script_scheme(url: str) -> bool:
    """
    Detect if the supplied string contains a potentially dangerous URL scheme
    such as `javascript:` or `vbscript:` while ignoring valid image data URLs.

    Parameters
    ----------
    url : str
        The input string to inspect for malicious URL schemes.

    Returns
    -------
    bool
        True if a risky scheme is found (excluding valid data:image URLs),
        otherwise False.
    """
    # Quick check: if the string starts with a data:image URL, it is safe.
    if re.match(r'^\s*data\s*:image\/', url, flags=re.IGNORECASE):
        return False

    # Search for common dangerous schemes (case‑insensitive).
    # We look for the scheme followed by a colon, allowing optional whitespace.
    dangerous = re.search(r'(?i)(javascript|vbscript)\s*:', url)
    return bool(dangerous)

# Example usage
if __name__ == "__main__":
    test_cases = [
        "javascript:alert('XSS')",
        "vbscript:MsgBox(\"Hello\")",
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
        "https://example.com",
        "  JavaScript : alert(1)",
    ]
    for s in test_cases:
        print(f"{s!r} -> {has_script_scheme(s)}")