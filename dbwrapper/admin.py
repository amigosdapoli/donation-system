from django.contrib import admin
from django.http import HttpResponse
from .models import Donation, Donor
import io
import csv
import logging

logger = logging.getLogger(__name__)

admin.site.disable_action('delete_selected')

class DonationAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    search_fields = ('donor_full_name', 'donor_tax_id')
    list_display = ('created_at_format', 'donor_full_name', 'donor_email', 'order_id', \
                    'nsu_id', 'donor_tax_id', 'donation_value', 'is_recurring', 'was_captured')
    list_filter = ('was_captured', )

    def download_csv(self, request, queryset):

        filename = 'stat-info.csv'
        f = io.StringIO()
        writer = csv.writer(f)
        writer.writerow(["created_at", "order_id"])

        for s in queryset:
            writer.writerow([s.created_at, s.order_id])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response
    download_csv.short_description = "Download CSV file for selected donations."

    def donor_full_name(self, instance):
        return instance.donor.name + " " + instance.donor.surname

    def donor_email(self, instance):
        return instance.donor.email

    def created_at_format(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M:%S")

class DonorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'tax_id')
    list_display = ('name', 'email', 'course_taken', 'course_year', 'tax_id', 'is_anonymous')


admin.site.register(Donation, DonationAdmin)
admin.site.register(Donor, DonorAdmin)
