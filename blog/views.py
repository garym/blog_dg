from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('published_date')
    context = {
        'posts': posts,
        'page_title': 'Blog',
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


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
        'page_title': post.page_title(),
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_new(request):
    return post_edit(request)


@login_required
def post_edit(request, pk=None):
    post = None if pk is None else get_object_or_404(Post, pk=pk)
    heading = "New post" if pk is None else f"Edit: {post.title}"

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'page_title': heading,
        'heading': heading,
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_unpublish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.unpublish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
