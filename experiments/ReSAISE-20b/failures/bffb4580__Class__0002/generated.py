import html

# Predefined HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe User Page</title>
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
        The raw string supplied by the user to be inserted into the page.

    Returns
    -------
    str
        The complete HTML document with the user content escaped to prevent
        script injection or other HTML-based attacks.

    Notes
    -----
    - Uses html.escape to neutralize special characters (<, >, &, ", ').
    - No exceptions are raised; malformed input is simply escaped.
    """
    # Escape user input to avoid HTML injection (CWE-74).
    safe_content = html.escape(client_input, quote=True)

    # Format the template with the escaped content.
    return html_template.format(user_content=safe_content)