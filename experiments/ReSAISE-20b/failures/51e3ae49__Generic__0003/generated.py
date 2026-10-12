import requests
import hmac

# Example global dictionary mapping URLs to their correct signatures.
# In practice this would be populated from a secure source.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "abc123",
    "https://example.com/doc2.pdf": "def456",
    # add more entries as needed
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate a document's integrity by comparing the provided cryptographic
    signature with the stored one.

    Parameters:
        file_url (str): The URL of the document to validate.
        crypt_signature (str): The signature supplied for verification.

    Returns:
        bool: True if the provided signature matches the stored one,
              False otherwise.

    Raises:
        IOError: If the document cannot be found at the specified URL.
    """
    # Ensure the URL exists in our trusted signature store
    if file_url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document not found: {file_url}")

    # Perform a HEAD request to confirm the document is reachable
    try:
        response = requests.head(file_url, timeout=10)
    except requests.RequestException as exc:
        raise IOError(f"Could not access document at {file_url}") from exc

    if response.status_code == 404:
        raise IOError(f"Document not found (404): {file_url}")
    if response.status_code >= 400:
        raise IOError(f"Error accessing document (status {response.status_code}): {file_url}")

    # Retrieve the stored signature
    expected_signature = DOCUMENT_SIGNATURES[file_url]

    # Use a constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(crypt_signature, expected_signature)