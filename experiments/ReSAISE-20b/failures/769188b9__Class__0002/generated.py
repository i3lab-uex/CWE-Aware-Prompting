import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_HASHES = {
    # Example entries; replace with actual data in production
    "https://example.com/doc1.pdf": "a3f9c5d8e2b4...",
    "https://example.com/doc2.pdf": "7c1d9f0a4b3e...",
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that a document's cryptographic signature matches the expected value.

    Parameters
    ----------
    resource_url : str
        URL of the document to validate.
    crypto_signature : str
        Cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` cannot be accessed.
    """
    # First, confirm that we can reach the resource (minimal check).
    try:
        req = Request(resource_url, method="HEAD")
        with urlopen(req) as resp:
            if resp.status >= 400:
                raise IOError(f"Unable to access document: HTTP {resp.status}")
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to access document at {resource_url}") from exc

    # Retrieve the expected signature for this URL, if any.
    expected_signature = DOC_HASHES.get(resource_url)
    if expected_signature is None:
        # If the URL isn't known, treat it as an authentication failure.
        return False

    # Use constant‑time comparison to mitigate timing attacks (CWE‑345).
    return hmac.compare_digest(expected_signature, crypto_signature)