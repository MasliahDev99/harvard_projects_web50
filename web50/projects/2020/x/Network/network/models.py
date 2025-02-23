from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Post {self.id} by {self.user}"

class Like(models.Model):
    """
        This model is used to store the likes of a post by a user.

    """
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_likes")
    
    class Meta:
        """
            This class is used to define the unique_together constraint.
        """
        unique_together = ("user", "post")
    def __str__(self):
        return f"Like {self.id} by {self.user} on {self.post}"
    

class Follow(models.Model):
    """
        This model is used to store the follows of a user.
    """
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followings")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")

    class Meta:
        """
            This class is used to define the unique_together constraint.
        """
        unique_together = ("follower", "following")
    
    def __str__(self):
        return f"Follow {self.id} by {self.follower} on {self.following}"
        


