import uuid
from django.db import models

class  BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    class Meta:
        abstract = True