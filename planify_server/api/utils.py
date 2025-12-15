from django.http import JsonResponse
from .models import AuthToken

def require_token(view_func):
    def wrapped(request, *args, **kwargs):
        auth = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION')
        if not auth:
            return JsonResponse({'error': 'Missing Authorization header'}, status=401)
        if auth.startswith('Bearer '):
            token = auth.split(' ',1)[1]
        else:
            token = auth
        try:
            at = AuthToken.objects.get(key=token)
            request.current_user = at.user
        except AuthToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        return view_func(request, *args, **kwargs)
    wrapped.__name__ = view_func.__name__
    return wrapped

def project_to_dict(project):
    return{
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "members": [u.id for u in project.members.all()],
    }
def task_to_dict(task):
    return{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "state": task.state,
        "assigned_to": task.assigned_to.id if task.assigned_to else None,
        "project_id": task.project.id,
        "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else None
    }