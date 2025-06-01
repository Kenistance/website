# payments/admin.py

from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'amount', 'method', 'status', 'transaction_id', 'created_at')
    search_fields = ('user__username', 'project__title', 'transaction_id')
    list_filter = ('method', 'status')
    readonly_fields = ('created_at',)
