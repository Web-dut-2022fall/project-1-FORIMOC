from random import randint
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_md = util.get_entry(title)
    if entry_md == None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found."})
    else:
        entry_html = Markdown().convert(entry_md)
        context = {
            "title": title,
            "entry": entry_html
        }
        return render(request, "encyclopedia/entry.html", context)

def search(request):
    word = request.POST.get('q')
    if not word:
        return HttpResponseRedirect(reverse("index"))
    entry_list = util.list_entries()
    entries = []
    if word in entry_list:
        return HttpResponseRedirect(reverse("entry", args=(word,)))
    else:
        for entry in entry_list:
            if entry.find(word) != -1:
                entries.append(entry)
        context = {
            "entries": entries
        }
        return render(request, "encyclopedia/search.html", context)

def create(request):
    if request.method=='GET':
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not title:
            return render(request, "encyclopedia/error.html", {"message": "Please input title!"})
        elif title in util.list_entries():
            return render(request, "encyclopedia/error.html", {"message": "Page already exists!"})
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=(title,)))

def edit(request, title):
    entry_md = util.get_entry(title)
    if entry_md == None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found."})
    elif request.method=='GET':
        # entry_html = Markdown().convert(entry_md)
        context = {
            "title": title,
            "entry": entry_md
        }
        return render(request, "encyclopedia/edit.html", context)
    else:
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=(title,)))

def random(request):
    entry_list = util.list_entries()
    num = randint(0, len(entry_list)-1)
    return HttpResponseRedirect(reverse("entry", args=(entry_list[num],)))
