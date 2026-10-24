"""
Board views for the XSS lab.

Two classic cross-site scripting (XSS) bugs are shown side by side, each with a
vulnerable mode and a safe mode selected by a ?mode= query parameter:

  - stored XSS   (board_view):  a <script> saved in a post runs for every visitor
  - reflected XSS (search_view): a <script> in the URL runs for whoever opens the link

The defence is the same idea in both: never print user input as raw HTML.
  1. OUTPUT ESCAPING - Django auto-escapes {{ value }}, turning < into &lt; so the
     browser shows the text instead of running it. The bug only appears when we
     opt OUT of that with the |safe filter / mark_safe().
  2. CSP (defence in depth) - safe mode also sends a Content-Security-Policy header
     that forbids inline scripts, so even a missed escape cannot execute.

WARNING: the vulnerable modes are intentionally insecure. Run this app locally only.
"""
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from .forms import PostForm
from .models import Post

# Safe mode sends this header. "script-src 'self'" means the browser will run
# scripts only from this site's own files, never an inline <script> injected
# into the page, so a missed escape still cannot execute attacker code.
CSP_HEADER = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"


def _apply_csp(response, mode):
    """Attach the CSP header in safe mode only, so the two modes can be compared."""
    if mode == "safe":
        response["Content-Security-Policy"] = CSP_HEADER
    return response


def board_view(request):
    """Stored XSS demo: list posts (GET) or save a new post (POST)."""
    # The clicked button / link carries the render mode: vulnerable or safe.
    mode = request.GET.get("mode", "safe")

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # Store the content verbatim. This write is NOT where XSS happens -
            # the danger is purely in how a template prints it back later.
            Post.objects.create(
                author=form.cleaned_data["author"],
                content=form.cleaned_data["content"],
            )
            # Redirect back to the same mode so a refresh does not re-submit.
            return redirect(f"{request.path}?mode={mode}")
    else:
        form = PostForm()

    posts = Post.objects.all().order_by("-id")

    # Pick the template by mode:
    #   vulnerable -> prints {{ post.content|safe }}  (escaping turned OFF -> script runs)
    #   safe       -> prints {{ post.content }}        (auto-escaped -> script shown as text)
    template = "board_vulnerable.html" if mode == "vulnerable" else "board_safe.html"

    response = render(request, template, {"form": form, "posts": posts, "mode": mode})
    return _apply_csp(response, mode)


def search_view(request):
    """Reflected XSS demo: echo the search term back to the page."""
    mode = request.GET.get("mode", "safe")
    query = request.GET.get("q", "")

    context = {"mode": mode, "query": query, "echo": query}

    if mode == "vulnerable":
        # mark_safe() tells the template "trust this, do not escape it", so the
        # raw ?q= value is written straight into the HTML. A link such as
        #   /myapp/search/?mode=vulnerable&q=<script>alert(1)</script>
        # runs the script in the victim's browser the moment they open it.
        context["echo"] = mark_safe(query)

    # In safe mode "echo" stays a plain string, so the template auto-escapes it
    # (< becomes &lt;) and the browser displays the tags as text.
    response = render(request, "search.html", context)
    return _apply_csp(response, mode)
