import html

# Example template containing a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Message</title>
</head>
<body>
    <h1>Hello, Visitor!</h1>
    <p>{user_content}</p>
</body>
</html>
"""

def render_html_page(visitor_message: str) -> str:
    """
    Render an HTML page with the visitor's message safely embedded.

    Parameters
    ----------
    visitor_message : str
        The user-provided content to be inserted into the page.

    Returns
    -------
    str
        The complete HTML string with the escaped user content.
    """
    # Escape any potentially dangerous characters to prevent XSS attacks.
    safe_content = html.escape(visitor_message, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)