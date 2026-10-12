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
        The raw content contributed by a user. It may contain characters that need to be escaped.

    Returns
    -------
    str
        The final HTML string with the user's content inserted in place of {user_content}.
    """
    # Escape user input to prevent XSS and ensure the HTML remains well-formed.
    safe_content = html.escape(visitor_message, quote=True)
    return html_template.format(user_content=safe_content)

# Example usage:
if __name__ == "__main__":
    message = '<script>alert("XSS")</script>'
    print(render_html_page(message))