from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Household(models.Model):
    name = models.CharField(max_length=200)
    aum_estimate = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    primary_advisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Client(models.Model):
    household = models.ForeignKey(Household, related_name='clients', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    dob = models.DateField(null=True, blank=True)
    ssn_last4 = models.CharField(max_length=4, blank=True)
    address = models.CharField(max_length=255, blank=True)
    risk_score = models.PositiveIntegerField(default=50)
    kyc_status = models.CharField(max_length=50, default='In Review')
    def __str__(self): return f"{self.first_name} {self.last_name}"

class Account(models.Model):
    TAX = [('Taxable','Taxable'),('Traditional IRA','Traditional IRA'),('Roth IRA','Roth IRA'),('SEP IRA','SEP IRA')]
    household = models.ForeignKey(Household, related_name='accounts', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='accounts', on_delete=models.SET_NULL, null=True, blank=True)
    custodian = models.CharField(max_length=100, default='Schwab')
    account_number_last4 = models.CharField(max_length=4, blank=True)
    account_type = models.CharField(max_length=100, default='Brokerage')
    tax_status = models.CharField(max_length=50, choices=TAX, default='Taxable')
    model = models.CharField(max_length=100, blank=True)
    opened_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Active')
    def __str__(self): return f"{self.custodian} ••••{self.account_number_last4}"

class Holding(models.Model):
    account = models.ForeignKey(Account, related_name='holdings', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=12)
    quantity = models.DecimalField(max_digits=16, decimal_places=4)
    cost_basis = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_as_of = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    as_of_date = models.DateField()

class Task(models.Model):
    STATUS = [('Open','Open'),('Done','Done')]
    PRIORITY = [('Low','Low'),('Normal','Normal'),('High','High')]
    household = models.ForeignKey(Household, related_name='tasks', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    due_on = models.DateField()
    assigned_to = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Open')
    priority = models.CharField(max_length=20, choices=PRIORITY, default='Normal')

class Document(models.Model):
    household = models.ForeignKey(Household, related_name='documents', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='documents', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=255, help_text='Placeholder path or URL')
    immutable_flag = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
