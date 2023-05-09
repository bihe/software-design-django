# this can be seen as our repository for our model
from django.db import models


class OrderManager(models.Manager):
    def get_by_id(self, id: int) -> models.QuerySet:
        qs: models.QuerySet = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

