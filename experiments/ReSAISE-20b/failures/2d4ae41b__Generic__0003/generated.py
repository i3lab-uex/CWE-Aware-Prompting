import html

# Example HTML template with a placeholder for user content.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Message</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div class="message">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_page(visitor_message: str, html_template: str = HTML_TEMPLATE) -> str:
    """
    Return an HTML page with the user's message safely embedded.

    Parameters
    ----------
    visitor_message : str
        Content supplied by the user.
    html_template : str, optional
        The HTML template containing a `{user_content}` placeholder.

    Returns
    -------
    str
        The final HTML string with the escaped user content.
    """
    # Escape special HTML characters to prevent XSS attacks.
    safe_content = html.escape(visitor_message, quote=True)
    return html_template.format(user_content=safe_content)