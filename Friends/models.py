from django.db import models
from User.models import Account

class FriendShip(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_friend', null=True)
    friends = models.ManyToManyField(Account, blank=True, related_name='friend_ship')
    status = models.CharField(max_length=10, choices=[
        ('PENDING', 'PENDING'),
        ('ACCEPTED', 'ACCEPTED'),
        ('REFUSE', 'REFUSE'),
    ])

    def __str__(self):
        return f"{self.user.username} - {', '.join([friend.username for friend in self.friends.all()])}"

class Request_FriendShip(models.Model):
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REFUSE = 'REFUSE'
    CHOICES_REQUEST = [
        (PENDING, 'PENDING'),
        (ACCEPTED, 'ACCEPTED'),
        (REFUSE, 'REFUSE'),
    ]

    from_user = models.ForeignKey(Account, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Account, related_name='to_user', on_delete=models.CASCADE)
    status = models.CharField(max_length=30,choices=CHOICES_REQUEST, default=PENDING)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now_add=True)

