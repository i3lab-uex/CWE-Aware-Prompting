import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <p>{user_content}</p>
</body>
</html>
"""

def build_html_page(client_input: str) -> str:
    """
    Construct an HTML page embedding the user-provided content safely.

    Parameters
    ----------
    client_input : str
        Raw input from the user that should appear inside the HTML page.

    Returns
    -------
    str
        The full HTML document with the user content inserted.
        All special characters are escaped to prevent XSS attacks.

    Notes
    -----
    The function uses `html.escape` to convert characters such as
    `<`, `>`, and `&` into their corresponding HTML entities.
    This ensures that any attempt to inject scripts or malicious
    markup is neutralized.
    """
    # Escape the user input so that it cannot break out of the <p> element
    safe_content = html.escape(client_input, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)