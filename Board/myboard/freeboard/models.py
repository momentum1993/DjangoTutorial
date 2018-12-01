from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    views = models.IntegerField(default = 0)

    def __str__(self):
        return "Post Object ( title: '"  + self.title + "', writer: '" + self.writer +"', content: '" + self.content[:10] + "...' )"

    def increase_Views(self):
        self.views = self.views + 1
        self.save()

    # def post_Edited(self, eTitle, eContent):
    #     self.title = eTitle
    #     self.content = eContent
    #     self.updated_at = timezone.now()




