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
    Return an HTML page with the visitor's message safely inserted.

    Parameters
    ----------
    visitor_message : str
        Content contributed by the user.

    Returns
    -------
    str
        The final HTML string with the message embedded.
    """
    # Escape any special HTML characters to prevent injection attacks
    safe_content = html.escape(visitor_message, quote=True)
    return html_template.format(user_content=safe_content)