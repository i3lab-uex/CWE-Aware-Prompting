import html

# Predefined HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Output</title>
</head>
<body>
    <h1>User Content</h1>
    <div>{user_content}</div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Construct an HTML page by safely embedding the user-provided input into a
    predefined template.

    Parameters:
        user_input (str): Content supplied by the user that should appear in
                          the resulting HTML.

    Returns:
        str: A complete HTML document with the user content inserted in a
             safe manner (HTML-escaped to prevent injection).

    Notes:
        - The function uses `html.escape` to neutralize special characters,
          preventing cross‑site scripting (XSS) and other injection attacks.
        - No exceptions are raised; invalid input is handled gracefully
          by escaping it.
    """
    # Escape user content to avoid HTML injection.
    safe_content = html.escape(user_input, quote=True)

    # Render the final HTML by substituting the placeholder.
    return html_template.format(user_content=safe_content)