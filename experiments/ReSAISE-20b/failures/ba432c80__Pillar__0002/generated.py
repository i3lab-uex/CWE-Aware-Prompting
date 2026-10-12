import requests
from hmac import compare_digest

# Global dictionary mapping URLs to the expected cryptographic signature.
DOC_SIGS = {
    # Example entries (to be replaced with real data in production)
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1234567890abcdef1234",
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Validate a document's cryptographic signature.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the provided signature matches the expected value for the URL,
        False otherwise.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible.
    """
    # Ensure we only accept HTTPS URLs to mitigate MITM attacks.
    if not url.lower().startswith("https://"):
        raise IOError(f"Insecure or unsupported URL scheme: {url}")

    try:
        # Fetch the document with a short timeout to avoid hanging.
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Any network/HTTP error results in an IOError to signal failure.
        raise IOError(f"Unable to access document at {url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # If we don't know the signature, treat it as invalid.
        return False

    # Use constant‑time comparison to avoid timing attacks (CWE-693).
    return compare_digest(sign_hash, expected_sig)