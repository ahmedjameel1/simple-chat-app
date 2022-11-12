from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True , blank=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True , blank=True, related_name="messages")
    is_read = models.BooleanField(default=False,null=True)
    body = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.body
    
    class Meta:
        ordering = ['is_read','-created']