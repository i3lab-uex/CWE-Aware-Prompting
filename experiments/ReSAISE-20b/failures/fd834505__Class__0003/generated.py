import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Output</title>
</head>
<body>
    <h1>User Submitted Content</h1>
    <div id="content">{user_content}</div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Safely embed user-provided content into an HTML template.

    Parameters
    ----------
    user_input : str
        The raw string provided by the user. It may contain characters that
        need to be escaped (e.g., <, >, &, ", ').

    Returns
    -------
    str
        The final HTML string with the user content properly escaped to
        prevent injection attacks such as cross‑site scripting (XSS).

    Notes
    -----
    The function uses `html.escape` to neutralize special HTML characters.
    No other transformations are performed, so the output remains
    deterministic and safe for inclusion in an HTML document.
    """
    # Escape special characters to avoid injection vulnerabilities
    safe_content = html.escape(user_input, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)