from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import random
import os


markdowner = Markdown()

class SearchForm(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))
    
class NewForm(forms.Form):
    title = forms.CharField(label='Title')
    text = forms.CharField(label='Text', widget=forms.Textarea())

class EditForm(forms.Form):
    edit = forms.CharField(label='Text', initial='wtf', widget=forms.Textarea()) 


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
        "form": SearchForm()
    })

def search(request):
        entries = util.list_entries()
        lowerCaseEntries = [x.lower() for x in util.list_entries()]
        q = (request.GET["q"]).lower()
        if q in lowerCaseEntries:
            return HttpResponseRedirect("/wiki/" + q)
        else:
            foundEntry = []
            for i in range(len(entries)):
                if q in lowerCaseEntries[i]:
                    foundEntry.append(entries[i])
            if len(foundEntry) > 0:
                print(foundEntry)
                return render(request, "encyclopedia/search.html", {
                    "entries": foundEntry, 
                    "form": SearchForm()
                })
            else: 
                return render(request, "encyclopedia/error.html",{
                "error": "No results, try again!", 
                "form": SearchForm()  
                })

def entry(request, entry):
    if util.get_entry(entry):
        content = markdowner.convert(util.get_entry(entry))
        return render(request, "encyclopedia/entry.html",{
        "content": content, 
        "form": SearchForm(), 
        "title" : entry
        })
    else:
        return render(request, "encyclopedia/error.html",{
        "error": "Entry not found, try searching!", 
        "form": SearchForm() 
        })
    
def new(request):  
    if request.method == "POST":
        form = NewForm(request.POST)
        print(form)
        if form.is_valid():
            lowerCaseEntries = [x.lower() for x in util.list_entries()]
            if form.cleaned_data["title"].lower() in lowerCaseEntries:
                return render(request, "encyclopedia/error.html",{
                "error": "Page already exists!", 
                "form": SearchForm()  
                })
            else:
                util.save_entry(form.cleaned_data["title"],form.cleaned_data['text'])
                return HttpResponseRedirect("/wiki/" + form.cleaned_data["title"])
  
    else:     
        return render(request, "encyclopedia/new.html", {
        "form": SearchForm(),  
        "newForm": NewForm()
        })


def edit(request, page):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data
            util.save_entry(page, content['edit'])
            print("from edit POST" )
            print(content)
            return HttpResponseRedirect("/wiki/" + page)
    else:    
        with open(os.path.join('entries/', page + ".md"), "r") as file1:
            txtToEdit = file1.read()
            formForEdit = EditForm(initial={'edit': txtToEdit})
            print("formForEdit")
            print(formForEdit)

            return render(request, "encyclopedia/edit.html", {
                "editForm" : formForEdit, 
                "title" : page, 
                "form": SearchForm(),  
            })


def random_page(request):
    entries = util.list_entries()
    randomize = random.randint(0,len(entries))

    return HttpResponseRedirect("/wiki/" + entries[randomize])