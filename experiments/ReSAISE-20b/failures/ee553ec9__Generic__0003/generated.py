import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Message</title>
</head>
<body>
    <h1>Message Received:</h1>
    <p>{user_content}</p>
</body>
</html>
"""

def build_html_output(client_message: str) -> str:
    """
    Build an HTML page that safely embeds the client's message.

    Parameters
    ----------
    client_message : str
        The content contributed by a user. It will be escaped to prevent
        XSS or other injection attacks.

    Returns
    -------
    str
        The complete HTML string with the user's content inserted.
    """
    # Escape user-provided content to ensure it is safe for HTML rendering.
    escaped_message = html.escape(client_message, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=escaped_message)