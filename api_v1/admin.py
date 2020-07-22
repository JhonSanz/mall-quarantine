from django.contrib import admin
from .models.mall import Mall
from .models.registry import Registry
from .models.visitor import Visitor

admin.site.register(Mall)
admin.site.register(Registry)
admin.site.register(Visitor)