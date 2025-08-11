from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('aum_estimate', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('primary_advisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('dob', models.DateField(blank=True, null=True)),
                ('ssn_last4', models.CharField(blank=True, max_length=4)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('risk_score', models.PositiveIntegerField(default=50)),
                ('kyc_status', models.CharField(default='In Review', max_length=50)),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='crm.household')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custodian', models.CharField(default='Schwab', max_length=100)),
                ('account_number_last4', models.CharField(blank=True, max_length=4)),
                ('account_type', models.CharField(default='Brokerage', max_length=100)),
                ('tax_status', models.CharField(choices=[('Taxable','Taxable'),('Traditional IRA','Traditional IRA'),('Roth IRA','Roth IRA'),('SEP IRA','SEP IRA')], default='Taxable', max_length=50)),
                ('model', models.CharField(blank=True, max_length=100)),
                ('opened_on', models.DateField(blank=True, null=True)),
                ('status', models.CharField(default='Active', max_length=50)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts', to='crm.client')),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='crm.household')),
            ],
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=12)),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=16)),
                ('cost_basis', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('price_as_of', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('as_of_date', models.DateField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holdings', to='crm.account')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('due_on', models.DateField()),
                ('assigned_to', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('Open','Open'),('Done','Done')], default='Open', max_length=20)),
                ('priority', models.CharField(choices=[('Low','Low'),('Normal','Normal'),('High','High')], default='Normal', max_length=20)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='crm.client')),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='crm.household')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('location', models.CharField(help_text='Placeholder path or URL', max_length=255)),
                ('immutable_flag', models.BooleanField(default=False)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='crm.client')),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='crm.household')),
            ],
        ),
    ]

