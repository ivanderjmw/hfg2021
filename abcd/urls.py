from django.urls.conf import path, re_path

from . import views

urlpatterns = [
    path('results/sendJson/', views.save_graph, name='save_graph'),
    path('community/', views.step1, name='step1'),
    path('individuals/', views.step2, name='step2'),
    path('assets/', views.step3, name='step3'),
    path('assoc-institutions/', views.step4, name='step4'),
    path('results/', views.results, name='results'),
    re_path(r'^$', views.home, name='home')
]
