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
    Render an HTML page by safely inserting the visitor's message into
    a predefined template.

    Parameters:
        visitor_message (str): Content contributed by the user.

    Returns:
        str: The final HTML string with the user's content embedded.
    """
    # Escape special HTML characters to prevent injection (CWE‑74).
    safe_content = html.escape(visitor_message, quote=True)
    return html_template.format(user_content=safe_content)