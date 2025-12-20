from django.contrib.auth import authenticate
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
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    print("REGISTER BODY:", request.body)

    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({'error': 'Missing fields'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'User already exists'}, status=400)

    # REGISTRO SIMPLE (password en claro, desarrollo DAM)
    user = User.objects.create(
        email=email,
        password=password
    )

    return JsonResponse({
        'id': user.id,
        'email': user.email
    }, status=201)

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({'error': 'Missing fields'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    # COMPARACIÓN DIRECTA (DESARROLLO)
    if user.password != password:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({
        'user': {
            'id': user.id,
            'email': user.email
        }
    }, status=200)


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

@csrf_exempt
def projects_list(request):
    if request.method == "GET":
        projects = Project.objects.all()
        data = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description
            }
            for p in projects
        ]
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        print("POST RECIBIDO:", request.body)
        try:
            data = json.loads(request.body)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        name = data.get("name")
        description = data.get("description", "")

        if not name:
            return JsonResponse({"error": "Name is required"}, status=400)

        project = Project.objects.create(
            name=name,
            description=description
        )

        return JsonResponse({
            "id": project.id,
            "name": project.name,
            "description": project.description
        }, status=201)



@csrf_exempt
def project_detail(request, project_id):
    def project_detail(request, project_id):
        """
        Endpoint REST para operaciones sobre un proyecto concreto.

        Métodos soportados:
        - GET: devuelve los datos del proyecto
        - PUT: actualiza el proyecto
        - DELETE: elimina el proyecto

        Parámetros:
        - project_id (int): identificador del proyecto (path param)

        Respuestas:
        - 200: operación correcta
        - 404: proyecto no encontrado
        """
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Proyecto no encontrado"}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "id": project.id,
            "name": project.name,
            "description": project.description
        })

    elif request.method == "PUT":
        data = json.loads(request.body)
        project.name = data.get("name", project.name)
        project.description = data.get("description", project.description)
        project.save()
        return JsonResponse({
            "id": project.id,
            "name": project.name,
            "description": project.description
        })

    elif request.method == "DELETE":
        project.delete()
        return JsonResponse({"deleted": True})

    return JsonResponse({"error": "Método no permitido"}, status=405)
