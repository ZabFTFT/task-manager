from django.urls import path

from tasks.views import index, ToDoList

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path("to_do_list/", ToDoList.as_view(), name="ToDoList"),

]