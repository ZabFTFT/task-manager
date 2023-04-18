from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from tasks.models import Task, TaskType, Position, Worker


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            name="Test Task",
            description="This is a test task",
            deadline=timezone.now() + timedelta(days=1),
            priority="M",
            task_type=TaskType.objects.create(name="Some"),
        )

    def test_task_creation(self):
        task = Task.objects.get(name="Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertFalse(task.is_completed)
        self.assertFalse(task.in_progress)
        self.assertEqual(task.priority, "M")

    def test_task_clean_method(self):
        task = Task(
            name="Test Task 2",
            description="This is a test task",
            deadline=timezone.now() - timedelta(days=1),
            priority="M",
            task_type_id=1,
        )
        with self.assertRaises(ValidationError):
            task.clean()

    def test_task_assignees(self):
        user1 = get_user_model().objects.create_user(
            username="test_user1",
            email="test1@example.com",
            password="test_password",
            position=Position.objects.create(name="Some"),
        )
        user2 = get_user_model().objects.create_user(
            username="test_user2",
            email="test2@example.com",
            password="test_password",
            position=Position.objects.create(name="Some"),
        )
        self.task.assignees.set([user1, user2])
        self.assertEqual(self.task.assignees.count(), 2)


class PositionTestCase(TestCase):
    def test_str_representation(self):
        position = Position.objects.create(name="Manager")
        self.assertEqual(str(position), "Manager")


class TaskTypeTestCase(TestCase):
    def test_str_representation(self):
        task_type = TaskType.objects.create(name="QA")
        self.assertEqual(str(task_type), "QA")


class WorkerTestCase(TestCase):
    def test_str_representation(self):
        position = Position.objects.create(name="Developer")
        user = Worker.objects.create_user(
            username="testuser",
            password="testpass",
            first_name="John",
            last_name="Doe",
            position=position,
        )
        self.assertEqual(str(user), "John Doe Developer")
