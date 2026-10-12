import requests
from hmac import compare_digest

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_SIGS = {
    # Example entries; replace with real URLs and signatures
    "https://example.com/doc1.pdf": "a3f5c9d7e8b0...",
    "https://example.com/doc2.pdf": "4c1a9f3b7e6d...",
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a document hosted at `url`.

    Parameters
    ----------
    url : str
        The HTTPS URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document at `url` cannot be accessed (e.g., network error,
        non-200 status code, or SSL verification failure).
    """
    # 1. Ensure the URL is reachable and accessible.
    try:
        resp = requests.head(url, allow_redirects=True, timeout=5)
        if resp.status_code != 200:
            raise IOError(f"Document not accessible, status code {resp.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document at {url}") from exc

    # 2. Retrieve the expected signature for this URL.
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # No signature known for this URL; treat as invalid.
        return False

    # 3. Compare the provided signature with the expected one in a timing‑safe manner.
    return compare_digest(sign_hash, expected_sig)