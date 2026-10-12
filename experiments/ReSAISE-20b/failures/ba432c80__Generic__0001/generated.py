import urllib.request
from urllib.error import URLError, HTTPError

# Example global dictionary mapping URLs to their expected signatures.
# In real usage this would be populated with actual values.
DOC_SIGS = {
    # "https://example.com/doc1.pdf": "abcd1234efgh5678",
    # "https://example.org/report.txt": "9876fedc5432abcd",
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that the cryptographic signature supplied for a document matches
    the expected value stored in DOC_SIGS.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the supplied signature matches the expected value,
        False otherwise.

    Raises
    ------
    IOError
        If the document at ``url`` cannot be accessed (network error,
        HTTP error, etc.).
    """
    # Ensure the URL is reachable before checking the signature.
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            # Read a small portion just to confirm the URL is accessible.
            _ = resp.read(1)
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to access document at {url}") from exc

    # Retrieve the expected signature for this URL.
    expected = DOC_SIGS.get(url)

    if expected is None:
        # No known signature for this URL – treat as invalid.
        return False

    # Compare signatures in a constant‑time manner to avoid timing attacks
    # (although for simple string comparison this is rarely a concern,
    # but good practice for cryptographic values).
    def constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode('utf-8'), b.encode('utf-8')):
            result |= x ^ y
        return result == 0

    return constant_time_compare(sign_hash, expected)