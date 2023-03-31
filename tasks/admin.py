from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Position, TaskType, Worker, Task


@admin.register(Worker)
class WorkerUser(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "priority",
        "task_type",
        "in_progress",
        "is_completed",
    ]


admin.site.register(Position)
admin.site.register(TaskType)
