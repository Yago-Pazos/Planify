import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User,AuthToken
from .utils import require_token


@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error':'Only POST'}, status=405)
    data = json.loads(request.body)
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not (name and email and password):
        return JsonResponse({'error':'Missing fields'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error':'Email already exists'}, status=400)

    u = User.objects.create(name=name,email=email,password=password)
    token = AuthToken.objects.create(user=u)
    return JsonResponse({'id': u.id, 'token': token.key, 'user': {'id':u.id,'name':u.name,'email':u.email}})

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error':'Only POST'}, status=405)
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    if not (email and password):
        return JsonResponse({'error':'Missing fields'}, status=400)
    try:
        u = User.objects.get(email=email, password=password)
    except User.DoesNotExist:
        return JsonResponse({'error':'Invalid credentials'}, status=401)
    token, created = AuthToken.objects.get_or_create(user=u)
    if not created:
        token.regenerate()
    return JsonResponse({'token':token.key,'user':{'id':u.id,'name':u.name,'email':u.email}})

# TODO Aquí las contraseñas se guardan sin hash (sólo para desarrollo rápido).








