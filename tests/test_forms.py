from django.test import TestCase
from django.utils import timezone

from tasks.forms import CreateTaskForm, CreateWorkerForm
from tasks.models import Task, TaskType, Worker, Position


class CreateTaskFormTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Test Task Type")
        self.worker = Worker.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
            position=Position.objects.create(name="Tester"),
        )

    def test_create_task_form_valid_data(self):
        form = CreateTaskForm(
            data={
                "name": "Test Task",
                "description": "Test description",
                "deadline": timezone.now() + timezone.timedelta(days=1),
                "priority": "M",
                "task_type": self.task_type.id,
                "assignees": [self.worker.id],
            }
        )
        self.assertTrue(form.is_valid())
