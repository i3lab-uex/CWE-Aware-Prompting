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
    Construct an HTML page embedding the given client input safely.

    Parameters
    ----------
    client_input : str
        Content supplied by the user that will be inserted into the page.

    Returns
    -------
    str
        The complete HTML page with the user content safely escaped.
    """
    # Escape special HTML characters to prevent injection attacks
    safe_content = html.escape(client_input, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)