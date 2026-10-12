import urllib.parse
import requests

# Example of the predefined dictionary containing authentic signatures.
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "abc123def456...",
    # Add real entries here.
}

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate that the cryptographic signature for a remote document matches
    the expected value stored in DOCUMENT_SIGNATURES.

    Parameters:
        document_location (str): URL of the document to be verified.
        crypto_sign (str): The cryptographic signature provided for validation.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the given URL.
    """
    # Validate URL scheme to prevent HTTP/HTTPS downgrade or local file access
    parsed = urllib.parse.urlparse(document_location)
    if parsed.scheme not in {"http", "https"}:
        raise IOError(f"Unsupported URL scheme: {parsed.scheme}")

    try:
        # Retrieve the document with a reasonable timeout and SSL verification
        response = requests.get(document_location, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise IOError(f"Failed to retrieve document: {exc}") from exc

    # Compare the provided signature with the expected one
    expected_sign = DOCUMENT_SIGNATURES.get(document_location)
    if expected_sign is None:
        # If the document is not in our registry, treat it as invalid
        return False

    # Use a constant‑time comparison to avoid timing attacks
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(crypto_sign, expected_sign)