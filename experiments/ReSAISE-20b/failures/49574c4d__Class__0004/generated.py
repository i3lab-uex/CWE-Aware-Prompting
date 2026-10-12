import re

def extract_html_elements(document: str) -> list[str]:
    """
    Return a list of all substrings in `document` that match HTML tags.
    Tags are defined as sequences starting with '<', ending with '>', and
    containing no nested angle brackets.

    The function is defensive: it never raises an exception; any error
    during regex processing results in an empty list.
    """
    if not isinstance(document, str):
        return []

    # Use a non‑greedy pattern that does not allow nested angle brackets.
    # This prevents catastrophic backtracking on malformed input
    pattern = r'<[^<>]+?>'

    try:
        return re.findall(pattern, document)
    except Exception:
        # In case of unexpected regex errors or other runtime issues,
        # return an empty list instead of propagating the exception.
        return []