import html

# HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Page</title>
</head>
<body>
    {user_content}
</body>
</html>
"""

def build_html_page(page_content: str) -> str:
    """
    Build a complete HTML page by safely injecting user-provided content
    into the predefined template.

    Parameters:
        page_content (str): The dynamic content supplied by the user.

    Returns:
        str: A fully formed HTML string with the user content escaped.
    """
    # Escape special characters to prevent injection attacks (CWE-707).
    safe_content = html.escape(page_content, quote=True)

    # Format the template with the escaped content.
    return html_template.format(user_content=safe_content)