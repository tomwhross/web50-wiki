import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


class NewEntryForm(forms.Form):
    """ Form for new wiki entries """

    title = forms.CharField()
    markdown = forms.CharField(widget=forms.Textarea)


def index(request):

    search_entry = request.GET.get("q", None)

    if search_entry:
        entry_markdown = util.get_entry(search_entry)
        if entry_markdown:
            return HttpResponseRedirect(reverse("view_entry", args=(search_entry,)))

        all_entries = util.list_entries()

        search_results = []
        for entry in all_entries:
            if search_entry.lower() in entry.lower():
                search_results.append(entry)

        return render(
            request,
            "encyclopedia/search_results.html",
            {"query": search_entry, "entries": search_results},
        )

    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def view_entry(request, entry):
    entry_markdown = util.get_entry(entry)

    if not entry_markdown:
        return render(request, "encyclopedia/not_found.html", {"entry_title": entry})

    entry_html = markdown2.markdown(entry_markdown)
    return render(
        request,
        "encyclopedia/entry.html",
        {
            "entry_title": entry,
            "entry_body": entry_html,
        },
    )


def create_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]

            markdown = form.cleaned_data["markdown"]

            if util.get_entry(title):
                return render(
                    request,
                    "encyclopedia/create_entry_error.html",
                    {"entry": title},
                )

            util.save_entry(title, markdown)
            return HttpResponseRedirect(reverse("view_entry", args=(title,)))

    return render(request, "encyclopedia/create_entry.html", {"form": NewEntryForm()})
