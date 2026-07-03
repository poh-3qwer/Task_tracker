from django.urls import path
from task_tracker import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('create/', views.TaskCreateView.as_view(), name='task-create'),
    path('update/<int:pk>', views.TaskUpdateView.as_view(), name='task-update'),
    path('delete/<int:pk>', views.TaskDeleteView.as_view(), name='task-delete'),
    path('comment-edit/<int:pk>/', views.CommentUpdateView.as_view(), name='edit-comment'),
    path('comment-delete/<int:pk>/', views.DeleteCommentView.as_view(), name='delete-comment'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path("logout/", views.CustomLogoutView.as_view(), name='logout'),
    path("register/", views.RegisterUserView.as_view(), name='register'),
]
