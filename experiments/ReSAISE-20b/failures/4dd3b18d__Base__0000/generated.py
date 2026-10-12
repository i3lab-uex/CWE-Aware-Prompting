import hashlib
import hmac
import urllib.request
from urllib.error import URLError, HTTPError

# Global dictionary mapping document URLs to their expected signatures.
# Example:
# DOC_SIGNATURES = {
#     "https://example.com/doc1.pdf": "5f2d9c...",
#     ...
# }
DOC_SIGNATURES = {}

def _fetch_document(url: str) -> bytes:
    """
    Attempt to fetch the document at the given URL.

    Raises:
        IOError: If the resource cannot be accessed.
    """
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to access document at {url}") from exc

def _expected_signature(url: str) -> str:
    """
    Retrieve the expected signature for a given URL.

    Raises:
        KeyError: If no signature is registered for the URL.
    """
    return DOC_SIGNATURES[url]

def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate the cryptographic signature of a document located at `file_url`.

    The function performs the following steps:
        1. Ensure the document is reachable (raises IOError if not).
        2. Retrieve the expected signature from `DOC_SIGNATURES`.
        3. Compare the provided signature with the expected one using
           constant‑time comparison to mitigate timing attacks.

    Args:
        file_url (str): The URL of the document to validate.
        sign (str): The cryptographic signature submitted with the document.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        IOError: If the document at `file_url` cannot be accessed.
        KeyError: If no expected signature is registered for the URL.
    """
    # Step 1: Confirm document accessibility
    _fetch_document(file_url)

    # Step 2: Retrieve expected signature
    expected = _expected_signature(file_url)

    # Ensure both signatures are comparable strings (hex or base64)
    if not isinstance(sign, str) or not isinstance(expected, str):
        return False

    # Step 3: Constant‑time comparison
    return hmac.compare_digest(sign.strip(), expected.strip())