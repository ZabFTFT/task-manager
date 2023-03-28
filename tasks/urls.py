from django.urls import path

from tasks.views import index, ToDoList, CreateTaskView

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path("to_do_list/", ToDoList.as_view(), name="to-do-list"),
    path("create_task/", CreateTaskView.as_view(), name="create-task"),

]