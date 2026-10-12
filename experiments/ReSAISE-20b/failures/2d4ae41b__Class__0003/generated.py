import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Message</title>
</head>
<body>
    <h1>Welcome Visitor!</h1>
    <div id="message">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_page(visitor_message: str) -> str:
    """
    Render an HTML page with the visitor's message safely embedded.

    Parameters
    ----------
    visitor_message : str
        The raw text supplied by the user to be displayed in the page.

    Returns
    -------
    str
        A complete HTML document with the user's message inserted and properly escaped.
    """
    # Escape any special HTML characters to prevent injection attacks (CWE-74).
    safe_content = html.escape(visitor_message, quote=True)
    return html_template.format(user_content=safe_content)