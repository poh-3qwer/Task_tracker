from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Task, Comment
from .forms import TaskForm, CommentForm
from .mixins import UserIsOwnerMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.task = self.get_object()
            comment.save()

            return redirect('task-detail', pk=comment.task.pk)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
class TaskUpdateView(UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

class TaskDeleteView(UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = 'task_tracker/task_delete_confirmation.html'
    success_url = reverse_lazy('task-list')

class CommentUpdateView(UserIsOwnerMixin, UpdateView):
    model = Comment
    fields = ['text', ]

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})

class DeleteCommentView(UserIsOwnerMixin, DeleteView):
    model = Comment
    template_name = 'task_tracker/delete_comment_form.html'
    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})
    
class CustomLoginView(LoginView):
    template_name = 'task_tracker/login_form.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'login'

class RegisterUserView(CreateView):
    template_name = 'task_tracker/register_form.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy('login'))