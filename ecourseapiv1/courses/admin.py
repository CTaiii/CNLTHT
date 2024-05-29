from cloudinary.templatetags import cloudinary
from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe, format_html
from rest_framework import request

from courses.models import Course, Category,Lesson, Comment, Tag, Like, User, Points
from django.contrib.sites.shortcuts import get_current_site
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path


class MyCourseAdminSite(admin.AdminSite):
    site_header = 'eCourseOnline'

    def get_urls(self):
        return [path('course-stats/', self.stats_view)] + super().get_urls()

    def stats_view(self, request):
        course_stats = Category.objects.annotate(c=Count('course__id')).values('id', 'name', 'c')
        return TemplateResponse(request, 'admin/stats.html', {
            "course_stats": course_stats
        })


admin_site = MyCourseAdminSite(name='iCourse')


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class MyCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code','credit', 'active']
    search_fields = ['name', 'credit','user__username','category__name']
    list_filter = ['id', 'created_date', 'name']
    readonly_fields = ['my_image']
    form = CourseForm

    def my_image(self, instance):
        if instance and instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="120" />')
        else:
            return '-'

    my_image.short_description = 'Image'
    my_image.allow_tags = True

class MyColumn_NumberAdmin(admin.StackedInline):
    model = Points
    fk_name = 'lesson'


class MyLessonAdmin(admin.ModelAdmin):
    list_display = ['id','course_name', 'subject', 'image_tag','active']
    inlines = (MyColumn_NumberAdmin,)
    def image_tag(self, obj, request=None):
        if obj.image:
            return format_html('<a target="_blank" href="{}">{}</a>', obj.image.url, {obj.image.url})
        else:
            return '-'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def course_name(self, obj):
        return obj.course.name

class MyPointsAdmin(admin.ModelAdmin):
    list_display = ['get_course_name','column_name','lesson','status']

    def get_course_name(self, obj):
        return obj.lesson.course.name

    get_course_name.short_description = 'Course Name'


admin_site.register(Category)
admin_site.register(Course, MyCourseAdmin)
admin_site.register(Lesson, MyLessonAdmin)
admin_site.register(User)
admin_site.register(Tag)
admin_site.register(Comment)
admin_site.register(Like)
admin_site.register(Points,MyPointsAdmin)
