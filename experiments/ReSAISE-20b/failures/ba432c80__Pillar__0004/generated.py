import requests
from hmac import compare_digest

# Global dictionary containing the expected signatures for each document URL.
DOC_SIGS = {
    # Example entries; replace with real URLs and signatures as needed.
    "https://example.com/doc1.pdf": "a3f5c2e8b4d9...",
    "https://example.com/doc2.pdf": "7b1e6f4c9a2d...",
    # Add more URLs and their corresponding expected signatures here.
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Validate a document's cryptographic signature against the expected value.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible.
    """
    # Verify that we can reach the URL (basic connectivity check).
    try:
        # Use a HEAD request to minimize data transfer; follow redirects.
        response = requests.head(url, allow_redirects=True, timeout=5)
        if not response.ok:
            raise IOError(f"Unable to access document at {url} (status code: {response.status_code})")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document at {url}: {exc}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # If the URL is unknown, treat it as an invalid signature.
        return False

    # Use constant‑time comparison to mitigate timing attacks (CWE-693).
    return compare_digest(sign_hash, expected_sig)