from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import User, AuthToken, Project, Task
from .utils import require_token
from .utils import project_to_dict, task_to_dict

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
    if len(password) < 6:
        return JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error':'Email exists'}, status=400)

    hashed = make_password(password)
    u = User.objects.create(name=name, email=email, password=hashed)
    token = AuthToken.objects.create(user=u)

    return JsonResponse({'id': u.id, 'token': token.key, 'user': {'id': u.id, 'name': u.name, 'email': u.email}})

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
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error':'Invalid credentials'}, status=401)

    if not check_password(password, u.password):
        return JsonResponse({'error':'Invalid credentials'}, status=401)

    token, created = AuthToken.objects.get_or_create(user=u)
    if not created:
        token.regenerate()

    return JsonResponse({'token': token.key, 'user': {'id': u.id, 'name': u.name, 'email': u.email}})


# TODO Aquí las contraseñas se guardan sin hash (sólo para desarrollo rápido).


@csrf_exempt
@require_token

def task_list(request, project_id):
    project = get_object_or_404(Project, pk = project_id)

    if request.method == 'GET':
        estado = request.GET.get('estado')
        task = project.tasks.all()
        if estado:
            task = task.filter(state=estado)
        return JsonResponse([task_to_dict(t) for t in task ], safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        title = data.get('title', '').strip()
        description = data.get('description', '')
        state = data.get('state', 'todo')
        assigned_to_id = data.get('assigned_to')

        if not title or len (title) < 3:
            return JsonResponse({'error': 'Task title must be at least 3 characters'}, status=400)

        if state not in ['todo','doing' ,'done']:
            return JsonResponse({'error': 'Invalid task state'}, status=400)

        assigned_to = None
        if assigned_to_id:
            assigned_to = get_object_or_404(User, pk=assigned_to_id)

        task = Task.objects.create(
            project=project,
            title=title,
            description=description,
            state=state,
            assigned_to=assigned_to
        )

        return JsonResponse(task_to_dict(task), status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
@require_token
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'GET':
        return JsonResponse(task_to_dict(task))

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if 'title' in data:
            title = data.get('title', '').strip()
            if not title or len(title) < 3:
                return JsonResponse(
                    {'error': 'Task title must be at least 3 characters'},
                    status=400
                )
            task.title = title

        if 'description' in data:
            task.description = data['description']

        if 'state' in data:
            if data['state'] not in ['todo', 'doing', 'done']:
                return JsonResponse({'error': 'Invalid task state'}, status=400)
            task.state = data['state']

        if 'assigned_to' in data:
            if data['assigned_to'] is None:
                task.assigned_to = None
            else:
                task.assigned_to = get_object_or_404(
                    User, pk=data['assigned_to']
                )

        task.save()
        return JsonResponse(task_to_dict(task))

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'ok': True})

    return JsonResponse({'error': 'Method not allowed'}, status=405)
















