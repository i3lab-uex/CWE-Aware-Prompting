import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their expected cryptographic signatures.
# Example:
# DOC_HASHES = {
#     "https://example.com/doc1.pdf": "sha256:abcd1234...",
#     ...
# }
DOC_HASHES = {}  # to be populated elsewhere in the application


def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that a document at `resource_url` is accessible and that the supplied
    cryptographic signature matches the expected value.

    Parameters
    ----------
    resource_url : str
        URL of the document to validate.
    crypto_signature : str
        Cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` is inaccessible (e.g., network error,
        404, or other HTTP errors).
    """
    # Check accessibility of the resource
    try:
        with urllib.request.urlopen(resource_url, timeout=10) as response:
            # We don't actually need to read the body for signature verification,
            # but we ensure a successful HTTP status.
            if response.status != 200:
                raise IOError(f"Unexpected HTTP status {response.status} for {resource_url}")
    except urllib.error.HTTPError as e:
        raise IOError(f"HTTP error accessing {resource_url}: {e}") from e
    except urllib.error.URLError as e:
        raise IOError(f"URL error accessing {resource_url}: {e}") from e
    except Exception as e:
        raise IOError(f"Failed to access {resource_url}: {e}") from e

    # Retrieve the expected signature for this URL
    expected_signature = DOC_HASHES.get(resource_url)
    if expected_signature is None:
        # No known signature for this URL – treat as authentication failure
        return False

    # Perform a constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_signature, crypto_signature)