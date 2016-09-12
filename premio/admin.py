from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class SectionResource(resources.ModelResource):

    class Meta:
        model = Section
        import_id_fields = ['id']

admin.site.register(EventDay)
admin.site.register(EventType)
admin.site.register(Event)

admin.site.register(CategoryNew)
admin.site.register(New)
admin.site.register(Race)



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
    list_display = ['title', 'section', 'get_grandstand']
    list_filter = ['section', 'section__grandstand']
    
    def get_grandstand(self, obj):
    	return obj.section.grandstand


class SeatAdmin(ImportExportModelAdmin):
    pass




admin.site.register(Row, RowAdmin)
admin.site.register(Seat, SeatAdmin)