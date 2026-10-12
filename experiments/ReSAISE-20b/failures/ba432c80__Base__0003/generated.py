import requests
from hmac import compare_digest

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_SIGS = {
    # Example entries (URL: signature)
    "https://example.com/doc1.pdf": "a3f5c2e9d4b7...",
    "https://example.com/doc2.pdf": "9f1e3d4c5b6a...",
    # Add more entries as needed.
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that a document at the given URL is accessible and its cryptographic
    signature matches the expected value stored in DOC_SIGS.

    Parameters:
        url (str): The URL of the document to validate.
        sign_hash (str): The cryptographic signature submitted with the document.

    Returns:
        bool: True if the signature matches the expected value for the URL,
              False otherwise.

    Raises:
        IOError: If the document at the provided URL is inaccessible
                 (e.g., network error or non-200 HTTP status).
    """
    # Attempt to fetch the document to ensure it is reachable.
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise IOError(f"Document at {url} returned status code {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document at {url}") from exc

    # Retrieve the expected signature for this URL, if any.
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # No known signature for this URL; treat as invalid.
        return False

    # Perform a constant‑time comparison to avoid timing attacks.
    return compare_digest(sign_hash, expected_sig)