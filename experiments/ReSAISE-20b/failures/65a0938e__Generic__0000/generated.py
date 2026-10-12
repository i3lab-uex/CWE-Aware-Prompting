import requests
import hmac
from typing import Dict

# Global dictionary mapping document URLs to their correct cryptographic signatures.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries – in real usage this would be populated with actual URLs and signatures.
    "https://example.com/doc1.pdf": "a3f5c8d9e0b2...",
    "https://example.com/doc2.pdf": "1c4d7e9f0a3b...",
    # Add more entries as needed.
}

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that a document at the given URL exists and its signature matches
    the expected cryptographic signature.

    Parameters
    ----------
    doc_link : str
        The URL of the document to validate.
    check_signature : str
        The cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the provided signature matches the stored signature, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (e.g., 404 Not Found).
    """
    # Ensure the document exists by performing a HEAD request.
    try:
        response = requests.head(doc_link, allow_redirects=True, timeout=10)
    except requests.RequestException as exc:
        raise IOError(f"Failed to access the document at {doc_link}: {exc}") from exc

    if response.status_code != 200:
        raise IOError(f"Document not found at {doc_link} (status code: {response.status_code})")

    # Retrieve the expected signature from the global dictionary.
    expected_signature = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_signature is None:
        # If we have no stored signature for this URL, consider it invalid.
        return False

    # Use a constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(check_signature, expected_signature)