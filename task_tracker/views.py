from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from .mixins import UserIsOwnerMixin


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'

class TaskCreateView(CreateView):
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
