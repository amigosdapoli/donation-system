from django.contrib import admin
from django.http import HttpResponse
from .models import Donation, Donor
import io
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

admin.site.disable_action('delete_selected')

class DonationAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    search_fields = ('donor_full_name', 'donor_tax_id')
    list_display = ('created_at_format', 'donor_full_name', 'donor_email', 'donor_phone_number', 'order_id', \
                    'nsu_id', 'donor_tax_id', 'donation_value', 'is_recurring', 'was_captured')
    list_filter = ('was_captured', 'created_at',)

    def download_csv(self, request, queryset):
        """
        Generates csv for download.
        """

        today = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = 'donations{}.csv'.format(today)

        donation_ids = []
        for s in queryset:
            donation_ids.append(s.donation_id)

        donations = Donation.objects.select_related("donor").filter(donation_id__in=donation_ids)

        columns = [
            "created_at",
            "donor_full_name",
            "donor_email",
            "donor_phone_number",
            "order_id",
            "nsu_id",
            "donor_tax_id",
            "donation_value",
            "is_recurring",
            "was_captured"]

        f = io.StringIO()
        writer = csv.writer(f)
        writer.writerow(columns)

        for s in donations:
            writer.writerow([
                s.created_at,
                s.donor.name.title() + " " + s.donor.surname.title(),
                s.donor.email,
                s.donor.phone_number,
                s.order_id,
                s.nsu_id,
                s.donor.tax_id,
                s.donation_value,
                s.is_recurring,
                s.was_captured])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response
    download_csv.short_description = "Download CSV file for selected donations."

    def donor_full_name(self, instance):
        return instance.donor.name + " " + instance.donor.surname

    def donor_email(self, instance):
        return instance.donor.email

    def donor_phone_number(self, instance):
        return instance.donor.phone_number

    def created_at_format(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M:%S")

class DonorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'tax_id')
    list_display = ('name', 'email', 'course_taken', 'course_year', 'tax_id', 'is_anonymous')


admin.site.register(Donation, DonationAdmin)
admin.site.register(Donor, DonorAdmin)
