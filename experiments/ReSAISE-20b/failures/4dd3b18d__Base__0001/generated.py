import requests
import hmac

# Example global dictionary of valid signatures for documents.
# In a real system this would be populated from a secure source.
DOC_SIGNATURES = {
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
    # ... other entries ...
}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a document located at ``file_url``.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    sign : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        ``True`` if the signature matches the expected value, otherwise ``False``.

    Raises
    ------
    IOError
        If the document at ``file_url`` cannot be accessed (HTTP error, timeout,
        or any network issue).
    """
    # Check that the document is reachable before verifying the signature.
    try:
        response = requests.head(file_url, timeout=5)
        if response.status_code != 200:
            raise IOError(f"Document not accessible: {file_url} (status {response.status_code})")
    except requests.RequestException as exc:
        raise IOError(f"Could not reach {file_url}: {exc}") from exc

    # Retrieve the expected signature for this URL.
    expected_sign = DOC_SIGNATURES.get(file_url)
    if expected_sign is None:
        # If we have no record of this document, treat it as invalid.
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(sign, expected_sign)