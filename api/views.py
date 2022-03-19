from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from upload.models import Upload


def clearFile(request):
    if "app" in request.META["HTTP_HOST"]: # this function allow only request call from http://...app.../ (container network)
        upload_object = Upload.objects.filter(
            Q(is_delete=False),
            Q(max_downloads__lte=0) | Q(expired_at__lte=timezone.now())
        )
    else:
        raise PermissionDenied("the request not allowed")

    for item in upload_object:
        print(item)
        item.delete()
        
    return HttpResponse("success")
