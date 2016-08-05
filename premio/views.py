from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import viewsets, mixins
from common.mixins import CustomFieldsMixin, ActiveDesactiveMixin
from request_log.mixins import LoggingMixin
from rest_framework import viewsets, mixins
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings
from operator import itemgetter
#from rest_framework_tracking.mixins import LoggingMixin
from django.contrib.sites.models import Site


def get_domain():
    return "http://104.236.3.158"

damain_url = Site.objects.get_current().domain

class EventDayViewSet(LoggingMixin, CustomFieldsMixin, ActiveDesactiveMixin, viewsets.ModelViewSet):
    """
    Event Day endpoints
    """
    serializer_class = EventDaySerializer
    queryset = EventDay.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    model = EventDay
    default_fields = ['id', 'description', 'date', 'tipoeventos']

    def create(self, validated_data):
        instance = EventDay.objects.create(**validated_data)
        return instance


class CategoryNewViewSet(LoggingMixin, CustomFieldsMixin, ActiveDesactiveMixin, viewsets.ModelViewSet):
    """
    Category New endpoints
    """
    serializer_class = CategoryNewSerializer
    queryset = CategoryNew.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    model = EventDay
    default_fields = ['id', 'description']

class CategoryNewList(ListAPIView):
    serializer_class = CategoryNewSerializer
    permission_classes = []
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        return CategoryNew.objects.all().order_by('ordering')


class NewList(ListAPIView):
    serializer_class = NewListSerializer
    permission_classes = []

    def get_queryset(self):
        if self.request.method == "GET":
            if 'pk_category' in self.kwargs:
                return New.objects.filter(category_new=self.kwargs['pk_category']).order_by('date')

        return []


class LastNewsList(CustomFieldsMixin, ActiveDesactiveMixin, ListAPIView):
    serializer_class = NewListSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    model = New
    queryset = New.objects.all()

    def get_queryset(self):


        return New.objects.all().order_by('date')[:self.kwargs['last_news']]


class NewItemView(APIView):
    """
    List all snippets, or create a new snippet.
    Add a comment to this line
    """
    permission_classes = []
    def get(self, request, pk_category,pk_new, format=None):
        data_null = {"count": 0,
                     "next": None,
                     "previous": None,
                     "results": []
                     }
        try:
            new = New.objects.get(category_new=pk_category, pk=pk_new)
            serializer = NewItemSerializer(new)
            return Response(serializer.data)
        except New.DoesNotExist:
            return Response(data_null)
        return Response(data_null)


class RelatedNewList(ListAPIView):
    serializer_class = NewListSerializer
    permission_classes = []

    def get_queryset(self):
        if self.request.method == "GET":
            if 'pk_category' in self.kwargs and 'pk_new' in self.kwargs:
                try:
                    New.objects.get(category_new=self.kwargs['pk_category'], pk=self.kwargs['pk_new'])
                except New.DoesNotExist:
                    return []
                else:
                    return New.objects.filter(category_new=self.kwargs['pk_category']).exclude(pk=self.kwargs['pk_new']).order_by('date')[:3]

        return []



class PremioViewSet(CustomFieldsMixin, ActiveDesactiveMixin, viewsets.ModelViewSet):
    """
    Premios endpoints
    """
    serializer_class = PremioListSerializer
    queryset = Race.objects.all().order_by('name')
    permission_classes = []
    model = Race

    def create(self, validated_data):
        instance = Race.objects.create(**validated_data)
        return instance

    def list(self, request, client_pk=None):
        queryset = Race.objects.all().order_by('name')
        serializer = PremioListSerializer(queryset, many=True)
        return Response({"count": len(serializer.data),
                     "next": None,
                     "previous": None,
                     "results": serializer.data
                     })


    def retrieve(self, request, pk=None):
        queryset = Race.objects.filter(pk=pk)
        r = get_object_or_404(queryset, pk=pk)
        race = {"id": r.pk,"name": r.name,"flag": damain_url + settings.MEDIA_URL + str(r.flag)}
        phase_set = Phase.objects.filter(race=r).order_by("name")
        phases = []
        for i, phase in enumerate(phase_set):
            phase_aux = {"id": phase.pk,"name": phase.name,"phase_type": phase.phase_type.name}
            phases.append(phase_aux)
            positions = Position.objects.filter(phase=phase).order_by("number")
            positions_set = []
            for p in positions:
                position = {"id":p.pk, "number":p.number, "time":p.time, "gap": p.gap, "laps": p.laps, "q1":p.q1, "q2":p.q2, "q3":p.q3, "points": p.points, "driver": p.driver.short_name, "team":damain_url + settings.MEDIA_URL + str(
                    p.driver.team.picture)}
                positions_set.append(position)
            phases[i]["position_set"] = positions_set
        race["phase_set"] = phases
        return Response(race)


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


