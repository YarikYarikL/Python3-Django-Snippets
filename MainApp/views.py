from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.models import Snippet
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    #создаем пустую форму при запросе методом GET
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'form': form,
            'pagename': 'Добавление нового сниппета'
            }
        return render(request, 'pages/add_snippet.html', context)
    #если форма заполнена, то получаем данные из формы и создаем новый сниппет в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("SnippetsList")
        return render(request, "pages/add_snippet.html", {"form": form})


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets
               }
    return render(request, 'pages/view_snippets.html', context)


def snippet_details(request, num):
    try:
        snippet = Snippet.objects.get(id=num)
    except ObjectDoesNotExist:
        context = {
            "pagename": 'Просмотр сниппета',
            "ErrorText":f'Сниппет с id {num} не существует.'
        }
        return render(request, "pages/error_page.html", context)
    else:
        snippet = Snippet.objects.get(id=num)
        context = {
            "pagename": 'Просмотр сниппета',
            "snippet": snippet
                   }
        return render(request,'pages/snippet_details.html',context)

def snippet_edit(request, num):
    context ={
        "pagename":"Редактирование сниппета"
    }
    try:
        snippet = Snippet.objects.get(id=num)
    except ObjectDoesNotExist:
        return Http404
    #хотим получить страницу с данными сниппета
    if request.method == "GET":
        context = {
            'snippet': snippet,
            'type': 'edit',
            }
        return render(request, 'pages/snippet_details.html', context)
    #если форма заполнена, то получаем данные из формы и создаем новый сниппет в БД
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        print(f'{data_form["creation_date"]=}')
        # snippet.creation_date = data_form["creation_date"]
        snippet.save()
        return redirect("SnippetsList")    



def snippet_delete(request, num):
    if request.method == "POST" or request.method == "GET":
        snippet = get_object_or_404(Snippet, id=num)
        snippet.delete()
    return redirect("SnippetsList")