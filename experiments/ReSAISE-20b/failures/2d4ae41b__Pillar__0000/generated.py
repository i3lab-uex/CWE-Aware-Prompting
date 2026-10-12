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
    <h1>Welcome!</h1>
    <div id="message">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_page(visitor_message: str) -> str:
    """
    Render an HTML page with the visitor's message safely inserted.

    Parameters
    ----------
    visitor_message : str
        The content contributed by a user. It will be escaped to prevent XSS.

    Returns
    -------
    str
        The final HTML string with the user's content embedded.
    """
    # Escape special HTML characters to prevent injection attacks.
    safe_message = html.escape(visitor_message, quote=True)
    # Insert the escaped message into the template.
    return html_template.format(user_content=safe_message)