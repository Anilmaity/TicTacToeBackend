from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from gameuser.schema import schema
from graphene_django.views import GraphQLView

urlpatterns = [
        path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
        path('', views.index, name='index'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