class RankingGeneralViewSet(APIView):
    """
    List all snippets, or create a new snippet.
    Add a comment to this line
    """
    permission_classes = []

    def get(self, request):
        races = Race.objects.all()
        results = []
        for i, race in enumerate(races):
            try:
                phase_r = race.phase_set.get(name='R')
            except Phase.DoesNotExist:
                pass
            else:
                positions = Position.objects.filter(phase=phase_r)
                if i == 0 or len(results) == 0:
                    for p in positions:
                        p_aux = {"id": p.driver.pk,"driver":p.driver.short_name,"team":p.driver.team.name,"picture_team":damain_url + settings.MEDIA_URL + str(p.driver.team.picture),"points":int(p.points)}
                        results.append(p_aux)
                else:
                    for p in positions:
                        index = find(results, "id", p.driver.pk)
                        if int(index) > -1:
                            results[index]["points"] = results[index]["points"] + int(p.points)
                        else:
                            p_aux = {"id": p.driver.pk, "driver": p.driver.short_name, "team": p.driver.team.name,
                                            "picture_team": damain_url + settings.MEDIA_URL + str(p.driver.team.picture),
                                            "points": int(p.points)}
                            results.append(p_aux)
        return Response(sorted(results, key=itemgetter('points'),reverse=True))


class PilotoViewSet(viewsets.ModelViewSet):
    """
    Premios endpoints
    """
    serializer_class = PilotoListSerializer
    queryset = Driver.objects.all().order_by('name')
    permission_classes = []
    model = Driver
    default_fields = ['id','name','picture']

    def create(self, validated_data):
        instance = Driver.objects.create(**validated_data)
        return instance

    def list(self, request, client_pk=None):
        print "list"
        queryset = Driver.objects.all().order_by('name')
        serializer = PilotoListSerializer(queryset, many=True)
        return Response({"count": len(serializer.data),
             "next": None,
             "previous": None,
             "results": serializer.data
             })


    def retrieve(self, request, pk=None):
        queryset = Driver.objects.filter(pk=pk)
        d = get_object_or_404(queryset, pk=pk)
        d_photos = d.photodriver_set.all()
        photos = []
        for p in d_photos:
            photos.append({"id":p.pk,"name":p.name,"picture":damain_url + settings.MEDIA_URL + str(p.picture),"thumbnail":damain_url + settings.MEDIA_URL + str(p.thumbnail)})
        driver = {"id": d.pk, "name": d.name, "number":d.number,"nationality":d.nationality, "birthday":d.birthday,
                  "place_of_birth":d.place_of_birth,"championships":d.championships,"photos": photos}

        return Response(driver)


class CiudadHotelesViewSet(LoggingMixin, CustomFieldsMixin, ActiveDesactiveMixin, viewsets.ModelViewSet):
    """
    Event Day endpoints
    """
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    permission_classes = []
    model = Hotel
    default_fields = ['id', 'name', 'location', 'phone','picture','latitude','longitude','ordering']

    def create(self, validated_data):
        instance = Hotel.objects.create(**validated_data)
        return instance


class CiudadRestaurantesViewSet(LoggingMixin, CustomFieldsMixin, ActiveDesactiveMixin, viewsets.ModelViewSet):
    """
    Event Day endpoints
    """
    serializer_class = RestauranteSerializer
    queryset = Restaurant.objects.all()
    permission_classes = []
    model = Restaurant
    default_fields = ['id', 'name', 'location', 'phone','picture','latitude','longitude','ordering']

    def create(self, validated_data):
        instance = Restaurant.objects.create(**validated_data)
        return instance

class CiudadLugaresVisitarViewSet(LoggingMixin, CustomFieldsMixin, ActiveDesactiveMixin, viewsets.ModelViewSet):
    """
    Event Day endpoints
    """
    serializer_class = LugarVisitarSerializer
    queryset = Place.objects.all()
    permission_classes = []
    model = Place
    default_fields = ['id', 'name', 'location', 'phone','picture','latitude','longitude','ordering']

    def create(self, validated_data):
        instance = Place.objects.create(**validated_data)
        return instance

