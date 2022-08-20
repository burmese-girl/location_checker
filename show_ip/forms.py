
from ipaddress import ip_address
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from . import models
import re


LANGUAGES = ((1, "English"),)


class UserDetailAdminForm(forms.ModelForm):
    GENDER = [('', _('-----------')), ('MALE', 'MALE'), ('FEMALE', 'FEMALE')]
    LANGUAGE = ((1, 'English'))
    NATIONALITY_CHOICES = [
        ('', _('-----------')),
        ('MM', _('BURMESE')),
        ('AF', _('AFGHAN')),
        ('AL', _('ALBANIAN')),
        ('DZ', _('ALGERIAN')),
        ('US', _('AMERICAN')),
        ('AD', _('ANDORRAN')),
        ('AO', _('ANGOLAN')),
        ('AG', _('ANTIGUANS OR BARBUDANS')),
        ('AR', _('ARGENTINEAN')),
        ('AM', _('ARMENIAN')),
        ('AU', _('AUSTRALIAN')),
        ('AT', _('AUSTRIAN')),
        ('AZ', _('AZERBAIJANI')),
        ('BS', _('BAHAMIAN')),
        ('BH', _('BAHRAINI')),
        ('BD', _('BANGLADESHI')),
        ('BB', _('BARBADIAN')),
        ('BW', _('BATSWANA')),
        ('BY', _('BELARUSIAN')),
        ('BE', _('BELGIAN')),
        ('BZ', _('BELIZEAN')),
        ('BJ', _('BENINESE')),
        ('BT', _('BHUTANESE')),
        ('BO', _('BOLIVIAN')),
        ('BA', _('BOSNIAN OR HERZEGOVINIAN')),
        ('BR', _('BRAZILIAN')),
        ('GB-ENG', _('BRITISH')),
        ('BN', _('BRUNEIAN')),
        ('BG', _('BULGARIAN')),
        ('BF', _('BURKINABE')),
        ('BI', _('BURUNDIAN')),
        ('KH', _('CAMBODIAN')),
        ('CM', _('CAMEROONIAN')),
        ('CA', _('CANADIAN')),
        ('CV', _('CAPE VERDEAN')),
        ('CF', _('CENTRAL AFRICAN')),
        ('TD', _('CHADIAN')),
        ('CL', _('CHILEAN')),
        ('CN', _('CHINESE')),
        ('CO', _('COLOMBIAN')),
        ('KM', _('COMORAN')),
        ('CG', _('CONGOLESE')),
        ('CR', _('COSTA RICAN')),
        ('HR', _('CROATIAN')),
        ('CU', _('CUBAN')),
        ('CY', _('CYPRIOT')),
        ('CZ', _('CZECH')),
        ('DK', _('DANISH')),
        ('DJ', _('DJIBOUTI')),
        ('DO', _('DOMINICAN')),
        ('NL', _('DUTCH')),
        ('TL', _('EAST TIMORESE')),
        ('EC', _('ECUADOREAN')),
        ('EG', _('EGYPTIAN')),
        ('AE', _('EMIRIAN')),
        ('GQ', _('EQUATORIAL GUINEAN')),
        ('ER', _('ERITREAN')),
        ('EE', _('ESTONIAN')),
        ('ET', _('ETHIOPIAN')),
        ('FJ', _('FIJIAN')),
        ('PH', _('FILIPINO')),
        ('FI', _('FINNISH')),
        ('FR', _('FRENCH')),
        ('GA', _('GABONESE')),
        ('GM', _('GAMBIAN')),
        ('GE', _('GEORGIAN')),
        ('DE', _('GERMAN')),
        ('GH', _('GHANAIAN')),
        ('GR', _('GREEK')),
        ('GD', _('GRENADIAN')),
        ('GT', _('GUATEMALAN')),
        ('GW', _('GUINEA-BISSAUAN')),
        ('GN', _('GUINEAN')),
        ('GY', _('GUYANESE')),
        ('HT', _('HAITIAN')),
        ('HN', _('HONDURAN')),
        ('HU', _('HUNGARIAN')),
        ('KI', _('I-KIRIBATI')),
        ('IS', _('ICELANDER')),
        ('IN', _('INDIAN')),
        ('ID', _('INDONESIAN')),
        ('IR', _('IRANIAN')),
        ('IQ', _('IRAQI')),
        ('IE', _('IRISH')),
        ('IL', _('ISRAELI')),
        ('IT', _('ITALIAN')),
        ('CI', _('IVORIAN')),
        ('JM', _('JAMAICAN')),
        ('JP', _('JAPANESE')),
        ('JO', _('JORDANIAN')),
        ('KZ', _('KAZAKHSTANI')),
        ('KE', _('KENYAN')),
        ('KN', _('KITTIAN AND NEVISIAN')),
        ('KW', _('KUWAITI')),
        ('KG', _('KYRGYZ')),
        ('LA', _('LAOTIAN')),
        ('LV', _('LATVIAN')),
        ('LB', _('LEBANESE')),
        ('LR', _('LIBERIAN')),
        ('LY', _('LIBYAN')),
        ('LI', _('LIECHTENSTEINER')),
        ('LT', _('LITHUANIAN')),
        ('LU', _('LUXEMBOURGER')),
        ('MK', _('MACEDONIAN')),
        ('MG', _('MALAGASY')),
        ('MW', _('MALAWIAN')),
        ('MY', _('MALAYSIAN')),
        ('MV', _('MALDIVAN')),
        ('ML', _('MALIAN')),
        ('MT', _('MALTESE')),
        ('MH', _('MARSHALLESE')),
        ('MR', _('MAURITANIAN')),
        ('MU', _('MAURITIAN')),
        ('MX', _('MEXICAN')),
        ('FM', _('MICRONESIAN')),
        ('MD', _('MOLDOVAN')),
        ('MC', _('MONACAN')),
        ('MN', _('MONGOLIAN')),
        ('MA', _('MOROCCAN')),
        ('LS', _('MOSOTHO')),
        ('MZ', _('MOZAMBICAN')),
        ('NA', _('NAMIBIAN')),
        ('NR', _('NAURUAN')),
        ('NP', _('NEPALESE')),
        ('NZ', _('NEW ZEALANDER')),
        ('NI', _('NICARAGUAN')),
        ('NG', _('NIGERIAN')),
        ('NE', _('NIGERIEN')),
        ('KP', _('NORTH KOREAN')),
        ('GB-NIR', _('NORTHERN IRISH')),
        ('NO', _('NORWEGIAN')),
        ('OM', _('OMANI')),
        ('PK', _('PAKISTANI')),
        ('PW', _('PALAUAN')),
        ('PA', _('PANAMANIAN')),
        ('PG', _('PAPUA NEW GUINEAN')),
        ('PY', _('PARAGUAYAN')),
        ('PE', _('PERUVIAN')),
        ('PL', _('POLISH')),
        ('PT', _('PORTUGUESE')),
        ('QA', _('QATARI')),
        ('RO', _('ROMANIAN')),
        ('RU', _('RUSSIAN')),
        ('RW', _('RWANDAN')),
        ('LC', _('SAINT LUCIAN')),
        ('SV', _('SALVADORAN')),
        ('WS', _('SAMOAN')),
        ('SM', _('SAN MARINESE')),
        ('ST', _('SAO TOMEAN')),
        ('SA', _('SAUDI')),
        ('GB-SCT', _('SCOTTISH')),
        ('SN', _('SENEGALESE')),
        ('RS', _('SERBIAN')),
        ('SC', _('SEYCHELLOIS')),
        ('SL', _('SIERRA LEONEAN')),
        ('SG', _('SINGAPOREAN')),
        ('SK', _('SLOVAKIAN')),
        ('SI', _('SLOVENIAN')),
        ('SB', _('SOLOMON ISLANDER')),
        ('SO', _('SOMALI')),
        ('ZA', _('SOUTH AFRICAN')),
        ('KR', _('SOUTH KOREAN')),
        ('ES', _('SPANISH')),
        ('LK', _('SRI LANKAN')),
        ('SD', _('SUDANESE')),
        ('SR', _('SURINAMER')),
        ('SZ', _('SWAZI')),
        ('SE', _('SWEDISH')),
        ('CH', _('SWISS')),
        ('SY', _('SYRIAN')),
        ('TW', _('TAIWANESE')),
        ('TJ', _('TAJIK')),
        ('TZ', _('TANZANIAN')),
        ('TH', _('THAI')),
        ('TG', _('TOGOLESE')),
        ('TO', _('TONGAN')),
        ('TT', _('TRINIDADIAN OR TOBAGONIAN')),
        ('TN', _('TUNISIAN')),
        ('TR', _('TURKISH')),
        ('TV', _('TUVALUAN')),
        ('UG', _('UGANDAN')),
        ('UA', _('UKRAINIAN')),
        ('UY', _('URUGUAYAN')),
        ('UZ', _('UZBEKISTANI')),
        ('VE', _('VENEZUELAN')),
        ('VN', _('VIETNAMESE')),
        ('GB-WLS', _('WELSH')),
        ('YE', _('YEMENITE')),
        ('ZM', _('ZAMBIAN')),
        ('ZW', _('ZIMBABWEAN')),
        ('99', _('OTHER'))
    ]
    # confirm_temp_email = forms.CharField(max_length=254, required=False)
    gender = forms.ChoiceField(choices=GENDER, required=False)

    def __init__(self, *args, **kwargs):
        super(UserDetailAdminForm, self).__init__(*args, **kwargs)

        self.fields['language'] = forms.ChoiceField(
            choices=self.LANGUAGE)


