import urllib.request
import urllib.error

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_SIGNATURES = {
    # Example entries:
    # "https://example.com/docs/report.pdf": "a1b2c3d4e5f6...",
    # "https://example.org/files/data.json": "1234567890abcdef..."
}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Verify that the cryptographic signature `sign` matches the expected
    signature for the document located at `file_url`.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    sign : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value; False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` cannot be accessed (e.g., network error,
        HTTP 404, etc.).
    """
    # Ensure the URL is reachable. This also protects against typos in
    # DOC_SIGNATURES keys that could otherwise lead to a silent False.
    try:
        with urllib.request.urlopen(file_url, timeout=10) as response:
            # We don't actually need the content; we just check that a 200 OK
            # response is returned. Any non-2xx status will raise an HTTPError.
            if response.status != 200:
                raise urllib.error.HTTPError(
                    file_url, response.status, "Non-OK status", None, None
                )
    except urllib.error.HTTPError as e:
        raise IOError(f"HTTP error when accessing {file_url}: {e}") from None
    except urllib.error.URLError as e:
        raise IOError(f"URL error when accessing {file_url}: {e}") from None
    except Exception as e:
        # Catch-all for any other exceptions that may arise during the request.
        raise IOError(f"Failed to access {file_url}: {e}") from None

    # Retrieve the expected signature for this URL.
    expected_sign = DOC_SIGNATURES.get(file_url)

    # If no entry exists for the URL, treat it as a mismatch.
    if expected_sign is None:
        return False

    # Compare the provided signature with the expected one in a
    # constant‑time manner to avoid timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(sign, expected_sign)