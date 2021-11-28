from django.contrib.admin import AdminSite
from django.contrib import admin

from .models import *

AdminSite.index_title = 'Администрация сайта'
AdminSite.site_title = 'Интернет-провайдер'
AdminSite.site_header = 'Интернет-провайдер'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('status', 'client', 'connection_date', 'rate')
    list_filter = ('connection_date', 'status', 'client', 'rate')


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'mid_name', 'contract_number')
    search_fields = ('last_name', 'contract_number')


class RatesAdmin(admin.ModelAdmin):
    list_display = ('rate_name', 'fee', 'provided_speed')
    search_fields = ['rate_name']
    list_filter = ('fee', 'provided_speed')


class ListOfServicesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'service_name')
    search_fields = ['service_name']


class ListOfEquipAdmin(admin.ModelAdmin):
    list_display = ('pk', 'equip_type')
    search_fields = ['equip_type']


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'mid_name', 'post')
    list_filter = ['post']
    search_fields = ['last_name']


class CustomersEquipmentAdmin(admin.ModelAdmin):
    list_display = ('equip_name', 'serial_number')
    list_filter = ['equip_name']
    search_fields = ['serial_number']


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('equip_name', 'serial_number', 'cequip_id', 'equip_type')
    list_filter = ['equip_type']
    search_fields = ('equip_name', 'serial_number')


admin.site.register(Order, OrderAdmin)
admin.site.register(Clients, ClientsAdmin)
admin.site.register(Rates, RatesAdmin)
admin.site.register(ListOfServices, ListOfServicesAdmin)
admin.site.register(ListOfEquip, ListOfEquipAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(CustomersEquipment, CustomersEquipmentAdmin)
