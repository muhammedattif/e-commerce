from django.contrib import admin
from .models import Stock, JoinForm

class JoinFormConfig(admin.ModelAdmin):
    model = JoinForm

    list_display = ('phone_number', 'email', 'agent_name', 'vendor_name')
    fields = ('agent_name', 'vendor_name', 'phone_number', 'email')

    actions = ['create_vendor', ]

    def create_vendor(self, request, queryset):
        for form in queryset:
            pass


admin.site.register(JoinForm, JoinFormConfig)


class StockConfig(admin.ModelAdmin):
    model = Stock

    list_filter = ('product', 'quantity')
    list_display = ('product', 'quantity')

    fields = ('product', 'options', 'quantity')

    def get_queryset(self, request):
        queryset = super(StockConfig, self).get_queryset(request)
        queryset = queryset.select_related('product').prefetch_related('options__feature')
        return queryset

admin.site.register(Stock, StockConfig)
