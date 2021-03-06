# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-18 20:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_on_card', models.CharField(max_length=30)),
                ('card_number', models.CharField(max_length=19)),
                ('expiry_date_month', models.CharField(max_length=2)),
                ('expiry_date_year', models.CharField(max_length=2)),
                ('card_code', models.CharField(max_length=4)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('donation_id', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('donation_value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('donor_tax_id', models.CharField(max_length=15)),
                ('donor_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('is_recurring', models.NullBooleanField(default=False)),
                ('was_captured', models.NullBooleanField(default=False)),
                ('response_code', models.IntegerField(blank=True, default=None, null=True)),
                ('error_message', models.TextField(blank=True, default=None, null=True)),
                ('order_id', models.CharField(blank=True, default=None, max_length=35, null=True)),
                ('nsu_id', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('installments', models.IntegerField(choices=[(12, '1 ano'), (48, 'Indeterminada (cancelamento via e-mail contato@amigosdapoli.com.br)')], null=True)),
                ('created_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('referral_channel', models.CharField(blank=True, choices=[(None, 'Escolha...'), ('Indicação de amigos', 'Indicação de amigos'), ('Facebook', 'Facebook'), ('Linkedin', 'Linkedin'), ('Site de buscas (Google)', 'Site de buscas (Google)'), ('Mídias externas (rádio/jornal/revista)', 'Mídias externas (rádio/jornal/revista)')], default=None, max_length=40, null=True)),
                ('campaign_name', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('campaign_group', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('is_fraud', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('donor_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('tax_id', models.CharField(max_length=15, unique=True)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=15, null=True)),
                ('email', models.EmailField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('course_taken', models.CharField(blank=True, choices=[(None, 'Escolha...'), ('Não cursei engenharia na Poli', 'Não cursei engenharia na Poli'), ('Engenharia Ambiental', 'Engenharia Ambiental'), ('Engenharia Civil', 'Engenharia Civil'), ('Engenharia de Computação', 'Engenharia de Computação'), ('Engenharia de Materiais', 'Engenharia de Materiais'), ('Engenharia de Minas', 'Engenharia de Minas'), ('Engenharia de Petróleo', 'Engenharia de Petróleo'), ('Engenharia de Produção', 'Engenharia de Produção'), ('Engenharia Elétrica', 'Engenharia Elétrica'), ('Engenharia Mecânica', 'Engenharia Mecânica'), ('Engenharia Mecatrônica', 'Engenharia Mecatrônica'), ('Engenharia Metalurgica', 'Engenharia Metalurgica'), ('Engenharia Naval', 'Engenharia Naval'), ('Engenharia Química', 'Engenharia Química')], default=None, max_length=30, null=True)),
                ('course_year', models.CharField(blank=True, choices=[(None, 'Escolha...'), ('1950', '1950'), ('1951', '1951'), ('1952', '1952'), ('1953', '1953'), ('1954', '1954'), ('1955', '1955'), ('1956', '1956'), ('1957', '1957'), ('1958', '1958'), ('1959', '1959'), ('1960', '1960'), ('1961', '1961'), ('1962', '1962'), ('1963', '1963'), ('1964', '1964'), ('1965', '1965'), ('1966', '1966'), ('1967', '1967'), ('1968', '1968'), ('1969', '1969'), ('1970', '1970'), ('1971', '1971'), ('1972', '1972'), ('1973', '1973'), ('1974', '1974'), ('1975', '1975'), ('1976', '1976'), ('1977', '1977'), ('1978', '1978'), ('1979', '1979'), ('1980', '1980'), ('1981', '1981'), ('1982', '1982'), ('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025')], default=None, max_length=4, null=True)),
                ('is_anonymous', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EmailBlacklist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('updated_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('email_pattern', models.CharField(blank=True, default=None, max_length=35, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boleto_url', models.CharField(max_length=100)),
                ('onlineDebit_url', models.CharField(max_length=100)),
                ('authentication_url', models.CharField(max_length=100)),
                ('auth_code', models.CharField(max_length=20)),
                ('reference_num', models.CharField(max_length=20)),
                ('order_id', models.CharField(max_length=20)),
                ('transaction_id', models.CharField(max_length=20)),
                ('transaction_timestamp', models.DateTimeField()),
                ('response_code', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbwrapper.Donor'),
        ),
    ]
