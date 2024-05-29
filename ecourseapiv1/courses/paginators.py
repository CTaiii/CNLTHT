from rest_framework import pagination


class CoursePaginator(pagination.PageNumberPagination):
    page_size = 2

class LessonPaginator(pagination.PageNumberPagination):
    page_size = 2

class CommentPaginator(pagination.PageNumberPagination):
    page_size = 2
