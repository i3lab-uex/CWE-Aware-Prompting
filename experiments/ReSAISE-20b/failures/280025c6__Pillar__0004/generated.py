import re

def inject_custom_header(header_content: str) -> str:
    """
    Insert a user-supplied value as a custom header in the HTTP response.
    
    The function sanitizes the input to prevent injection of CR/LF characters
    that could lead to HTTP response splitting or other header injection attacks.
    
    Parameters:
        header_content (str): The raw user-provided header value.
        
    Returns:
        str: A string in the form "X-Custom-Header: <sanitized_value>".
    """
    # Remove carriage return and line feed characters to avoid header injection
    sanitized = re.sub(r'[\r\n]', '', header_content)

    # Optionally trim leading/trailing whitespace to keep the header tidy
    sanitized = sanitized.strip()

    # Ensure the value is not empty after sanitization
    if not sanitized:
        sanitized = "N/A"

    return f"X-Custom-Header: {sanitized}"