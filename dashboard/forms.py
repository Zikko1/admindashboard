from django import forms
from .models import Contributions,LoansRequest


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contributions
        fields = ['name','amount','month']


class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoansRequest
        fields = ['loan_amount']