class AuthenticateExtraForm(AuthenticationForm):

    username = forms.CharField(max_length=254, widget=forms.TextInput(
        attrs={'placeholder': ("Email")}))
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(
        attrs={'placeholder': ("Password")}))


class SingupForm(forms.Form):
    email = forms.CharField(label=('Email'), widget=forms.TextInput(
        attrs={'class': 'form-control override-form', 'placeholder': ("Email")}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': ("New Password")}), label=('Password'), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': ("Confirm Password")}), label=('Confirm Password'), required=False)

    first_name = forms.CharField(label=('First name',),
                                 widget=forms.TextInput(attrs={'class': 'form-control override-form', 'placeholder': ("First name")}))
    last_name = forms.CharField(label=('Surname'),
                                widget=forms.TextInput(attrs={'class': 'form-control override-form', 'placeholder': ("Surname")}))
    country_code = forms.CharField(label=('Country Code'), required=False,
                                   widget=forms.TextInput(
                                       attrs={'placeholder': ('Country Code'), 'class': 'form-control override-form'}))
    mobile = forms.CharField(label=('Phone Number'), required=False,
                             widget=forms.TextInput(
        attrs={'placeholder': ('Phone Number'), 'class': 'form-control override-form'}))

    gender = forms.ChoiceField(initial="", choices=models.gender_choices, label=('Gender'),
                               widget=forms.RadioSelect(attrs={'class': 'btn btn-radio', 'placeholder': ('Gender')}))

    dob = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
                               'class': 'datepicker form-control override-form', 'placeholder': ('Date Of Birth')}),
        label=('Date Of Birth'))
    address = forms.CharField(label=('Address'), widget=forms.TextInput(attrs={'class': 'form-control override-form'}),
                              required=False)

    def __init__(self, *args, **kwargs):
        super(SingupForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget.attrs['readonly'] = True

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
            raise forms.ValidationError(('Invalid email format.'))

        # if len(email) > 30:
        # 	raise forms.ValidationError(('Ensure this value has at most 30 characters.'))

        user = User.objects.filter(username=email).count()
        if user > 0:
            raise forms.ValidationError(('Email exists.'))

        return self.cleaned_data.get('email')

    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')

        if phone_num and not phone_num.isdigit():
            raise forms.ValidationError(('Invalid format.'))

        if len(phone_num) > 30:
            raise forms.ValidationError(
                ('Ensure this value has at most 30 characters.'))

        return self.cleaned_data.get('phone_num')

    def clean_country_code(self):
        country_code = self.cleaned_data.get('country_code')
        if len(country_code) > 6:
            raise forms.ValidationError(
                ('Ensure this value has at most 6 characters.'))

        return self.cleaned_data.get('country_code')


class ProfileForm(forms.ModelForm):

    name = forms.CharField(required=False, max_length=256, label="Name",
                           widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    gender = forms.ChoiceField(required=False, initial="", choices=(
        ('', ' '),)+models.gender_choices, label="Gender",)
    mobile = forms.CharField(required=False, max_length=256, label="Phone No.",
                             widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    country_code = forms.CharField(
        required=False, max_length=256, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    dob = forms.DateField(input_formats=['%Y-%m-%d'], required=False,
                          label="Date Of Birth", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    language = forms.ChoiceField(
        choices=LANGUAGES, label="Languages", required=False,)

    class Meta:

        model = models.UserProfile
        exclude = ('id', 'user', 'active_user')


class IPSearchForm(forms.ModelForm):

    ip_address = forms.CharField(max_length=254, widget=forms.TextInput(
        attrs={'placeholder': ("Search IP Address Here")}))

    class Meta:
        model = models.IpAddress
        exclude = ('id',)
