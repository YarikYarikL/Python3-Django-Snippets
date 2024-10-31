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
    #если форма заполненаЁ то получаем данные из формы и создаем новый сниппет в БД
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
        single_snippet = Snippet.objects.get(id=num)
    except ObjectDoesNotExist:
        context = {
            "pagename": 'Просмотр сниппета',
            "ErrorText":f'Сниппет с id {num} не существует.'
        }
        return render(request, "pages/error_page.html", context)
    else:
        single_snippet = Snippet.objects.get(id=num)
        context = {
            "pagename": 'Просмотр сниппета',
            "single_snippet": single_snippet
                   }
        return render(request,'pages/snippet_details.html',context)

def snippet_edit(request, num):
    pass

def snippet_delete(request, num):
    if request.method == "POST":
        snippet = get_object_or_404(Snippet, id=num)
        snippet.delete()
    return redirect("SnippetsList")