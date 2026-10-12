import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_SIGS = {
    # Example entries (URL : signature)
    "https://example.com/doc1.pdf": "a3f5c2e7b8d9...",
    "https://example.com/doc2.pdf": "4e1f6a8c9b0d...",
    # Add real entries here
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that a document at the given URL is accessible and that the supplied
    cryptographic signature matches the expected value stored in DOC_SIGS.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible (e.g., network error,
        404, etc.).
    """
    # First ensure the URL is reachable. We only check connectivity; we do not
    # download or process the document content for security reasons.
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            # A 200 OK response indicates accessibility.
            if resp.status != 200:
                raise IOError(f"Unable to access document: HTTP {resp.status}")
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to access document at {url}") from exc

    # Retrieve the expected signature for this URL.
    expected = DOC_SIGS.get(url)
    if expected is None:
        # No signature known for this URL; treat as invalid.
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(sign_hash, expected)