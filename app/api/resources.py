from simple_rest import Resource
from django.http import JsonResponse

from api.models import Shot
from api.utils import resource_wrapper


class ApiResource(Resource):

    @resource_wrapper
    def get(self, request):
        shots = []
        for s in Shot.objects.all():
            shots.append(s.as_dict())
        return JsonResponse({'status': 200,
                             'data': shots}, status=200)
