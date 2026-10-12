import html

# The base HTML template containing a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Message</title>
</head>
<body>
    <h1>Welcome Visitor!</h1>
    <p>{user_content}</p>
</body>
</html>
"""

def render_html_page(visitor_message: str) -> str:
    """
    Render an HTML page with the visitor's message safely inserted.

    Parameters
    ----------
    visitor_message : str
        The content contributed by a user which will be inserted into the HTML template.

    Returns
    -------
    str
        The resulting HTML string with the user’s content embedded.
    """
    # Escape the visitor message to prevent XSS and other HTML injection issues
    safe_message = html.escape(visitor_message, quote=True)
    return html_template.format(user_content=safe_message)