from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Post, Category, Tag, Comment
from .forms import CreatePostForm
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.db.models import F, Q
from .forms import CommentSubmitForm


class HomeView(ListView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('category').prefetch_related('tags')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Django Blog'
        return context


class SinglePostView(FormMixin, DetailView):
    model = Post
    template_name = 'news/single_post.html'
    context_object_name = 'post'
    form_class = CommentSubmitForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['comments'] = Comment.objects.exclude(status=Comment.AttrStatus.INVISIBLE). \
            select_related('post', 'user_submitter__userprofile', 'parent'). \
            filter(post=Post.objects.select_related('author__userprofile').get(slug=self.kwargs['slug']))
        context['form'] = self.form_class(initial={'post': Post.objects.select_related('author__userprofile').
                                          get(slug=self.kwargs['slug'])})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            new_comment = form.save(commit=False)
            new_comment.user_submitter = self.request.user
            new_comment.text = form.cleaned_data['text']
            new_comment.save()
            return HttpResponseRedirect(reverse("post", kwargs={'slug': self.object.slug}))
        else:
            return HttpResponseRedirect(reverse("login"))


class PostsByCategoryView(ListView):
    template_name = 'news/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category=Category.objects.get(slug=self.kwargs['slug']),
                                   is_published=True).select_related('category').prefetch_related('tags')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTagView(ListView):
    template_name = 'news/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags=Tag.objects.get(slug=self.kwargs['slug']),
                                   is_published=True).select_related('category').prefetch_related('tags')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


@method_decorator(login_required, name='dispatch')
class CreatePostView(CreateView):
    form_class = CreatePostForm
    template_name = 'news/create_post.html'
    context_object_name = 'news'

    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Django Blog'
        context['form'] = self.form_class(initial={'author': self.request.user})
        return context


class SearchPostView(ListView):
    template_name = 'news/search_posts.html'
    context_object_name = 'posts'
    allow_empty = True
    ordering = '-created_at'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        return context

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        queryset = Post.objects.filter(Q(title__icontains=search_query) | Q(author__username__icontains=search_query)).\
            prefetch_related('tags').exclude(is_published=False).order_by(self.ordering)
        return queryset
