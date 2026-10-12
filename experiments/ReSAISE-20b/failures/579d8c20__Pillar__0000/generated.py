import html

# Example base template that contains a placeholder for user content.
# In practice this could be read from a file or defined elsewhere.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Page</title>
</head>
<body>
    <h1>Welcome to the Visitor Page</h1>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_response(visitor_content: str) -> str:
    """
    Construct an HTML page that safely embeds user-provided content.

    Parameters
    ----------
    visitor_content : str
        Raw text supplied by a user that should appear within the HTML page.

    Returns
    -------
    str
        The complete HTML document with the user content inserted, escaped to
        prevent script injection attacks.

    Notes
    -----
    - The function uses ``html.escape`` to neutralize any characters that could be
      interpreted as markup or script.  This mitigates the risk of CWE-707 (improper
      neutralization) and common XSS vulnerabilities.
    - No external libraries are required beyond the standard library.
    """
    # Escape special HTML characters to avoid injection.
    safe_content = html.escape(visitor_content, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)