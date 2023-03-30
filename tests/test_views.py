from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Task, Worker, Position, TaskType


class TasksViewsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass", position=Position.objects.create(name="Some")
        )
        cls.worker = Worker.objects.create(first_name="John", last_name="Doe", position=Position.objects.create(name="Some")
        )
        cls.task = Task.objects.create(
            name="Test Task",
            description="This is a test task",
            deadline="2023-04-01T12:00",
            priority="medium",
            task_type=TaskType.objects.create(name="QA")
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
