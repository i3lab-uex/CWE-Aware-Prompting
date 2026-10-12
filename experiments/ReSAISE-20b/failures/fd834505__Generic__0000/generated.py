import html

def render_html_output(user_input: str) -> str:
    """
    Construct an HTML response by safely inserting user-provided content into a predefined template.

    Parameters
    ----------
    user_input : str
        Content supplied by the user that will be embedded in the HTML response.

    Returns
    -------
    str
        The complete HTML page with the user content safely escaped to prevent script injection.

    Notes
    -----
    The function uses :func:`html.escape` to neutralize any HTML special characters
    in the user input. This prevents malicious scripts from being executed when the
    resulting page is rendered by a browser.
    """
    # Predefined HTML template with a placeholder for user content
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Safe User Content</title>
<style>
    body {font-family: Arial, sans-serif; margin: 2rem;}
    .content {border: 1px solid #ccc; padding: 1rem; background:#f9f9f9;}
</style>
</head>
<body>
<h1>Welcome!</h1>
<div class="content">
    {user_content}
</div>
</body>
</html>
"""

    # Escape the user input to avoid XSS
    safe_content = html.escape(user_input, quote=True)

    # Return the final HTML with the escaped content inserted
    return html_template.format(user_content=safe_content)