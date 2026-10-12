import urllib.request
import urllib.error
import hmac

# Example global dictionary containing expected signatures for each document URL.
DOC_HASHES = {
    "https://example.com/docs/report.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/docs/summary.pdf": "6c569aabbf7775ef8fc570e228c16b98",
    # Add more entries as needed
}

def _is_url_accessible(url: str) -> bool:
    """
    Perform a lightweight HEAD request to verify that the URL is reachable.
    Returns True if the server responds with a 2xx status code, False otherwise.
    """
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return 200 <= resp.getcode() < 300
    except (urllib.error.HTTPError, urllib.error.URLError):
        return False

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected value
    for the document located at `resource_url`.

    Parameters
    ----------
    resource_url : str
        The URL of the document to validate.
    crypto_signature : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` is inaccessible.
    """
    # Ensure the URL is reachable before performing any checks
    if not _is_url_accessible(resource_url):
        raise IOError(f"Document at {resource_url} is inaccessible")

    # Retrieve the expected signature from the global dictionary
    expected_signature = DOC_HASHES.get(resource_url)

    # If we have no stored signature for this URL, treat it as invalid
    if expected_signature is None:
        return False

    # Perform a constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)