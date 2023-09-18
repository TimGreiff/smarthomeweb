from django.urls import path
from . import views
from .views import htmlviewer
from .views import SensorListView
from .views import login_view

urlpatterns = [
    path('', views.login_view, name='login'),
    path('web/', htmlviewer.as_view(template_name="web/index_a.html"), name='showindex'),
    path('about/', htmlviewer.as_view(template_name="web/about.html"), name='showabout'),
    path('contact/', htmlviewer.as_view(template_name="web/contact.html"), name='showcontact'),
    path("sensors/", SensorListView.as_view (), name='showsensorbasepage'),
    path("showtemps/", views.display_temps, name="displaytemps"),
    path("showhumid/", views.display_lf, name="displayhumidity"),
    path("showpress/", views.display_ld, name="displaypressure"),
    path("showtemps/<str:temp_id>/", views.tempdetails, name="temp_detail"),
    path("showhumid/<str:luftfeuchte_id>/", views.luftfeuchtedetails, name="luftfeuchte_detail"),
    path("showpress/<str:luftdruck_id>/", views.luftdruckdetails, name="luftdruck_detail"),
    path('sensors/editsensor/<str:sensor_id>/', views.edit_sensor_details),
    path('sensors/newsensor', views.add_sensor, name="add_sensor")
]

