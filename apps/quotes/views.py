from django.shortcuts import render, HttpResponse, redirect
from .models import User, Quote
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'quotes/index.html')

def register(request):
    if request.method == 'POST':
        data = {
            'name': request.POST['name'],
            'alias': request.POST['alias'],
            'e_address': request.POST['email'],
            'pass_word': request.POST['password'],
            'confirm_pass_word': request.POST['pw_confirm'],
            'dob': request.POST['birthday'],
        }
        new_user = User.objects.reg(data)
        if new_user['error_list']: #connected to lines 39 and 45 in models.py
            for error in new_user['error_list']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
        else:
            request.session['user_id'] = new_user['new'].id
            request.session['alias'] = new_user['new'].alias
            return redirect('/dashboard')

def login(request):
    if request.method == 'POST':
        data = {
            'e_mail': request.POST['email'],
            'p_word': request.POST['password'],
        }
        a_user = User.objects.log(data)
        if a_user['list_errors']: #connected to lines 39 and 45 in models.py
            for error in a_user['list_errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
        else:
            request.session['user_id'] = a_user['logged_user'].id
            request.session['alias'] = a_user['logged_user'].alias
            return redirect('/dashboard')

def dashboard(request):
    current_user = User.objects.get(id=request.session['user_id'])
    favorites = Quote.objects.filter(favorite = current_user)
    not_favorites = Quote.objects.exclude(favorite = current_user)
    context = {
        'user_favorites': favorites,
        'other_quotes': not_favorites,
    }
    return render(request, 'quotes/dashboard.html', context)

def add_quote(request):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.session['user_id'], alias=request.session['alias'])
        data = {
            'author': request.POST['author'],
            'quote': request.POST['quote'],
            'creator': current_user,
            'favorite': current_user,
        }
        new_quote = Quote.objects.new(data)
        if new_quote['error_list']: #connected to lines 39 and 45 in models.py
            for error in new_quote['error_list']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')

def posted_by(request, user_id):
    user = User.objects.filter(id=user_id)
    all_quotes = Quote.objects.all()
    user_quotes = Quote.objects.filter(creator=user)
    count = len(user_quotes)
    context = {
        "quotes": user_quotes,
        "count": count,
    }
    return render(request, 'quotes/posts.html', context)

def add_favorite(request, quote_id):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.session['user_id'])
        quote = Quote.objects.get(id = quote_id)
        quote.favorite.add(current_user)
        return redirect('/dashboard')

def remove_favorite(request, quote_id):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.session['user_id'])
        quote = Quote.objects.get(id = quote_id)
        quote.favorite.remove(current_user)
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')
