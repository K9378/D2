from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    au_user = models.OneToOneField(User, on_delete=models.CASCADE)
    au_rating = models.IntegerField(default=0)

    def update_rating(self):
        pr = self.post_set.aggregate(post_rating=Sum('post_rating'))
        prate = 0
        prate += pr.get('post_rating')

        cr = self.au_user.comment_set.aggregate(com_rating=Sum('com_rating'))
        crate = 0
        crate += cr.get('com_rating')

        self.au_rating = prate * 3 + crate
        self.save()


class Category(models.Model):
    cat_type = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    POST = 'PO'
    CATEGORY_POST = ((NEWS, 'Новость'), (POST, 'Статья'))
    post_category = models.CharField(max_length=2, choices=CATEGORY_POST, default=POST)
    post_time_in = models.DateTimeField(auto_now_add=True)
    post_cat = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[0:123]} ...'


class PostCategory(models.Model):
    pc_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pc_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    com_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    com_user = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.TextField()
    com_time_in = models.DateTimeField(auto_now_add=True)
    com_rating = models.IntegerField(default=0)

    def like(self):
        self.com_rating += 1
        self.save()

    def dislike(self):
        self.com_rating -= 1
        self.save()



