from django.shortcuts import redirect


def view_404(request, exception):

    return redirect("docs")
