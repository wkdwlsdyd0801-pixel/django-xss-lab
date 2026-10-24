from django import forms


class PostForm(forms.Form):
    """New post input. Validation here checks format only.

    It deliberately does NOT strip or escape HTML: cleaning input is one valid
    defence, but this lab defends at OUTPUT time (escaping + CSP) so the stored
    data stays exactly as sent and the two render modes can be compared.
    """

    author = forms.CharField(label="작성자", max_length=50)
    content = forms.CharField(label="내용", widget=forms.Textarea, max_length=2000)
