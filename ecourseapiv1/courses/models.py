from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField(null=True)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ItemBase(BaseModel):
    tags = models.ManyToManyField(Tag)

    class Meta:
        abstract = True


class Course(ItemBase):
    name = models.CharField(max_length=255)
    description = RichTextField()
    code = models.CharField(max_length=10, default=None)
    credit = models.CharField(max_length=1,default=0)
    image = CloudinaryField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name


class Lesson(ItemBase):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = CloudinaryField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} - {self.lesson_id}'

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255)


class Like(Interaction):

    class Meta:
        unique_together = ('user', 'lesson')


class Points(BaseModel):
    column_name = models.CharField(max_length=255,null=True)
    point = models.CharField(max_length=3,default=0)
    status = models.BooleanField(default=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,null=True)
