from django.contrib import admin
from django.utils import timezone

from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'teacher', 'student', 'status', 'scheduled_at', 'created_at'
    )
    list_filter = ('status', 'created_at', 'scheduled_at')
    search_fields = ('title', 'student__username', 'teacher__username')
    date_hierarchy = 'scheduled_at'

    actions = ('mark_as_completed',)

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(
            status='completed', completed_at=timezone.now()
        )
        self.message_user(
            request, f'{updated} уроков отмечено как завершенные'
        )

    mark_as_completed.short_description = 'Отметить как завершенные'
