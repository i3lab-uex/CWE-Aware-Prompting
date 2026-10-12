import html

# Default HTML template with a placeholder for user content.
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
    Construct an HTML page by safely inserting user-provided content.

    Args:
        page_content: The raw string supplied by the user to be embedded in the page.

    Returns:
        A complete HTML document as a string with the user content properly escaped.
    """
    # Escape special HTML characters to prevent injection attacks.
    safe_content = html.escape(page_content, quote=True)
    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)