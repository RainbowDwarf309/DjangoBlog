from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category
from django.db.models import F


class Home(ListView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Django Blog'
        return context
