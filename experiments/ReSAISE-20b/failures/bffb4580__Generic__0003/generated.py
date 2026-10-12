import html

# Predefined HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def build_html_page(client_input: str) -> str:
    """
    Construct an HTML page embedding the provided user input safely.

    Parameters
    ----------
    client_input : str
        Content supplied by the user that should be inserted into the page.

    Returns
    -------
    str
        The complete HTML document with user content safely escaped.
    """
    if not isinstance(client_input, str):
        raise TypeError("client_input must be a string")

    # Escape any HTML special characters to prevent script injection.
    safe_content = html.escape(client_input, quote=True)

    # Format the template with the escaped content.
    return html_template.format(user_content=safe_content)