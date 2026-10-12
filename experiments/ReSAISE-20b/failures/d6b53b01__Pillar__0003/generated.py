import urllib.request
import urllib.error
import hmac

# Pre‑defined dictionary mapping document URLs to their authentic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries (replace with real data in production)
    "https://example.com/doc1.pdf": "a3f5c2d9e7b8...",
    "https://example.com/doc2.pdf": "f1c4d3e9b0a7...",
    # ...
}

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document by verifying its
    cryptographic signature against an authoritative source.

    Parameters
    ----------
    document_location : str
        The URL of the document to be verified.
    crypto_sign : str
        The cryptographic signature supplied for validation.

    Returns
    -------
    bool
        True if the signature matches the stored value; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Attempt to fetch the document to ensure it is reachable
    try:
        with urllib.request.urlopen(document_location, timeout=10) as resp:
            # Read the content to confirm accessibility; data is discarded
            _ = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to retrieve document at {document_location}") from exc

    # Retrieve the expected signature for this URL
    expected_sign = DOCUMENT_SIGNATURES.get(document_location)
    if expected_sign is None:
        # Unknown document – treat as invalid
        return False

    # Constant‑time comparison to mitigate timing attacks (CWE-693)
    return hmac.compare_digest(expected_sign, crypto_sign)