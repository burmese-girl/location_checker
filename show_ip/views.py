from http.client import UNPROCESSABLE_ENTITY
import json
from urllib import request
from django.http import JsonResponse
from datetime import datetime
from itertools import count
from requests import get
from json import dumps
from ipaddress import ip_address
from .models import IpAddress
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from . import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model, login as auth_login, logout
from django.http import HttpResponse
from . import models
from django.contrib import auth
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.views import generic

# Create your views here.


def index(request):
    # return render(request, "index.html", {})
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:profile'))
    return HttpResponseRedirect(reverse(settings.LOGIN_URL))


def login(request):
    print("Went Login")
    form = forms.AuthenticateExtraForm(request, data=request.POST)

    if request.method != 'POST':
        form = forms.AuthenticateExtraForm(request)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            print("Login Successfully!")

        else:
            html = "<h2 style='background-color:yellow;'> Authentication Error! Check username & password again !</h2>"
            return HttpResponse(html)

        return HttpResponseRedirect(reverse('user:profile'))

    return render(request, "login.html", {
        'form': form,

    })


def profile(request):
    print("reached profile. :")

    try:
        user = models.UserProfile.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse(settings.LOGIN_URL))

    if request.method != 'POST':
        profile_form = forms.ProfileForm(instance=user, initial={'first_name': request.user.first_name,
                                                                 'last_name': request.user.last_name})
        return render(request, "profile.html", {'form': profile_form, })
    return HttpResponseRedirect(reverse('user:profile'))


def show_ipDashboard(request):

    print("reached Dasboard")
    try:
        user = models.UserProfile.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse(settings.LOGIN_URL))

    if request.method != 'POST':
        profile_form = forms.ProfileForm(instance=user, initial={'first_name': request.user.first_name,
                                                                 'last_name': request.user.last_name})
        return render(request, "dashboard.html", {'form': profile_form, })

    return HttpResponseRedirect(reverse('user:dasboard'))


def logout(request):
    form = forms.AuthenticateExtraForm(request)
    # import pdb;pdb.set_trace()
    auth.logout(request)

    return render(request, "logout.html", {'form': form, })


def register(request):
    if request.method != 'POST':
        form = forms.SingupForm()
        return render(request, 'signup.html', {'form': form})

    register_form = forms.SingupForm(request.POST)
    if not register_form.is_valid():
        return render(request, 'signup.html', {"form": register_form})
    transaction.atomic()

    try:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        residential_country = request.POST.get('residential_country')
        nationality = request.POST.get('nationality', '')
        user = User.objects.create_user(username=email, email=email)
        user.is_active = True
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password:
            user.set_password(password)
        user.save()

        print("User =============")
        print(user)

        profile, created = models.UserProfile.objects.get_or_create(
            user_id=user.pk, dob=dob)  # requried field=dob
        profile.gender = gender
        profile.dob = dob
        profile.name = first_name+" "+last_name
        profile.residential_country = residential_country
        profile.nationality = nationality
        profile.active_user = True
        profile.created_user = "Admin Site"
        profile.save()
        print("Profile =============")

        print(profile)

    except ValueError:
        print
        transaction.rollback()
        messages.add_message(request, messages.INFO, _('Registration failed.'))
        return render(request, 'signup.html', {
            'form': forms.RegistrationForm(request.POST),

        })

    # return render(request,'signup.html', {'form': form,})
    return HttpResponseRedirect(reverse('user:profile'))


def search(request):

    if request.method == 'POST':
        search_id = request.POST.get('ip_address', None)

        url = "http://ipwho.is/%s" % (search_id)
        result = get(url).json()

        try:
            if result['success'] == True:
                ip = result['ip']
                continent = result["continent"]
                country = result["country"]
                country_code = result["country_code"]
                region = result["region"]
                region_code = result["region_code"]
                city = result["city"]
                print(url)
                from pprint import pprint
                pprint(result)
                req_user = request.user

                ip_model, created = models.IpAddress.objects.get_or_create(ip=ip,
                                                                           continent=continent,
                                                                           country=country,
                                                                           country_code=country_code,
                                                                           region=region,  region_code=region_code, city=city,
                                                                           user_id=req_user.pk, create_date=datetime.now())

                html = ("<H1>%s is checking for this ip addreess.</H1>", req_user
                        )
                # return HttpResponse('profile.html')
                return HttpResponseRedirect(reverse('user:dashboard'))
            elif result['success'] == False:
                msg = result['message']
                return HttpResponse("This IP is "+msg)

        except IpAddress.DoesNotExist:
            return HttpResponse("Fail API")
    else:
        form = forms.IPSearchForm()
        return render(request, 'search_ip.html', {'form': form, },)


