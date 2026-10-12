import html

# Example template; replace or modify as needed.
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
    Build a complete HTML page by safely inserting user-provided content
    into a predefined template.

    Parameters
    ----------
    page_content : str
        Raw content supplied by the user. It may contain HTML special
        characters that must be escaped to prevent XSS or malformed markup.

    Returns
    -------
    str
        A full HTML document with the escaped user content inserted.
    """
    # Escape special characters to avoid injection attacks
    safe_content = html.escape(page_content, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)