from django.contrib import admin
from .models import Category, Report, Vote


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    # Add the name of our *custom method* 'display_priority_score' to list_display
    list_display = ('title', 'user', 'status', 'created_at', 'display_priority_score')

    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')

    # We define a custom method for our new column.
    # The name of this method is what we put in list_display.
    @admin.display(description='Priority Score')
    def display_priority_score(self, obj):
        # 'obj' here is the Report instance for each row
        return obj.calculate_priority_score()

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'report')