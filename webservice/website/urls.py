from django.conf.urls import url

from website import views

app_name = 'website'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^detail/$', views.list_all_phim_le, name='list_all_data_view'),
    url(r'^result/$', views.get_data_from_search, name='result'),
]
