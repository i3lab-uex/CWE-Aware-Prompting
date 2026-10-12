import html

# Example HTML template with a placeholder for user content.
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
    Build a complete HTML page by inserting escaped user content into the template.

    Parameters
    ----------
    page_content : str
        The raw content supplied by the user. It may contain characters that need to be escaped.

    Returns
    -------
    str
        The final HTML string with the user content safely escaped.
    """
    # Escape special characters to prevent XSS or template injection
    safe_content = html.escape(page_content, quote=True)

    # Render the final page
    return html_template.format(user_content=safe_content)