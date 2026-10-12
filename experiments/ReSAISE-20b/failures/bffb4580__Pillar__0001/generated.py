import html

# Base HTML template with a placeholder for user content.
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
    Construct an HTML page embedding the user-provided content safely.

    Parameters
    ----------
    client_input : str
        The raw input string supplied by the user.

    Returns
    -------
    str
        A fully formed HTML document with the escaped user content inserted.

    Notes
    -----
    The function uses :func:`html.escape` to neutralize any HTML or JavaScript
    that might otherwise be executed in the browser, mitigating
    CWE-707 and other injection vulnerabilities.
    """
    # Escape special HTML characters to prevent script injection.
    safe_content = html.escape(client_input, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)