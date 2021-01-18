# Generated by Django 3.1.4 on 2021-01-18 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0013_auto_20201214_2052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('article_no', models.CharField(max_length=8)),
                ('description', models.CharField(max_length=30)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookingCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=3)),
                ('description_en', models.CharField(max_length=30)),
                ('description_de', models.CharField(max_length=30)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookingcode_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookingcode_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustComplaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('finished_on', models.SmallIntegerField()),
                ('memo', models.TextField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custcomplaint_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custcomplaint_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('memo', models.TextField(null=True)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('order_no', models.CharField(max_length=8)),
                ('price', models.SmallIntegerField(blank=True, null=True)),
                ('issued_on', models.SmallIntegerField()),
                ('delivery_date', models.SmallIntegerField()),
                ('received_on', models.SmallIntegerField(null=True)),
                ('memo', models.TextField(blank=True, null=True)),
                ('external_system', models.BooleanField(default=False)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custorder_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custorder_update_user', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustOrderDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('pos', models.IntegerField(blank=True)),
                ('unit_price', models.IntegerField()),
                ('received_on', models.SmallIntegerField(null=True)),
                ('memo', models.TextField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custorderdet_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custorderdet_update_user', to=settings.AUTH_USER_MODEL)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.article')),
                ('cust_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.custorder')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiveSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debugflag', models.BooleanField(default=True)),
                ('timeactive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('subject', models.CharField(max_length=100)),
                ('sent_on', models.SmallIntegerField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_update_user', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='receiver', to='auth.group')),
                ('sender', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('part_no', models.CharField(max_length=8)),
                ('description', models.CharField(max_length=30)),
                ('unit_price', models.SmallIntegerField(null=True)),
                ('image', models.BinaryField(null=True)),
                ('pack_quantity', models.SmallIntegerField()),
                ('install_quantity', models.SmallIntegerField()),
                ('initial_stock', models.SmallIntegerField()),
                ('total_stock', models.SmallIntegerField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='part_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='part_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('table', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=1)),
                ('description_en', models.CharField(max_length=30)),
                ('description_de', models.CharField(max_length=30)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='status_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='status_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('is_supplier_stock', models.BooleanField(default=False)),
                ('stock', models.SmallIntegerField()),
                ('reserved', models.SmallIntegerField(default=0)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_update_user', to=settings.AUTH_USER_MODEL)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.part')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SuppComplaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('finished_on', models.SmallIntegerField()),
                ('memo', models.TextField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suppcomplaint_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suppcomplaint_update_user', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('memo', models.TextField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplier_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplier_update_user', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SuppOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('order_no', models.CharField(max_length=8)),
                ('price', models.SmallIntegerField(blank=True, null=True)),
                ('issued_on', models.SmallIntegerField()),
                ('delivery_date', models.SmallIntegerField()),
                ('received_on', models.SmallIntegerField(null=True)),
                ('memo', models.TextField(blank=True, null=True)),
                ('external_system', models.BooleanField(default=False)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supporder_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supporder_update_user', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.supplier')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Timers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nowactive', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('string_en', models.CharField(max_length=128, unique=True)),
                ('string_de', models.CharField(max_length=128, unique=True)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='translation_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='translation_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TodoType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=3)),
                ('description_en', models.CharField(max_length=150)),
                ('description_de', models.CharField(max_length=150)),
                ('title_de', models.CharField(max_length=50)),
                ('title_en', models.CharField(max_length=50)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='todotype_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='todotype_update_user', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('start_on', models.SmallIntegerField(null=True)),
                ('finished_on', models.SmallIntegerField(null=True)),
                ('active', models.SmallIntegerField(null=True)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='todo_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='todo_update_user', to=settings.AUTH_USER_MODEL)),
                ('cust_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.custorder')),
                ('cust_order_det', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.custorderdet')),
                ('todo_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.todotype')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SuppOrderDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('pos', models.IntegerField(blank=True)),
                ('unit_price', models.IntegerField()),
                ('received_on', models.SmallIntegerField(null=True)),
                ('memo', models.TextField()),
                ('quantity', models.SmallIntegerField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supporderdet_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supporderdet_update_user', to=settings.AUTH_USER_MODEL)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.part')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
                ('supp_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.supporder')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SuppContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('barcode', models.CharField(max_length=8)),
                ('delivery_date', models.SmallIntegerField()),
                ('memo', models.TextField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suppcontainer_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suppcontainer_update_user', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
                ('supp_order_det', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.supporderdet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SuppComplaintDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('finished_on', models.SmallIntegerField()),
                ('memo', models.TextField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suppcomplaintdet_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suppcomplaintdet_update_user', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
                ('supp_complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.suppcomplaint')),
                ('supp_order_det', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.supporderdet')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('date', models.SmallIntegerField()),
                ('previous_stock', models.SmallIntegerField()),
                ('booking_quantity', models.SmallIntegerField()),
                ('new_stock', models.SmallIntegerField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stockmovement_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stockmovement_update_user', to=settings.AUTH_USER_MODEL)),
                ('booking_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.bookingcode')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.stock')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_update_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='part',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status'),
        ),
        migrations.AddField(
            model_name='part',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.supplier'),
        ),
        migrations.CreateModel(
            name='MessageUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('user_is_sender', models.BooleanField(default=False)),
                ('is_trash', models.BooleanField(default=False)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messageuser_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messageuser_update_user', to=settings.AUTH_USER_MODEL)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.message')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MessageTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=100)),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messagetemplate_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messagetemplate_update_user', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status'),
        ),
        migrations.AddField(
            model_name='custorderdet',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status'),
        ),
        migrations.AddField(
            model_name='custorder',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status'),
        ),
        migrations.AddField(
            model_name='custorder',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status'),
        ),
        migrations.CreateModel(
            name='CustContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('barcode', models.CharField(max_length=8)),
                ('delivery_date', models.SmallIntegerField()),
                ('memo', models.TextField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custcontainer_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custcontainer_update_user', to=settings.AUTH_USER_MODEL)),
                ('cust_order_det', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.custorderdet')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustComplaintDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('pos', models.SmallIntegerField()),
                ('quantity', models.SmallIntegerField()),
                ('memo', models.TextField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custcomplaintdet_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custcomplaintdet_update_user', to=settings.AUTH_USER_MODEL)),
                ('cust_complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.custcomplaint')),
                ('cust_order_det', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.custorderdet')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='custcomplaint',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status'),
        ),
        migrations.AddField(
            model_name='custcomplaint',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ArtiPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_creation_date', models.DateTimeField(auto_now_add=True)),
                ('_update_date', models.DateTimeField(auto_now=True)),
                ('quantity', models.SmallIntegerField()),
                ('_creation_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artipart_creation_user', to=settings.AUTH_USER_MODEL)),
                ('_update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artipart_update_user', to=settings.AUTH_USER_MODEL)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.article')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtapp.part')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='article',
            name='parts',
            field=models.ManyToManyField(through='gtapp.ArtiPart', to='gtapp.Part'),
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gtapp.status'),
        ),
    ]
