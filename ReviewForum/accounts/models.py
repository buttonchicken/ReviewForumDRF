from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    mobile_number = models.CharField(max_length=10)
    user_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    IsSeller = models.BooleanField(default=False)