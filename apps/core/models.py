from typing import List, Optional
from django.db import models
from django.db.models import QuerySet


class BaseProjectModel(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @classmethod
    def get_all(cls) -> QuerySet['BaseProjectModel']:
        return cls.objects.all()

    @classmethod
    def get_by_id(cls, id: int) -> Optional['BaseProjectModel']:

        try:
            return cls.objects.get(pk=id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_elements_by_list_id(cls, list_ids: List[int]) -> QuerySet['BaseProjectModel']:

        return cls.objects.filter(pk__in=list_ids)

    @classmethod
    def exists_by_id(cls, id: int) -> bool:

        return cls.objects.filter(pk=id).exists()

    @classmethod
    def get_element_by_id_like_queryset(cls, id: int) -> QuerySet['BaseProjectModel']:

        return cls.objects.filter(pk=id)