class LocationListView(generic.ListView):
    model = models.IpAddress
    context_object_name = 'IP_list'

    def get(self, request, *args, **kwargs):
        ip_list = models.IpAddress.objects.order_by(
            '-create_date').filter(user_id=request.user.pk)
        return render(request, 'ip_dashboard.html',
                      {'ip_list': ip_list})

    def post(self, request, *args, **kwargs):
        ip_list = models.IpAddress.objects.order_by(
            '-create_date').filter(user_id=request.user.pk)

        return render(request, 'ip_dashboard.html',
                      {'ip_list': ip_list})


def country_queryset(request):
    count = 0
    queryset = models.IpAddress.objects.filter(user_id=request.user.pk)
    label_data = []
    country_data = []
    region_data = []

    us = models.IpAddress.objects.filter(country_code='US')
    cn = models.IpAddress.objects.filter(country_code='CN')
    jp = models.IpAddress.objects.filter(country_code='JP')
    uk = models.IpAddress.objects.filter(country_code='GB')
    idon = models.IpAddress.objects.filter(country_code='ID')
    canada = models.IpAddress.objects.filter(country_code='CA')
    parkistan = models.IpAddress.objects.filter(country_code='PK')
    afghanistan = models.IpAddress.objects.filter(country_code='AF')
    albania = models.IpAddress.objects.filter(country_code='AL')
    Algeria = models.IpAddress.objects.filter(country_code='DZ')
    american_samoa = models.IpAddress.objects.filter(country_code='AS')
    andorra = models.IpAddress.objects.filter(country_code='AD')
    Angola = models.IpAddress.objects.filter(country_code='AO')
    Anguilla = models.IpAddress.objects.filter(country_code='AI')
    Antarctica = models.IpAddress.objects.filter(country_code='AQ')
    Australia = models.IpAddress.objects.filter(country_code='AU')
    Austria = models.IpAddress.objects.filter(country_code='AT')
    Bangladesh = models.IpAddress.objects.filter(country_code='BT')
    Barbados = models.IpAddress.objects.filter(country_code='BB')
    Belarus = models.IpAddress.objects.filter(country_code='BY')
    Belgium = models.IpAddress.objects.filter(country_code='BE')
    Bhutan = models.IpAddress.objects.filter(country_code='BT')
    Brazil = models.IpAddress.objects.filter(country_code='BR')
    Bulgaria = models.IpAddress.objects.filter(country_code='BG')
    Myanmar = models.IpAddress.objects.filter(country_code='MM')
    Slovakia = models.IpAddress.objects.filter(country_code='SK')
    Slovenia = models.IpAddress.objects.filter(country_code='SI')
    Iran = models.IpAddress.objects.filter(country_code='IR')
    Morocco = models.IpAddress.objects.filter(country_code='MA')
    Korea_South = models.IpAddress.objects.filter(country_code='KR')
    Korea_North = models.IpAddress.objects.filter(country_code='KP')
    Spain = models.IpAddress.objects.filter(country_code='ES')

    if len(Brazil) >= 1:
        count = len(Brazil)
        country = Brazil[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Spain) >= 1:
        count = len(Spain)
        country = Spain[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Korea_South) >= 1:
        count = len(Korea_South)
        country = Korea_South[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Korea_North) >= 1:
        count = len(Korea_North)
        country = Korea_North[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Morocco) >= 1:
        count = len(Morocco)
        country = Morocco[0].country
        label_data.append(country)
        country_data.append(count)

    if len(canada) >= 1:
        count = len(canada)
        country = canada[0].country
        label_data.append(country)
        country_data.append(count)

    if len(parkistan) >= 1:
        count = len(parkistan)
        country = parkistan[0].country
        label_data.append(country)
        country_data.append(count)

    if len(us) >= 1:
        count = len(us)
        country = us[0].country
        label_data.append(country)
        country_data.append(count)

    if len(cn) >= 1:
        count = len(cn)
        country = cn[0].country
        label_data.append(country)
        country_data.append(count)

    if len(jp) >= 1:
        count = len(jp)
        country = jp[0].country
        label_data.append(country)
        country_data.append(count)

    if len(idon) >= 1:
        count = len(idon)
        country = idon[0].country
        label_data.append(country)
        country_data.append(count)

    if len(uk) >= 1:
        count = len(uk)
        country = uk[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Myanmar) >= 1:
        count = len(Myanmar)
        country = Myanmar[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Australia) >= 1:
        count = len(Australia)
        country = Australia[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Austria) >= 1:
        count = len(Austria)
        country = Austria[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Slovakia) >= 1:
        count = len(Slovakia)
        country = Slovakia[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Slovenia) >= 1:
        count = len(Slovenia)
        country = Slovenia[0].country
        label_data.append(country)
        country_data.append(count)

    if len(Iran) >= 1:
        count = len(Iran)
        country = Iran[0].country
        label_data.append(country)
        country_data.append(count)

    return ({'label_data': label_data, 'country_data': country_data})


