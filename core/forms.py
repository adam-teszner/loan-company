from .models import Customer, Adress, UserInfo, Workplace, Product
from django import forms
from django.forms.widgets import *
from django.contrib.auth.forms import (
    UserChangeForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from .widgets import MyFileInput

# localflavor
from .validators import (
    PESELwithoutChecksum,
    IDwithoutChecksum,
    NIPwithoutChecksum,
    PhoneNumberField,
)


class CustCreateAdressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustCreateAdressForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class": "pyl-input"})

    class Meta:
        fields = "__all__"
        model = Adress

        labels = {
            "building_no": "Building no/flat no"
        }


class CustCreatePersonalInfo(forms.ModelForm):
    social_security_no_pesel = PESELwithoutChecksum()
    id_passport = IDwithoutChecksum()
    phone_no = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(CustCreatePersonalInfo, self).__init__(*args, **kwargs)

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class": "pyl-input"})
        self.fields["social_security_no_pesel"].widget.attrs.update(
            {"onfocusout": "checkPesel()"}
        )

    class Meta:
        fields = [
            "first_name",
            "last_name",
            "dob",
            "gender",
            "social_security_no_pesel",
            "id_passport",
            "martial_status",
            "phone_no",
            "email",
            "esd",
            "work_status",
            "salaty",
            "position",
        ]
        model = Customer
        widgets = {
            "dob": DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "gender": Select(attrs={"class": "pyl-input"}),
            "social_security_no_pesel": NumberInput(
                attrs={"onfocusout": "checkPesel()"}
            ),
            "esd": DateInput(format="%Y-%m-%d", attrs={"type": "date"})
        }
        labels = {
            "gender": "Sex",
            "social_security_no_pesel": "PESEL",
            "id_passport": "ID no. or Passport no.",
            "phone_no": "Mobile phone number",
            "email": "Email adress",
            "work_status": "Income source",
            "esd": "Employment start date",
            "salaty": "Net Income",
            "position": "Job Position"
        }


class CustCreatePersonalInfoUpdate(CustCreatePersonalInfo):
    class Meta(CustCreatePersonalInfo.Meta):
        exclude = ("first_name", "gender", "dob", "social_security_no_pesel")


class CustomWorkplaceForm(forms.ModelForm):
    id_nip = NIPwithoutChecksum()
    phone_no = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(CustomWorkplaceForm, self).__init__(*args, **kwargs)
        self.auto_id = "workplace_id_%s"
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class": "pyl-input"})

    class Meta:
        model = Workplace
        exclude = ["adress"]
        labels = {
            "id_nip": "NIP",
            "name": "Company Name",
            "email": "Email adress"
            }


class AddNewProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class": "pyl-input"})

    class Meta:
        model = Product
        exclude = (
            "created_date",
            "owner",
        )


class CustomSignUpForm(forms.ModelForm):
    social_security_no_pesel = PESELwithoutChecksum()
    id_passport = IDwithoutChecksum()
    phone_no = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            if name == "profile_pic":
                self.fields[name].widget.attrs.update(
                    {"class": "img-field", "accept": "image/*"}
                )
                continue
            if name == "information":
                self.fields[name].widget.attrs.update(
                    {"class": "pyl-text-area"})
                continue
            self.fields[name].widget.attrs.update({"class": "pyl-input"})
        self.fields["social_security_no_pesel"].widget.attrs.update(
                                                        {"type": "number"})

    class Meta:
        model = UserInfo
        fields = [
            "first_name",
            "last_name",
            "dob",
            "gender",
            "social_security_no_pesel",
            "id_passport",
            "phone_no",
            "information",
            "profile_pic",
        ]

        widgets = {
            "profile_pic": MyFileInput,
            "dob": DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }


class ChangeUsername(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "pyl-input", "label": "User login"}
        )
        self.fields["email"].widget.attrs.update({"class": "pyl-input"})

    class Meta(UserChangeForm.Meta):
        fields = ["username", "email"]


class CustomLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class": "pyl-input"})


class CustomPasswordResetFrorm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "pyl-input"})


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class": "pyl-input"})


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class": "pyl-input"})


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class": "pyl-input"})

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
