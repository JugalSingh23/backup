from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User

# Create your views here.

#not being used
def home(request): 
    context = {'posts':Post.objects.all()}
    return render(request, 'blog/home.html',context)

class PostListView(ListView): 
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts' 
    ordering = ['-date_posted']  
    paginate_by = 3

class UserPostListView(ListView): 
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts' 
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) #grab username from pk. check in User model. return 404 is doens't exist, else store in user
        return Post.objects.filter(author=user).order_by('-date_posted') #display only posts from author=user


class PostDetailView(DetailView): 
    model = Post
 #note : default template url format <app>/<model>_<viewtype>.html 
#Another note : refer to context as object here.


class PostCreateView(LoginRequiredMixin, CreateView): #this views was designed by django with model updation in mind. it expects you to refer to the form as "form" itself not object  
    model = Post 
    fields = ['title', 'content']

    def form_valid( self, form): #overriding the form and inputting the author field before submitting
        form.instance.author = self.request.user 
        return super().form_valid(form)
    #template format <app>/<model>_form. 
    #The magic is we don't even need to pass our form aur create the if post conditions and check if its valid and save it and update the model. becuz we inherited from CreateView, we save a lot of time

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Post 
    fields = ['title', 'content']

    def form_valid( self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
    
    def test_func(self): #test the user with a condition
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): 
    #expects <model>_confirm_delete.html in the <app> directory. also, no forms, so use object to refer to context
    model = Post
    success_url="/"
    def test_func(self): #test the user with a condition
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

def about(request):
    return render(request, 'blog/about.html',{'title':'About'})

