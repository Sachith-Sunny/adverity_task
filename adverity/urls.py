from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from api.views import counter, counter_api, fetch_api, home, show_table

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home, name="home"),
    path("list/", show_table, name="view"),
    path("fetch/", fetch_api, name="fetch"),
    path("counter/", counter, name="counter"),
    path("api/counter", counter_api),
]
