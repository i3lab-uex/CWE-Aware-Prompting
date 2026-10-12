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
    <p>{user_content}</p>
</body>
</html>
"""

def render_html_page(visitor_message: str) -> str:
    """
    Generate an HTML page by safely inserting the visitor's message into
    a predefined template.

    Parameters:
        visitor_message (str): Content contributed by the user.

    Returns:
        str: The resulting HTML string with the user's content embedded.
    """
    # Escape user-provided content to prevent XSS and other injection attacks.
    safe_content = html.escape(visitor_message, quote=True)
    return html_template.format(user_content=safe_content)

# Example usage:
if __name__ == "__main__":
    user_msg = '<script>alert("XSS")</script>'
    print(render_html_page(user_msg))