from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Contributions,LoansRequest
from .forms import ContributionForm,LoanRequestForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

@login_required
def index(request):
    Loans_application = LoansRequest.objects.all()
    all_contributions = Contributions.objects.all()
    loan_count = Loans_application.count()
    contribution_count = all_contributions.count()
    admins_count = User.objects.all().count()
    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.members = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = LoanRequestForm()
    context = {
    'Loans_application': Loans_application,
    'form': form,
    'all_contributions': all_contributions,
    'loan_count':loan_count,
    'contribution_count':contribution_count,
    'admins_count': admins_count
    }
    return render(request,'dashboard/index.html',context)

@login_required
def members(request):
    admins = User.objects.all()
    admins_count = admins.count()
    loan_count = LoansRequest.objects.all().count()
    contribution_count = Contributions.objects.all().count()
    context = {
    'admins': admins,
    'admins_count': admins_count,
    'loan_count': loan_count,
    'contribution_count':contribution_count
    }
    return render(request,'dashboard/members.html',context)

# ADMINS DETAILS PAGE
@login_required
def admins_details(request,pk):
    admins = User.objects.get(id=pk)
    context ={
    'admins':admins,
    }
    return render(request,'dashboard/admins_detail.html',context)


@login_required
def contributions(request):
    # USING ORM
    members_contributions = Contributions.objects.all()
    contribution_count = members_contributions.count()
    # USING SQL
    # members_contributions = Contributions.objects.raw('SELECT * FROM dashboard_contributions')
    admins_count = User.objects.all().count()
    loan_count = LoansRequest.objects.all().count()
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            form.save()
            member_name = form.cleaned_data.get('name')
            messages.success(request,f'{member_name} contribution has been added')
            return redirect('dashboard-contributions')
    else:
        form = ContributionForm()

    context ={
    'members_contributions': members_contributions,
    'form':form,
    'admins_count': admins_count,
    'loan_count': loan_count,
    'contribution_count': contribution_count,
    }
    return render(request,'dashboard/contributions.html',context)

# DELETING CONTRIBUTIONS
@login_required
def contributions_delete(request,pk):
    item = Contributions.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-contributions')
    return render(request,'dashboard/contributions_delete.html')

# UPDATING CONTRIBUTIONS
@login_required
def contributions_update(request,pk):
    item = Contributions.objects.get(id=pk)
    if request.method == 'POST':
        form = ContributionForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-contributions')
    else:
        form = ContributionForm(instance=item)
    context ={
        'form': form,
    }
    return render(request,'dashboard/contributions_update.html',context)

@login_required
def Loans(request):
    Loans_application = LoansRequest.objects.all()
    paginator = Paginator(Loans_application,10)
    page = request.GET.get('pg')
    Loans_application = paginator.get_page(page)
    loan_count = Loans_application.count(3)
    admins_count = User.objects.all().count()
    contribution_count = Contributions.objects.all().count()

    context ={
    'Loans_application': Loans_application,
    'admins_count':admins_count,
    'loan_count':loan_count,
    'contribution_count': contribution_count
    }
    return render(request,'dashboard/Loans.html',context)

@login_required
def approved_loans(request,pk):
    Loans_application = LoansRequest.objects.get(id=pk)
    Loans_application.is_approved = True
    Loans_application.save()
    return redirect('dashboard-loans')

@login_required
def pending_loans(request,pk):
    Loans_application = LoansRequest.objects.get(id=pk)
    Loans_application.is_approved = False
    Loans_application.save()
    return redirect('dashboard-loans')
