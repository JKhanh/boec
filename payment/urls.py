from django.urls import path

from payment import views

app_name = 'payment'
urlpatterns = [

    path('canceled/', views.payment_canceled, name='canceled'),
    path('done/<id>', views.payment_done, name='done'),
    path('<id>/process', views.payment_process, name='process')
]
