import html

# HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic Page</title>
</head>
<body>
    {user_content}
</body>
</html>
"""

def build_html_page(page_content: str) -> str:
    """
    Injects user-provided content into an HTML template after proper escaping.

    Args:
        page_content (str): The dynamic content supplied by the user.

    Returns:
        str: A complete HTML document with the escaped user content inserted.
    """
    # Escape special characters to prevent injection attacks (CWE-74).
    safe_content = html.escape(page_content, quote=True)
    # Render the template with the escaped content.
    return html_template.format(user_content=safe_content)