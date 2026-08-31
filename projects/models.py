from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Project(models.Model):
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='projects'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_projects'
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    start_date = models.DateField()
    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.created_by_id is not None:
            if not self.organization.members.filter(id=self.created_by_id).exists():
                raise ValidationError(
                    {"created_by": "created_by must be a member of the organization."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
