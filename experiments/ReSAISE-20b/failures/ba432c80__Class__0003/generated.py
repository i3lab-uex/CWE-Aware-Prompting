import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their expected signatures.
DOC_SIGS = {
    # Example entries – replace with real data in production
    "https://example.com/doc1.pdf": "f0a8c9d3e5b7...",
    "https://example.com/doc2.pdf": "a1b2c3d4e5f6...",
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that a document at *url* is accessible and that the supplied
    cryptographic signature (*sign_hash*) matches the expected value.

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
        If the document at *url* cannot be accessed (e.g., network error,
        404, etc.).
    """
    # First ensure the document is reachable.
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            # We don't actually need the content; just confirm access.
            if resp.status != 200:
                raise urllib.error.HTTPError(url, resp.status,
                                            resp.reason, resp.headers, None)
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        # Wrap network-related errors in an IOError to match the spec.
        raise IOError(f"Unable to access document at {url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # If we have no record of the signature, reject it.
        return False

    # Perform a constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(sign_hash, expected_sig)