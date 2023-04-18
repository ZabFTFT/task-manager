from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.forms.models import model_to_dict

from tasks.models import Task, Worker, Position, TaskType


class TasksViewsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass",
            position=Position.objects.create(name="Some"),
        )
        cls.task = Task.objects.create(
            name="Test Task",
            description="This is a test task",
            deadline="2023-04-01T12:00",
            priority="medium",
            task_type=TaskType.objects.create(name="QA"),
        )
        cls.task.assignees.set([cls.user])

    def setUp(self):
        self.client.login(username="testuser", password="testpass")

    def test_index_view(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")

    def test_project_task_list_view(self):
        response = self.client.get(reverse("tasks:project-tasks-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/project_task_all.html")
        self.assertContains(response, self.task.name)

    def test_project_task_list_finished_view(self):
        response = self.client.get(reverse("tasks:project-tasks-finished"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/project_task_finished.html")

    def test_project_task_detail_view(self):
        url = reverse("tasks:project-task-detail", args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/project_task_detail.html")
        self.assertContains(response, self.task.name)

    def test_create_task(self):
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.create(
            name="Test Task",
            description="This is a test task",
            deadline="2023-04-01T12:00",
            priority="medium",
            task_type=TaskType.objects.create(name="QA"),
        )

        url = reverse("tasks:create-task")
        task_dict = model_to_dict(task)
        task_dict.pop("completed_time", None)
        response = self.client.post(url, data=task_dict)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 2)

    def test_delete_task(self):
        url = reverse("tasks:task-delete", args=[self.task.pk])
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("tasks:project-tasks-list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertEqual(Task.objects.count(), 0)

    def test_create_worker(self):
        data = {
            "username": "testuser1",
            "password": "testpass1",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "position_id": 1,
        }
        user = get_user_model().objects.create_user(**data)

        self.assertEqual(Worker.objects.count(), 2)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@example.com")
