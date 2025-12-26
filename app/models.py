"""Django models."""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import send_lesson_notification

STATUS_CHOICES = [
    ('scheduled', 'Запланирован'),
    ('in_progress', 'В процессе'),
    ('completed', 'Завершен'),
    ('cancelled', 'Отменен'),
]


class Lesson(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='taught_lessons',
        verbose_name='Преподаватель'
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrolled_lessons',
        verbose_name='Студент'
    )

    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    scheduled_at = models.DateTimeField('Время начала')

    completed_at = models.DateTimeField(
        'Время завершения', null=True, blank=True
    )

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('-scheduled_at',)

    def __str__(self):
        return f"{self.title} - {self.student.username}"


@receiver(post_save, sender=Lesson)
def lesson_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """
    Signal sent when the lesson is created or completed.

    Args:
        sender: the model class
        instance: Lesson instance being saved
        created: a boolean, True if a new record was created
    """
    if created:
        send_lesson_notification.delay(
            student_id=instance.student.id,
            student_name=instance.student.username,
            lesson_title=instance.title,
            event_type='created'
        )
    elif instance.status == 'completed' and instance.completed_at:
        send_lesson_notification.delay(
            student_id=instance.student.id,
            student_name=instance.student.username,
            lesson_title=instance.title,
            event_type='completed'
        )