def region_queryset(request):
    region_data = []
    label_region = []
    label_country = []
    region_count = 0
    # for us
    us_colorado = models.IpAddress.objects.filter(region_code='CO')
    us_califonia = models.IpAddress.objects.filter(region_code='CA')
    us_NY = models.IpAddress.objects.filter(region_code='NY')
    us_OH = models.IpAddress.objects.filter(region_code='OH')
    us_VA = models.IpAddress.objects.filter(region_code='VA')
    us_NC = models.IpAddress.objects.filter(region_code='NC')
    us_PA = models.IpAddress.objects.filter(region_code='PA')
    us_TX = models.IpAddress.objects.filter(region_code='TX')
    us_OK = models.IpAddress.objects.filter(region_code='OK')
    us_SC = models.IpAddress.objects.filter(region_code='SC')
    # china
    china_hebei = models.IpAddress.objects.filter(region_code='42')
    china_beijing = models.IpAddress.objects.filter(region_code='11')
    china_guangdong = models.IpAddress.objects.filter(region_code='44')
    china_shanghi = models.IpAddress.objects.filter(region_code='31')
    jp_tokyo = models.IpAddress.objects.filter(region_code='13')
    au_vic = models.IpAddress.objects.filter(region_code='VIC')
    ca_on = models.IpAddress.objects.filter(region_code='ON')
    moroko_casaba = models.IpAddress.objects.filter(region_code='06')
    uk_wales = models.IpAddress.objects.filter(region_code='WLS')

    parkistan_punjab = models.IpAddress.objects.filter(region_code='PB')
    slovenia_ljb = models.IpAddress.objects.filter(region_code='061')
    iran_teheran = models.IpAddress.objects.filter(region_code='23')
    indo_jakata = models.IpAddress.objects.filter(
        region='Special Capital Region of Jakarta')

    if len(parkistan_punjab) >= 1:
        region_count = len(parkistan_punjab)
        label_region.append(parkistan_punjab[0].region)
        label_country.append(parkistan_punjab[0].country)
        region_data.append(region_count)

    if len(slovenia_ljb) >= 1:
        region_count = len(slovenia_ljb)
        label_region.append(slovenia_ljb[0].region)
        label_country.append(slovenia_ljb[0].country)
        region_data.append(region_count)

    if len(iran_teheran) >= 1:
        region_count = len(iran_teheran)
        label_region.append(iran_teheran[0].region)
        label_country.append(iran_teheran[0].country)
        region_data.append(region_count)

    if len(uk_wales) >= 1:
        region_count = len(uk_wales)
        label_region.append(uk_wales[0].region)
        label_country.append(uk_wales[0].country)
        region_data.append(region_count)

    if len(moroko_casaba) >= 1:
        region_count = len(moroko_casaba)
        label_region.append(moroko_casaba[0].region)
        label_country.append(moroko_casaba[0].country)
        region_data.append(region_count)

    if len(ca_on) >= 1:
        region_count = len(ca_on)
        label_region.append(ca_on[0].region)
        label_country.append(ca_on[0].country)
        region_data.append(region_count)

    if len(au_vic) >= 1:
        region_count = len(au_vic)
        label_region.append(au_vic[0].region)
        label_country.append(au_vic[0].country)
        region_data.append(region_count)

    if len(indo_jakata) >= 1:
        region_count = len(indo_jakata)
        label_region.append(indo_jakata[0].region)
        label_country.append(indo_jakata[0].country)
        region_data.append(region_count)

    if len(jp_tokyo) >= 1:
        region_count = len(jp_tokyo)
        label_region.append(jp_tokyo[0].region)
        label_country.append(jp_tokyo[0].country)
        region_data.append(region_count)

    if len(china_hebei) >= 1:
        region_count = len(china_hebei)
        label_region.append(china_hebei[0].region)
        label_country.append(china_hebei[0].country)
        region_data.append(region_count)

    if len(china_beijing) >= 1:
        region_count = len(china_beijing)
        label_region.append(china_beijing[0].region)
        label_country.append(china_beijing[0].country)
        region_data.append(region_count)

    if len(china_guangdong) >= 1:
        region_count = len(china_guangdong)
        label_region.append(china_guangdong[0].region)
        label_country.append(china_guangdong[0].country)
        region_data.append(region_count)

    if len(china_shanghi) >= 1:
        region_count = len(china_shanghi)
        label_region.append(china_shanghi[0].region)
        label_country.append(china_shanghi[0].country)
        region_data.append(region_count)

    if len(us_OK) >= 1:
        region_count = len(us_OK)
        label_region.append(us_OK[0].region_code)
        label_country.append(us_OK[0].country)
        region_data.append(region_count)

    if len(us_colorado) >= 1:
        region_count = len(us_colorado)
        label_region.append(us_colorado[0].region)
        label_country.append(us_colorado[0].country)
        region_data.append(region_count)

    if len(us_califonia) >= 1:
        region_count = len(us_califonia)
        label_region.append(us_califonia[0].region)
        label_country.append(us_califonia[0].country)
        region_data.append(region_count)

    if len(us_TX) >= 1:
        region_count = len(us_TX)
        label_region.append(us_TX[0].region)
        label_country.append(us_TX[0].country)
        region_data.append(region_count)

    if len(us_NY) >= 1:
        region_count = len(us_NY)
        label_region.append(us_NY[0].region)
        label_country.append(us_NY[0].country)
        region_data.append(region_count)

    if len(us_OH) >= 1:
        region_count = len(us_OH)
        label_region.append(us_OH[0].region)
        label_country.append(us_OH[0].country)
        region_data.append(region_count)

    if len(us_NC) >= 1:
        region_count = len(us_NC)
        label_region.append(us_NC[0].region)
        label_country.append(us_NC[0].country)
        region_data.append(region_count)

    if len(us_NC) >= 1:
        region_count = len(us_NC)
        label_region.append(us_NC[0].region)
        label_country.append(us_NC[0].country)
        region_data.append(region_count)

    if len(us_VA) >= 1:
        region_count = len(us_VA)
        label_region.append(us_VA[0].region)
        label_country.append(us_VA[0].country)
        region_data.append(region_count)

    if len(us_PA) >= 1:
        region_count = len(us_PA)
        label_region.append(us_PA[0].region)
        label_country.append(us_PA[0].country)
        region_data.append(region_count)

    if len(us_SC) >= 1:
        region_count = len(us_SC)
        label_region.append(us_SC[0].region)
        label_country.append(us_SC[0].country)
        region_data.append(region_count)

    return ({'region_data': region_data, 'label_region': label_region, 'label_country': label_country})


def pie_chart(request):

    data = country_queryset(request)
    label_data = data['label_data']
    country_data = data['country_data']

    return render(request, 'pie_chart.html', {
        'labels': label_data,
        'data': country_data
    })


def heap_map(request):

    data = region_queryset(request)
    region_data = data['region_data']
    label_region = data['label_region']
    label_country = data['label_country']
    print(label_region)

    return render(request, 'heap_map.html', {'label_region': label_region,
                                             'label_country': label_country
                                             })
