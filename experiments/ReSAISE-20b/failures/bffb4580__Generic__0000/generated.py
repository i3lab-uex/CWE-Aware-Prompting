import html

# Base HTML template with a placeholder for user-provided content.
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
    Construct an HTML page embedding the user-provided string in a safe manner.

    Parameters
    ----------
    client_input : str
        Content supplied by the user that will be inserted into the page.

    Returns
    -------
    str
        The complete HTML page with the user content escaped to prevent
        cross‑site scripting (XSS) attacks.
    """
    # Escape special HTML characters to avoid script injection
    safe_input = html.escape(client_input, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_input)