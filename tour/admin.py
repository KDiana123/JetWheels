from django.contrib import admin

from tour.models import Tour, Reservation, Service, Photo

# Register your models here.


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('image', 'caption', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return '<img src="{0}" style="width: 100px; height: auto;" />'.format(obj.image.url)
        return ''
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'


class TourAdmin(admin.ModelAdmin):
    list_display = ('tour_name', 'start_date', 'end_date', 'price', 'tour_capacity', 'location')
    inlines = [PhotoInline]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Tour, TourAdmin)
admin.site.register(Reservation)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Photo)