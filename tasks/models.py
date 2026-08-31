from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "Todo"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        org = self.project.organization

        # created_by must be member of the project's organization (if provided)
        if self.created_by_id is not None:
            if not org.members.filter(id=self.created_by_id) .exists():
                raise ValidationError({"created_by": "created_by must be a member of the project's organization."})

        # assigned_to must be member of the project's organization (if provided)
        if self.assigned_to_id is not None:
            if not org.members.filter(id=self.assigned_to_id) .exists():
                raise ValidationError(
                    {"assigned_to": "assigned_to must be a member of the project's organization"})

    def save(self, *args, **kwargs):
        self.full_clean()  # runs clean() + field validation
        return super().save(*args, **kwargs)


class TaskComment(models.Model):
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="task_comments",
    )

    tent = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.task}"
