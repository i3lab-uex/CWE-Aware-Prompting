import requests
import hmac

# Example global mapping of document URLs to their correct cryptographic signatures.
# In a real system this would be populated from a secure source or database.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a3f5e8c4b9d2e7f0",
    "https://example.com/doc2.pdf": "1c4b9e7f0a3d5e8c",
    # ... more entries ...
}

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a remote document.

    Parameters
    ----------
    doc_link : str
        URL of the document to validate.
    check_signature : str
        Signature supplied for verification.

    Returns
    -------
    bool
        True if the signature matches, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the provided URL.
    """
    # Ensure the link is a valid HTTP/HTTPS URL
    if not doc_link.startswith(("http://", "https://")):
        raise ValueError("Invalid URL scheme. Only HTTP/HTTPS are allowed.")

    # Attempt to fetch the document to confirm its existence.
    try:
        response = requests.get(doc_link, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Any network or HTTP error is treated as the document being unavailable.
        raise IOError(f"Unable to access document at {doc_link}") from exc

    # Retrieve the expected signature from the global mapping.
    stored_signature = DOCUMENT_SIGNATURES.get(doc_link)
    if stored_signature is None:
        # If the URL isn't known, we consider it an invalid document.
        raise IOError(f"No stored signature found for {doc_link}")

    # Perform a constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(stored_signature, check_signature)