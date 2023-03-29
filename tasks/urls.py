from django.urls import path

from tasks.views import (
    index,
    ProjectTasksList,
    CreateTaskView,
    personal_task_list,
    ProjectTaskDetailView,
    CreateWorkerView,
    DeleteTaskView,
)

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path("project_tasks/", ProjectTasksList.as_view(), name="project-tasks-list"),
    path("create_task/", CreateTaskView.as_view(), name="create-task"),
    path("profile/<int:pk>/", personal_task_list, name="profile-page"),
    path("project_tasks/<int:pk>/", ProjectTaskDetailView.as_view(), name="project-task"),
    path("create_worker/", CreateWorkerView.as_view(), name="worker-create"),
    path("project_tasks/<int:pk>/delete", DeleteTaskView.as_view(), name="task-delete"),



]