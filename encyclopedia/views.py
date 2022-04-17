from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from . import util
import random
import markdown2

class NewEntryForm(forms.Form):
    title = forms.CharField(label='title')
    entry = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), label='entry')

initial = "Initially, this message should be inside the teaxtarea of the form"

class EditForm(forms.Form):
    title = forms.CharField(label='title')
    entry = forms.CharField(initial=f'{initial}', widget=forms.Textarea(attrs={'class': 'textarea'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def update(request):
    #User has Submitted a new entry
    if request.method == "POST":
        entry = request.POST["entry"]
        title = request.POST["title"]

        #save entry
        util.save_entry(title, entry)
        return HttpResponseRedirect(f"/wiki/{ title }")

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
        })

    #User has Submitted a new entry
    if request.method == "POST":
        entry = request.POST["entry"]
        title = request.POST["title"]
        exists = util.get_entry(title)

        #Check if entry already exists
        if exists != None:
            return render(request, "encyclopedia/exists.html", {
                "title": title
            })

        #save entry
        util.save_entry(title, entry)
        return HttpResponseRedirect(f"/wiki/{ title }")

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/noentry.html", {
            "title": title
        })

    return render(request, 'encyclopedia/entry.html', {
        "title": title,
        "entry": markdown2.markdown(entry)
    })

def random_entry(request):
    entries = util.list_entries()
    range = len(entries)
    num = random.randrange(0, range)
    entry = util.get_entry(entries[num])
    return render(request, 'encyclopedia/random.html', {
        "entry": markdown2.markdown(entry)
    })

def edit(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")

    if request.method == "POST":
        title = request.POST["title"]
        initial = util.get_entry(request.POST["title"])
        if initial == None:
            initial = "Create Your Entry Here"
        return render(request, 'encyclopedia/edit.html', {
            "entry": initial, 
            "title": title,
            "form": EditForm()
    })

def search(request):

    #User submits search
    if request.method == "POST":
        title = request.POST["q"]

        #lookup exact word
        entry = util.get_entry(title)

        #If found, redirect to that page
        if entry != None:
            return HttpResponseRedirect(f"/wiki/{ title }")

        #If no exact match, find and display partial matches
        all_entries = util.list_entries()
        matches = []

        for one in all_entries:
            if title in one:
                matches.append(one)
        
        return render(request, 'encyclopedia/results.html', {
            "matches": matches,
            "q": title
        })

    #User just wants the page(No search)
    if request.method == "GET":
        return render(request, "encyclopedia/search.html")

def test(request):
    return render(request, "encyclopedia/test.html", {
        "form": NewEntryForm()
    })