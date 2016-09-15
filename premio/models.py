# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import smart_text
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class TimeStampModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventDay(models.Model):
    description = models.CharField(max_length=100)
    date = models.DateField()

    def __unicode__(self):
        return str(self.description)


class EventType(models.Model):
    description = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)
    event_day = models.ForeignKey(EventDay,related_name='event_types')

    def __unicode__(self):
        return str(self.description)


class Event(TimeStampModel):
    description = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    #hora_fin = models.CharField(max_length=100)
    #descripcion = models.CharField(max_length=100)
    #zona = models.CharField(max_length=100)
    #event_day = models.ForeignKey(EventDay)
    event_type = models.ForeignKey(EventType, related_name='events')
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.description)


class CategoryNew(models.Model):
    description = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.description)


class BaseNew(TimeStampModel):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField()

    class Meta:
        abstract = True


class New(BaseNew):
    short_title = models.CharField(max_length=100,null=True,blank=True)
    short_description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='news',null=True, blank=True)
    picture = models.ImageField(upload_to='news',null=True, blank=True)
    category_new = models.ForeignKey(CategoryNew, related_name='news')
    post_url = models.CharField(max_length=200, null=True, blank=True)
    def __unicode__(self):
        return str(self.short_title)


class Race(TimeStampModel):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='races', help_text='716px X 365px')
    flag = models.ImageField(upload_to='races', help_text='100px X 60px')
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.name)

    def get_queryset(self):
        queryset = Race.objects.all().order_by('ordering')


class PhaseType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return smart_text(self.name)


class Phase(models.Model):
    P1 = 'P1'
    P2 = 'P2'
    P3 = 'P3'
    Q = 'Q'
    R = 'R'
    PHASES = (
        (P1, 'P1'),
        (P2, 'P2'),
        (P3, 'P3'),
        (Q, 'Q'),
        (R, 'R'),
    )
    name = models.CharField(
        max_length=2,
        choices=PHASES,
        default=P1)
    race = models.ForeignKey(Race)
    phase_type = models.ForeignKey(PhaseType)

    def __unicode__(self):
        return str(self.name)


class Team(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='teams', help_text='200px X 45px',null=True,blank=True)

    def __unicode__(self):
        return str(self.name)

    def natural_key(self):
        return (self.name)


class Driver(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='drivers', help_text='')
    number = models.IntegerField()
    nationality = models.CharField(max_length=100)
    birthday = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    championships = models.CharField(max_length=100, default="Ninguno")
    team = models.ForeignKey(Team)
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return smart_text(self.name)


class PhotoDriver(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='drivers/slides', help_text='200px X 45px')
    thumbnail = models.ImageField(upload_to='drivers/slides', help_text='200px X 45px',null=True,blank=True)
    driver = models.ForeignKey(Driver)
    
    def __unicode__(self):
        return str(self.name)

    def natural_key(self):
        return (self.name)


class Position(models.Model):
    number = models.IntegerField(null=True)
    time = models.CharField(max_length=50, null=True)
    gap = models.CharField(max_length=50, null=True)
    laps = models.CharField(max_length=50, null=True)
    q1 = models.CharField(max_length=50, null=True)
    q2 = models.CharField(max_length=50, null=True)
    q3 = models.CharField(max_length=50, null=True)
    points = models.CharField(max_length=50, null=True, default=0)
    phase = models.ForeignKey(Phase,null=True)
    driver = models.ForeignKey(Driver,null=True)

    def __unicode__(self):
        return str(self.number)

    def filter_queryset(self, queryset):
        queryset = super(InvoiceViewSet, self).filter_queryset(queryset)
        return queryset.order_by('-number')


class Hotel(TimeStampModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='la_ciudad/hoteles', help_text='718px X 324px')
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)
    website = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.name)


class Restaurant(TimeStampModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='la_ciudad/restaurantes', help_text='718px X 324px')
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return smart_text(self.name)


class Place(TimeStampModel):
    name = models.CharField(max_length=100)
    exposition = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='la_ciudad/puntos_de_interes', help_text='718px X 324px')
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return smart_text(self.name)

class Formula1Taste(TimeStampModel):
    name = models.CharField(max_length=100)
    chef = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    picture = models.ImageField(upload_to='la_ciudad/sabor_del_chef', help_text='718px X 324px')
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return smart_text(self.name)


class Zone(models.Model):
    title = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return smart_text(self.title)

class Grandstand(models.Model):    
    title = models.CharField(max_length=100)
    zone = models.ForeignKey(Zone, related_name='grandstands')
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return smart_text(self.title)


class Section(models.Model):
    title = models.CharField(max_length=100)
    grandstand = models.ForeignKey(Grandstand, related_name='sections')
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['pk']

    def __unicode__(self):
        return smart_text(self.title)


class Row(models.Model):
    title = models.IntegerField()
    section = models.ForeignKey(Section, related_name='rows')

    class Meta:
        ordering = ['pk']

    def __unicode__(self):
        return smart_text(self.title)


class Seat(models.Model):
    title = models.IntegerField()
    row = models.ForeignKey(Row, related_name='seats')

    def __unicode__(self):
        return smart_text(self.title)
