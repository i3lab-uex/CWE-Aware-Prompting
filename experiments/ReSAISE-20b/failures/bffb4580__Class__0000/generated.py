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
    Construct an HTML page embedding the user-provided input safely.

    Parameters
    ----------
    client_input : str
        The raw content supplied by the user that will be inserted into the page.

    Returns
    -------
    str
        The complete HTML document with the user input escaped to prevent
        injection of malicious markup or scripts.

    Notes
    -----
    - The function uses `html.escape` to neutralize special characters such as
      `<`, `>`, `&`, `"`, and `'`. This protects against CWE-74
      (Improper Neutralization of Special Elements in Output).
    - No exceptions are raised; malformed input is simply escaped.
    """
    # Escape the user input to neutralize any HTML special characters
    safe_input = html.escape(client_input, quote=True)

    # Render the final HTML by inserting the escaped content
    return html_template.format(user_content=safe_input)