from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.text import slugify
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('published_date').reverse()
    paginator = Paginator(posts, 20)

    page_number = request.GET.get('page')

    context = {
        'page_title': 'Blog',
        'page_obj': paginator.get_page(page_number),
        'page_range': list(paginator.get_elided_page_range()),
    }
    return render(request, 'blog/post_list.html', context)


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True
    ).order_by('created_date')
    context = {
        'posts': posts,
        'page_title': 'Drafts',
    }
    return render(request, 'blog/post_draft_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
        'page_title': post.page_title(),
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_new(request):
    return post_edit(request)


@login_required
def post_edit(request, slug=None):
    post = None if slug is None else get_object_or_404(Post, slug=slug)
    heading = "New post" if slug is None else f"Edit: {post.title}"

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    context = {
        'page_title': heading,
        'heading': heading,
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)


@login_required
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('post_detail', slug=slug)


@login_required
def post_unpublish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.unpublish()
    return redirect('post_detail', slug=slug)


@login_required
def post_remove(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post_list')
