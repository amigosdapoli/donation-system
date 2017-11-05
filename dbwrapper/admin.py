from django.contrib import admin
from .models import Donation, Donor

admin.site.disable_action('delete_selected')

class DonationAdmin(admin.ModelAdmin):
    search_fields = ('donor_full_name', 'donor_tax_id')
    list_display = ('created_at_format', 'donor_full_name', 'donor_email', 'order_id', \
                    'nsu_id', 'donor_tax_id', 'donation_value', 'is_recurring', 'was_captured')
    list_filter = ('was_captured', )

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
