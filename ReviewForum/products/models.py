from django.db import models
import uuid
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
def nameFile(instance, filename):
    return '/'.join(['images/', str(instance.product_id),filename])

class Review(models.Model):
    written_by = models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    review_id = models.UUIDField(editable=False, default=uuid.uuid4)
    rating = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    comment = models.CharField(max_length=255)
    reply = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        if self.rating<0 or self.rating>5:
            raise ValidationError('Rating needs to be between 0 and 5')

class Product(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)
    product_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    body = models.TextField()
    reviews = models.ManyToManyField(Review,related_name='reviews_for_product')

     
