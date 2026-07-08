from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    # Check if a country change was requested via GET — redirect so CSRF token refreshes
    country = request.GET.get('country')
    if country:
        request.session['selected_country'] = country
        return redirect('login')

    if request.method == 'POST' and 'username' in request.POST:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard_redirect')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    selected_country = request.session.get('selected_country', 'IN')
    country_currencies = {
        'IN': {'name': 'India', 'symbol': '₹', 'silver': '50,000', 'gold': '75,000', 'platinum': '1,00,000', 'tax': 'GST'},
        'US': {'name': 'United States', 'symbol': '$', 'silver': '699', 'gold': '999', 'platinum': '1,399', 'tax': 'Sales Tax'},
        'GB': {'name': 'United Kingdom', 'symbol': '£', 'silver': '599', 'gold': '849', 'platinum': '1,199', 'tax': 'VAT'},
        'CA': {'name': 'Canada', 'symbol': 'C$', 'silver': '899', 'gold': '1,299', 'platinum': '1,799', 'tax': 'HST/GST'},
        'EU': {'name': 'Europe', 'symbol': '€', 'silver': '649', 'gold': '899', 'platinum': '1,249', 'tax': 'VAT'},
    }
    active_currency = country_currencies.get(selected_country, country_currencies['IN'])
    
    return render(request, 'accounts/login.html', {
        'form': form,
        'selected_country': selected_country,
        'country_currencies': country_currencies,
        'active_currency': active_currency,
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_redirect(request):
    role = request.user.role
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'principal':
        return redirect('principal_dashboard')
    elif role == 'teacher':
        return redirect('teacher_dashboard')
    elif role == 'student':
        return redirect('student_dashboard')
    elif role == 'parent':
        return redirect('parent_dashboard')
    elif role == 'accountant':
        return redirect('accountant_dashboard')
    else:
        return redirect('login')
