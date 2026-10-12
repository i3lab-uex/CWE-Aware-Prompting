import hashlib
import requests

# Pre‑defined dictionary mapping URLs to their authentic SHA‑256 signatures.
DOCUMENT_SIGNATURES = {
    # Example entries (URL: signature)
    "https://example.com/doc1.pdf": "a3f5c2b8d9e7... (full 64‑char hex)",
    "https://example.com/doc2.pdf": "b1c4d6e8f0a9... (full 64‑char hex)",
    # Add more entries as required
}


def _compute_sha256(content: bytes) -> str:
    """
    Compute the SHA‑256 hex digest of the given binary content.
    """
    hasher = hashlib.sha256()
    hasher.update(content)
    return hasher.hexdigest()


def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate a remotely hosted document by comparing its SHA‑256 signature
    against the authentic signature stored in DOCUMENT_SIGNATURES.

    Parameters:
        url (str): The URL of the document to be validated.
        crypt_signature (str): The provided cryptographic signature
            (hex string) that should match the authentic one.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the given URL.
    """
    # Retrieve the remote document
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {url}") from exc

    # Compute the SHA‑256 digest of the downloaded content
    local_digest = _compute_sha256(response.content)

    # Fetch the authentic signature for this URL
    authentic_sig = DOCUMENT_SIGNATURES.get(url)
    if not authentic_sig:
        # If no signature is stored for this URL, treat it as invalid
        return False

    # Compare the provided signature with both the local digest and the stored one
    if crypt_signature.lower() == authentic_sig.lower() and \
       local_digest.lower() == authentic_sig.lower():
        return True

    return False