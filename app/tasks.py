"""Celery tasks."""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_lesson_notification(
        self,
        student_id: int,
        student_name: str,
        lesson_title: str,
        event_type: str,
    ):
    """
    Send notification when a lesson is created, completed or changed.

    Args:
        self: current task instance
        student_id: student id
        student_name: student name
        lesson_title: lesson title
        event_type: event type ('created' or 'completed')
    """
    try:
        message = (
            f"Уведомление отправлено студенту {student_name} "
            f"(ID: {student_id}) по уроку '{lesson_title}.'"
        )
        if event_type == 'created':
            message += " Создан новый урок '{lesson_title}'."
        elif event_type == 'completed':
            message += " Урок '{lesson_title}' завершён."
        logger.info(message)
    except Exception as exc:
        logger.exception("Ошибка отправки уведомления")
        raise self.retry(exc=exc, countdown=60) from exc
