from .views import *
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf.urls import patterns, url, include
from rest_framework_nested import routers

router = DefaultRouter()
#router = routers.SimpleRouter()

router_premios = routers.SimpleRouter()

router.register(r'horarios', EventDayViewSet, base_name='horarios')
router.register(r'beneficios', BenefitViewSet, base_name='beneficios')

router.register(r'premios', PremioViewSet, base_name='premios')
router.register(r'pilotos', PilotoViewSet, base_name='pilotos')
router.register(r'la_ciudad/hoteles', CiudadHotelesViewSet, base_name='hoteles')
#router.register(r'la_ciudad/restaurantes', CiudadRestaurantesViewSet, base_name='restaurantes')
router.register(r'la_ciudad/a_donde_ir', CiudadLugaresVisitarViewSet, base_name='a_donde_ir')
router.register(r'la_ciudad/sabor_del_chef', SaborDelChefViewSet, base_name='sabor_del_chef')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^ranking_general/$', RankingGeneralViewSet.as_view()),
    url(r'^news/category_news/$', CategoryNewList.as_view()),
    url(r'^news/last_news/(?P<last_news>[0-9]+)/$', LastNewsList.as_view()),
    url(r'^news/category_news/(?P<pk_category>[0-9]+)/news/$', NewList.as_view()),
    url(r'^news/category_news/(?P<pk_category>[0-9]+)/news/(?P<pk_new>[0-9]+)/$', NewItemView.as_view()),
    url(r'^news/related_news/(?P<pk_category>[0-9]+)/news/(?P<pk_new>[0-9]+)/$', RelatedNewList.as_view()),

    url(r'^zones/$', ZoneList.as_view()),
    url(r'^grandstands/(?P<zone>[0-9]+)/$', GrandstandList.as_view()),
    url(r'^sections/(?P<grandstand>[0-9]+)/$', SectionList.as_view()),
    url(r'^rows/(?P<section>[0-9]+)/$', RowList.as_view()),
    url(r'^seats/(?P<row>[0-9]+)/$', SeatList.as_view()),

]
