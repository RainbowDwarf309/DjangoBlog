from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Post, Category, Tag, Comment, FavoriteCategory, ActionTrack
from .forms import CreatePostForm
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import CommentSubmitForm
from django.shortcuts import render, reverse, redirect
from services.functions import track_action, get_top_contributors_for_all_time, get_top_contributors_for_last_month


class HomeView(ListView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(is_published=True, status='APPROVED').select_related('category', 'author'). \
            prefetch_related('tags')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Django Blog'
        return context


class CategoriesListView(ListView):
    model = Category
    template_name = 'news/categories_list.html'
    context_object_name = 'categories'

    def get_favorites(self) -> list:
        """if user is not anonymous, then checks category in favorite and returns list of categories"""
        objects_list = []
        if not self.request.user.is_anonymous:
            favorites = FavoriteCategory.objects.filter(user=self.request.user)
            for fav in favorites:
                objects_list.append(fav.obj)
            return objects_list
        return objects_list


    def get_queryset(self):
        return Category.objects.filter(photo__isnull=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = self.get_favorites()
        context['title'] = 'Categories'
        return context


class SinglePostView(FormMixin, DetailView):
    model = Post
    template_name = 'news/single_post.html'
    context_object_name = 'post'
    form_class = CommentSubmitForm

    def is_favorite(self) -> bool:
        """if user is not anonymous, then checks post in favorite and returns True or False"""
        if not self.request.user.is_anonymous:
            return self.request.user.favoritepost.filter(obj=self.get_object()).exists()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_favorite'] = self.is_favorite()
        context['comments_count'] = Comment.objects.filter(post=Post.objects.select_related('author__userprofile').
                                                           get(slug=self.kwargs['slug'])).count()
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
    allow_empty = True

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
    allow_empty = True

    def get_queryset(self):
        return Post.objects.filter(tags=Tag.objects.get(slug=self.kwargs['slug']),
                                   is_published=True).select_related('category').prefetch_related('tags')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByAuthorView(ListView):
    template_name = 'news/authors_posts.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = True

    def get_queryset(self):
        return Post.objects.filter(author=User.objects.get(pk=self.kwargs['pk']),
                                   is_published=True).select_related('category', 'author').prefetch_related('tags')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        context['author'] = user
        context['title'] = user.username
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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.photo = form.cleaned_data['photo']
            new_post.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class SearchPostView(ListView):
    template_name = 'news/search_posts.html'
    context_object_name = 'posts'
    allow_empty = True
    ordering = '-created_at'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        return context

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        queryset = Post.objects.filter(Q(title__icontains=search_query) | Q(author__username__icontains=search_query)).\
            select_related('author').prefetch_related('tags').exclude(is_published=False).order_by(self.ordering)
        return queryset


class CommunityView(TemplateView):
    template_name = 'news/community.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_contributors'] = get_top_contributors_for_all_time()
        context['month_contributors'] = get_top_contributors_for_last_month()
        track_action(self.request, page=ActionTrack.AttrPage.PAGE_COMMUNITY, action=ActionTrack.AttrAction.VIEW)
        return context
