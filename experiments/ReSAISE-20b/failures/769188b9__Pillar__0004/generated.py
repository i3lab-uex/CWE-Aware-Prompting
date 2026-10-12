import urllib.request
import urllib.error
import ssl
from hmac import compare_digest

# Global dictionary mapping resource URLs to their expected cryptographic signatures.
# Example:
# DOC_HASHES = {
#     "https://example.com/doc1.pdf": "a3f5c9...",
#     ...
# }
DOC_HASHES = {}  # Should be populated elsewhere in the application.

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the cryptographic signature supplied for a remote document
    matches the expected value stored in DOC_HASHES.

    Parameters
    ----------
    resource_url : str
        The URL of the document to validate.
    crypto_signature : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the supplied signature matches the expected value,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` is inaccessible (network error,
        non-200 HTTP status, etc.).
    """
    # Ensure we are accessing a secure URL (HTTPS).  This mitigates
    # CWE-693 by avoiding insecure transport channels.
    if not resource_url.lower().startswith("https://"):
        raise IOError(f"Insecure URL scheme: {resource_url}")

    # Attempt to access the document to confirm it is reachable.
    try:
        req = urllib.request.Request(resource_url, method="HEAD")
        # Use a default SSL context that verifies certificates.
        context = ssl.create_default_context()
        with urllib.request.urlopen(req, context=context) as resp:
            # A 200 OK (or any 2xx status) indicates accessibility.
            if not 200 <= resp.getcode() < 300:
                raise IOError(f"Document returned non-success status {resp.getcode()}")
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to access document at {resource_url}: {exc}") from exc

    # Retrieve the expected signature for this URL.
    expected_signature = DOC_HASHES.get(resource_url)
    if expected_signature is None:
        # No known signature for this URL; treat as authentication failure.
        return False

    # Use constant‑time comparison to mitigate timing attacks (CWE-693).
    return compare_digest(crypto_signature, expected_signature)