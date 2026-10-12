import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_SIGS = {
    # Example entries (replace with real values in production)
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1234567890abcdef1234",
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Validate that the supplied cryptographic signature matches the expected
    signature for a document located at ``url``.

    Parameters:
        url (str): The URL of the document to validate.
        sign_hash (str): The cryptographic signature submitted with the document.

    Returns:
        bool: ``True`` if the signature matches the expected value, otherwise
              ``False``.

    Raises:
        IOError: If the document at the provided URL is inaccessible (e.g.,
                 network error, HTTP status >= 400).
    """
    # Verify that the document is reachable before checking its signature.
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status >= 400:
                raise IOError(f"Document inaccessible: HTTP {resp.status}")
    except urllib.error.URLError as exc:
        raise IOError(f"Unable to access document: {exc}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # No known signature for this URL; treat as invalid.
        return False

    # Use constant‑time comparison to mitigate timing attacks (CWE-693).
    return hmac.compare_digest(sign_hash, expected_sig)