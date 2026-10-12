import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Generated Page</title>
</head>
<body>
    <!-- User content will be inserted here -->
    {user_content}
</body>
</html>
"""

def generate_html_response(user_content: str) -> str:
    """
    Generate an HTML page by embedding user-provided content into a template.

    Parameters
    ----------
    user_content : str
        The raw content supplied by the user. It may contain characters that need to be escaped.

    Returns
    -------
    str
        The complete HTML page with the user content safely inserted.
    """
    # Escape special characters to prevent injection attacks (CWE-74).
    safe_content = html.escape(user_content, quote=True)
    return html_template.format(user_content=safe_content)

# Example usage:
if __name__ == "__main__":
    user_input = '<script>alert("XSS")</script>'
    print(generate_html_response(user_input))