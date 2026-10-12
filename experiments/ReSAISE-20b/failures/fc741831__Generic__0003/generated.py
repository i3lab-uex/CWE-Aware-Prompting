import hashlib
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Predefined mapping of document URLs to their valid SHA-256 signatures
DOCUMENT_SIGNATURES = {
    # Example:
    # "https://example.com/doc1.pdf": "a3f5c2b4d6e8..."
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remotely hosted document by comparing its
    SHA-256 digest against an expected cryptographic signature.

    Parameters:
        url (str): The URL of the document to retrieve.
        crypt_signature (str): The expected SHA-256 hexadecimal signature.

    Returns:
        bool: True if the computed digest matches the expected signature,
              False otherwise.

    Raises:
        IOError: If the document cannot be fetched from the provided URL.
    """
    try:
        # Use a User-Agent header to avoid being blocked by some servers
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req) as response:
            # Read the entire content (could be large; adjust if needed)
            data = response.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Failed to retrieve document from {url}") from exc

    # Compute SHA-256 digest of the retrieved data
    computed_digest = hashlib.sha256(data).hexdigest()

    # Normalize signatures to lowercase for case‑insensitive comparison
    expected_digest = crypt_signature.lower()
    computed_digest = computed_digest.lower()

    return computed_digest == expected_digest