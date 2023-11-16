from django.shortcuts import render, redirect

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, InsecureUser
import json
from .forms import UserForm


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    user = User.objects.filter(username=username, password=password).first()

    if user:
        return JsonResponse({"status": "logged in"})
    else:
        return JsonResponse({"status": "invalid credentials"})


def json_convert(request):
    return render(request, 'json_conversion.html')

@csrf_exempt
def make_user(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user_json_string = f'{{"account_type": "user", "username": "{username}", "password": "{password}"}}'

        try:
            input_data = json.loads(user_json_string)

            new_user = InsecureUser(user_data=input_data)
            new_user.save()

            request.session['user_id'] = new_user.id
            return redirect('login')

        except json.JSONDecodeError:
            return JsonResponse({"status": "Invalid JSON"}, status=400)

    form = UserForm()
    # {'form': form}
    return render(request, 'user_registration.html', )

@csrf_exempt
def safe_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user_dict = {
                "account_type": "user",
                "username": username,
                "password": password
            }

            try:

                new_user = InsecureUser(user_data=user_dict)
                new_user.save()

                request.session['user_id'] = new_user.id
                return redirect('login')

            except Exception as e:

                return JsonResponse({"status": "Error", "message": str(e)}, status=400)

    form = UserForm()

    return render(request, 'user_registration.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Fetch the user from the database
            user = InsecureUser.objects.get(user_data__username=username)

            # Check the password (this is insecure!)
            if user.user_data.get('password') == password:
                # You can set the user ID in the session to keep the user logged in
                request.session['user_id'] = user.id

                if user.user_data.get('account_type') == 'administrator':
                    return redirect('admin_home')
                else:
                    return redirect('home')

            else:
                return HttpResponse('Invalid password')
        except InsecureUser.DoesNotExist:
            return HttpResponse('Invalid username')

    return render(request, 'login.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def home(request):
    return render(request, 'home.html')
