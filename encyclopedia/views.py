from dataclasses import fields
from random import choice
from turtle import title
from django.shortcuts import render
from django import forms
from . import util
from django.core.files.storage import default_storage
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown # For markdown language
# TODO on 11th May 2022: FIX SEARCH and EDIT functions, if available throw exceptions as well
class NewEntryForm(forms.Form):
    # label is like placeholder, remember to import forms from django
    title = forms.CharField(label="New encyclopedia title")
    entry = forms.CharField(label="New encyclopedia entry")

class SearchForm(forms.Form):
    title = forms.CharField(label="Search in this encyclopedia!")

class EditForm(forms.Form):
    title = forms.CharField(label="Enter existing encyclopedia title")
    entry = forms.CharField(label="Edit encyclopedia entry", widget=forms.Textarea)

def index(request):
    
    # if "entries" not in required.session:
    #    request.session["entries"] = []
    entries = util.list_entries()
    
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "form": SearchForm()
    })

def entryPage(request, title):
    entry = util.get_entry(title)
    if entry is None:
        error_msg = "The entry does not exist!"
        return render(request, "encyclopedia/notfound.html", {
            "form": SearchForm(),
            "title": title,
            "error_msg": error_msg
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "form": SearchForm(),
            "entry": markdown.markdown(entry),
            "title": title
        })


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            # for this function just make it simple, q for query
            entries = util.list_entries()
            data = form.cleaned_data.get("title")
            here = False
            for entry in entries:
                if data.lower() == entry.lower():
                    content_md = util.get_entry(data)
                    content_html = markdown.markdown(content_md)
                    here = True
                    break
                                   
                    """title = entry
                    content_md = markdown.markdown(util.get_entry(title)) """
            if here:
                return render(request, "encyclopedia/entry.html", {
                    "title": data,
                    "entry": content_html,
                    "form": form
                })
                    # return HttpResponseRedirect(reverse("entry", args=[title]))
            else:
                searches = [] # search_list is to show the results
                for entry in entries:
                    if data.lower() in entry.lower():
                        searches.append(entry)
            
            if len(searches) == 0:
                form = SearchForm()
                error_msg = data + "No matches"
                return render(request, "encyclopedia/notfound.html", {
                    "title": data,
                    "error_msg": error_msg} )
            
            else:
                return render(request,"encyclopedia/index.html", {
                    
                    "form": form,
                    "entries": searches   
                })
        
    else:
        search_msg = "Let's search!"
        return render(request, "encyclopedia/index.html", {
            "form": SearchForm(),
            "title": "",
            "error_msg": search_msg    
            })
        
    """if request.method == "GET":
        query = markdown.markdown(request.GET.get("q"))
        entries = util.list_entries()
        searches = []
        
        for entry in entries:
            if query.lower() in entry.lower():
                searches.append(entry)
        
        for entry in entries:
            if query.lower() == entry.lower():
                return render(request, "encyclopeda/entry.html", {
                    "title": entry
                })
            elif searches != []:
                return render(request, "encyclopedia.html", {
                    "searches": searches
                })
            else: 
                return render(request, "encyclopedia/notfound.html", {
                    "title": query
                })"""
                
            #if query_md.lower() == entry.lower():
            #    return render(request, "encyclopedia/entry.html", {
            #    "title": query,
            #    "entry": entry        
            #    }) 
                
"""elif search_list != []:
                return render(request, "encyclopedia/search.html", {
                    "entries": search_list
                }) 
                
            else:
                return render(request, "encyclopedia/notfound.html", {
                    "title": query
                })"""
        
            
def newPage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["entry"]
            entries = util.list_entries()
            # title_md = markdown.markdown(title)
            
            for entry in entries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/newPage.html", {
                        "form": SearchForm(),
                        "newEntryForm": NewEntryForm(),
                        "error_message": "The entry is already existed!"
                    })
            
            new_entry = "# " + title
            new_content = "\n " + content        
            new_entry_content = new_entry + new_content
            util.save_entry(title, new_entry_content)
            entry_saved = util.get_entry(title)
            return render(request, "encyclopedia/entry.html", {
                "form": SearchForm(),
                "title" : title,
                "entry": markdown.markdown(entry_saved)

            })
        
    else:
        request.method == "GET"
        form = SearchForm()
        return render(request, "encyclopedia/newPage.html", {
            "form": form,
            "newEntryForm": NewEntryForm()
        })
    

def edit(request, title):
    if request.method == "POST":
        entry = util.get_entry(title)
        editForm = EditForm(initial={'title': title, 'entry': entry})
        return render(request, "encyclopedia/edit.html", {
            "form": SearchForm(),
            "editForm": editForm,
            "title": title,
            "entry": entry
        })


        #form = EditForm(request.POST)
        #if form.is_valid():
            #title_edited = form.cleaned_data.get("title")
            #entry_edited = form.cleaned_data.get("entry")
        ##   entry_edited = form.cleaned_data["entry"]
            
        #    util.save_entry(title_edited, entry_edited)
            
        #    entry = util.get_entry(entry_edited)
            
        #    return render(request, "encyclopedia/entry.html", {
        #        "form": SearchForm(),
        #        "title": title_edited,
        #        "entries": markdown.markdown(entry)
        #    })
    #else:
    #    request.method == "GET"
    #    return render(request, "encyclopedia/edit.html", {
    #        "form": SearchForm(),
    #        "editForm": EditForm({"title": title, "entry": util.get_entry(title)})
    #    })
        
            #lists = util.list_entries()
#title_md = markdown.markdown(title)
"""util.save_entry(title, entry)
            
            for list in lists:
                if title.lower() == list.lower():
                    return render
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": entry
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "form": form,
                "editForm": EditForm()
            })"""
def save(request, title):
    if request.method == "POST":
        # Extract information from form
        form = EditForm(request.POST)
        if form.is_valid():
            entry_edited = form.cleaned_data["entry"]
            title_edited = form.cleaned_data["title"]
            if title_edited != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            util.save_entry(title_edited, entry_edited)
            entry = util.get_entry(title_edited)

        return render(request, "encyclopedia/entry.html", {
            "title": title_edited,
            "entry": markdown.markdown(entry),
            "form": SearchForm(),

        })            

def randomPage(request):
    title = choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title": title
        
    })
    #return HttpResponseRedirect(reverse("entryPage", args=[title]))
    #return entryPage(request, )
    # return HttpResponseRedirect(reverse("entry", args=[title]))