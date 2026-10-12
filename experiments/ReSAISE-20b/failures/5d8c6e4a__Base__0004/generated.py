import hashlib
import urllib.request
from urllib.parse import urlparse

# Example dictionary of known signatures for documents.
# The keys are URLs, the values are hex-encoded SHA256 digests of the document content.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a3b2c4d5e6f7...",
    # Add more entries as needed
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its SHA256 digest
    against an expected signature.

    Parameters
    ----------
    location : str
        URL of the document to be verified.
    sign : str
        Expected hex-encoded SHA256 digest for the document.

    Returns
    -------
    bool
        True if the computed digest matches the expected signature,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    ValueError
        If the URL scheme is not HTTPS (to avoid insecure protocols).
    """
    # Ensure we are using a secure protocol
    parsed = urlparse(location)
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for document retrieval")

    try:
        with urllib.request.urlopen(location, timeout=10) as response:
            data = response.read()
    except Exception as e:
        raise IOError(f"Failed to retrieve document from {location}") from e

    # Compute SHA256 digest of the retrieved content
    computed_digest = hashlib.sha256(data).hexdigest()

    # Compare with expected signature (case-insensitive)
    return computed_digest.lower() == sign.lower()