from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
	DetailView,
	CreateView, 
	UpdateView,
	DeleteView
)
from django.http import HttpResponse
from .models import Post
# posts = [
#     {
#         'author' : 'Pankaj',
#         'title' : 'Blog Post',
#         'content' : 'First blog post',
#         'date_posted' : '24-05-2020'
#     },
#      {
#         'author' : 'Harshit',
#         'title' : 'Blog Post 2nd',
#         'content' : 'Second blog post',
#         'date_posted' : '24-05-2020'
#     }
# ]
def home(request):
	context = {
	    'posts' : Post.objects.all()
	}
	return render(request, 'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
    	form.instance.author = self.request.user
    	return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
    	form.instance.author = self.request.user
    	return super().form_valid(form)

    def test_func(self):
    	post = self.get_object()
    	if self.request.user == post.author:
    		return True
    	return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
    	post = self.get_object()
    	if self.request.user == post.author:
    		return True
    	return False
    
def about(request):
	return render(request,'blog/about.html', {'title': 'About'})

def hr(request):
	return HttpResponse('<h1>Harshit Pathak</h1>')

def mr(request):
	return HttpResponse('<h1>Pankaj Pathak</h1>')

