from django.db import models


class BaseProjectModel(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_by_id(cls, id: int):

        try:
            return cls.objects.get(pk=id)
        except BaseProjectModel.DoesNotExist:
            return None
