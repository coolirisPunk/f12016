from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class SectionResource(resources.ModelResource):

    class Meta:
        model = Section
        import_id_fields = ['id']

class RowResource(resources.ModelResource):

    class Meta:
        model = Row
        fields = ('id', 'title', 'section__title', 'section')
        export_order = ('section', 'title')



admin.site.register(CategoryNew)
admin.site.register(New)


class PocitionInlines(NestedStackedInline):
    model = Position
    extra = 10

class PhaseInlines(NestedStackedInline):
    model = Phase
    inlines = [PocitionInlines]


class RaceAdmin(NestedModelAdmin):

    inlines = [PhaseInlines]

admin.site.register(Race, RaceAdmin)



admin.site.register(PhaseType)
admin.site.register(Phase)
admin.site.register(Team)
admin.site.register(Driver)
admin.site.register(Position)
admin.site.register(PhotoDriver)

admin.site.register(Hotel)
admin.site.register(Restaurant)
admin.site.register(Place)
admin.site.register(Formula1Taste)

admin.site.register(Zone)
admin.site.register(Grandstand)
#admin.site.register(Row)


class SectionAdmin(ImportExportModelAdmin):
	pass


admin.site.register(Section, SectionAdmin)

class RowAdmin(ImportExportModelAdmin):
    resource_class = RowResource
    list_display = ['title', 'section', 'get_grandstand']
    list_filter = ['section', 'section__grandstand']
    
    def get_grandstand(self, obj):
    	return obj.section.grandstand


class SeatAdmin(ImportExportModelAdmin):
    pass


class EventoInlines(NestedStackedInline):
    model = Event

class EtapaDiaCarreraInlines(NestedStackedInline):
    model = EventType
    inlines = [EventoInlines]


class HorarioAdmin(NestedModelAdmin):
    
    inlines = [EtapaDiaCarreraInlines]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    #readonly_fields = ['slug','slug_notification']
    pass
    

admin.site.register(EventDay, HorarioAdmin)
admin.site.register(EventType)


admin.site.register(Row, RowAdmin)
admin.site.register(Seat, SeatAdmin)


