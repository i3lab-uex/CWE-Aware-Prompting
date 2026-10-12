import html

# Example HTML template containing a placeholder for user content.
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
    Build a complete HTML page by inserting escaped user-provided content
    into the predefined template.

    Parameters:
        page_content (str): The raw user-supplied content to embed in the page.

    Returns:
        str: A fully formed HTML string with user content safely escaped.
    """
    # Escape any special HTML characters to prevent injection attacks.
    safe_content = html.escape(page_content, quote=True)

    # Inject the escaped content into the template.
    return html_template.format(user_content=safe_content)