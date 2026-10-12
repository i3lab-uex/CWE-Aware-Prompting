import requests
import hmac

# Global dictionary mapping URLs to their expected signatures.
DOC_SIGS = {
    # Example entries; in real usage these would be populated elsewhere
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1234567890abcdef1234",
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for a document located at `url`.

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
        If the document at `url` is inaccessible (network error or HTTP error).
    """
    # Attempt to fetch the document to confirm accessibility.
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Treat any network/HTTP issue as an inaccessible document.
        raise IOError(f"Unable to access document at {url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # No signature known for this URL; treat as mismatch.
        return False

    # Use constant‑time comparison to avoid timing attacks (CWE‑693).
    return hmac.compare_digest(sign_hash, expected_sig)