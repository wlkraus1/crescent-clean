from django.contrib import admin
from .models import Household, Client, Account, Holding, Task, Document

@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('name','aum_estimate','primary_advisor','created_at')
    search_fields = ('name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','household','risk_score','kyc_status')
    search_fields = ('first_name','last_name','email','household__name')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('household','custodian','account_type','tax_status','account_number_last4','status')
    list_filter = ('custodian','account_type','tax_status','status')
    search_fields = ('household__name','account_number_last4')

@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('account','symbol','quantity','price_as_of','as_of_date')
    list_filter = ('as_of_date',)
    search_fields = ('symbol','account__household__name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','household','due_on','assigned_to','status','priority')
    list_filter = ('status','priority','due_on')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title','household','client','immutable_flag','uploaded_at')
    list_filter = ('immutable_flag','uploaded_at')
    search_fields = ('title','household__name')
