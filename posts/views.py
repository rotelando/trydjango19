from urllib import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Post
from .forms import PostForm


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully created")
        return redirect("posts:list")

    context = {
        "form": form,
        "title": "create"
    }
    return render(request, 'post_create.html', context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    context = {
        "instance": instance,
        "title": "detail",
        "share_string": share_string,
    }
    return render(request, 'post_detail.html', context)


def post_list(request):
    queryset_list = Post.objects.all()
    page_request_var = 'page'
    paginator = Paginator(queryset_list, 10)  # Show 25 contacts per page

    page = request.GET.get(page_request_var)
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        querysets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        querysets = paginator.page(paginator.num_pages)
    context = {
        "querysets": querysets,
        "title": "detail",
        "page_request_var": page_request_var
    }
    return render(request, 'index.html', context)


def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully updated!")
        return redirect("posts:list")

    context = {
        "form": form,
        "title": "create"
    }
    return render(request, 'post_create.html', context)


def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")