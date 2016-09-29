# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import smart_text
from autoslug import AutoSlugField
from django.db.models.signals import post_save
from pyfcm import FCMNotification

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

api_key = 'AIzaSyAuYvhngNUQRPLL9BH2ptvHu77tcUYjrNs'

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

    class Meta:
        ordering = ['ordering']

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
    slug = AutoSlugField(unique=True, populate_from='description', null=True, max_length=160)
    slug_notification = AutoSlugField(populate_from=get_slug_notification, unique_with=('description', 'event_type__event_day__description','start_time'), null=True, max_length=160)
    class Meta:
        ordering = ['ordering']

    def __unicode__(self):
        return str(self.description)

def get_slug_notification(self):
    return smart_text(self.description + self.start_time)



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
    #short_title = models.CharField(max_length=100,null=True,blank=True)
    #short_description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='news')
    picture = models.ImageField(upload_to='news',help_text='750 × 523')
    category_new = models.ForeignKey(CategoryNew, related_name='news')
    post_url = models.CharField(max_length=200, null=True, blank=True)
    def __unicode__(self):
        return str(self.title)


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
        null=True,blank=True)
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
    picture = models.ImageField(upload_to='drivers', help_text='',null=True,blank=True)
    number = models.IntegerField()
    nationality = models.CharField(max_length=100)
    birthday = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    championships = models.CharField(max_length=100, default="Ninguno")
    team = models.ForeignKey(Team)
    ordering = models.IntegerField(default=0)
    status_options = (
        ('enable', 'Habilitado',),
        ('disable', 'Deshabilitado',),
    )
    status = models.CharField(choices=status_options, max_length=20,default=status_options[0][0])
    
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
    number = models.IntegerField(null=True, blank=True)
    time = models.CharField(max_length=50,null=True, blank=True)
    gap = models.CharField(max_length=50,null=True, blank=True)
    laps = models.CharField(max_length=50,null=True, blank=True)
    q1 = models.CharField(max_length=50,null=True, blank=True)
    q2 = models.CharField(max_length=50,null=True, blank=True)
    q3 = models.CharField(max_length=50,null=True, blank=True)
    points = models.CharField(max_length=50,null=True, blank=True)
    phase = models.ForeignKey(Phase,null=True, blank=True)
    driver = models.ForeignKey(Driver,null=True,blank=True)

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
    location = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    picture = models.ImageField(upload_to='la_ciudad/sabor_del_chef', help_text='718px X 324px')
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


def send_notification_noticias(sender, instance, created, **kwargs):
    push_service = FCMNotification(api_key=api_key)
    if created:
        message = str(instance.title)
        title = "Nueva noticia"
    else:
        message = str(instance.title)
        title = "Actualización de noticia"
    data_message = {
        "type": "noticia",
        "noticia": str(instance.pk)
    }
    push_service.notify_topic_subscribers(message_title=title,topic_name="news",data_message=data_message, message_body=message,time_to_live=0)    

post_save.connect(send_notification_noticias, sender=New)

def send_notification_premio(sender, instance, created, **kwargs):
    push_service = FCMNotification(api_key=api_key)
    premio = instance.name
    if created:
        message = str(premio)
        title = "Resultados"
    else:
        message = str(premio)
        title = "Actualización de Resultados"
    data_message = {
        "type": "premio",
        "premio": str(instance.pk)
    }
    push_service.notify_topic_subscribers(message_title=title,topic_name="results", message_body=message,data_message=data_message,time_to_live=0)



post_save.connect(send_notification_premio, sender=Race)
