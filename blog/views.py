from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    RedirectView,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Category
from django.urls import reverse_lazy
from .forms import CreatePost
from django.http import HttpResponse

# imports related to api


class ShowPost(PermissionRequiredMixin, ListView):
    permission_required = "blog.view_post"
    template_name = "blog/blog.html"
    model = Post
    context_object_name = "all_posts"

    def get_ordering(self):
        order = self.request.GET.get("sort", "title")
        return [order]


class ShowPostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"


class ShowFormView(FormView):
    template_name = "blog/contact.html"
    form_class = CreatePost
    success_url = reverse_lazy("post")

    def form_valid(self, form):
        title = self.request.POST.get("title")
        content = self.request.POST.get("content")
        status = self.request.POST.get("status")
        post = Post()
        post.title = title
        post.content = content
        post.status = status
        post.author = get_user_model().objects.all()[0]
        post.category = Category.objects.all()[0]
        post.save()
        return super().form_valid(form)


class ShowCreateView(LoginRequiredMixin, CreateView):
    form_class = CreatePost
    model = Post
    template_name = "blog/contact.html"
    success_url = reverse_lazy("post")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            new_form = form.save(commit=False)
            user = self.request.user
            new_form.author = user
            new_form.save()
            return redirect(reverse("post"))
        else:
            return HttpResponse("you MUST logged")


class ShowUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/update.html"
    fields = ["title", "content", "status"]

    def form_valid(self, form):
        user = self.request.user
        new_form = form.save(commit=False)
        if new_form.author == user:
            form.save()
            return redirect(reverse("post"))
        else:
            return HttpResponse("you cannot edit other people posts")


class ShowDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/delete.html"
    success_url = reverse_lazy("post")
