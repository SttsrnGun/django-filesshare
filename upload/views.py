import os.path
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader as template_loader
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from upload.form import DownloadForm, UploadForm
from .models import Upload
from django.core.exceptions import PermissionDenied, FieldDoesNotExist
from django.shortcuts import render


def error_400(request, exception):
    data = {}
    return render(request,"error.html", data)

def error_500(request):
    data = {}
    return render(request,"error.html", data)
    
class UploadView(CreateView):
    model = Upload
    form_class = UploadForm
    template_name  = "upload/upload_form.html"

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("login")        
        return super().post(self, request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.expired_at = timezone.now() + timedelta(seconds=int(self.request.POST.get("expire_duration")))
        form.instance.name = self.request.FILES["file"].name
        if self.request.POST["password"]:
            form.instance.password = make_password(self.request.POST["password"])
            
        return super().form_valid(form)


class UploadDetailView(DetailView):
    model = Upload
    template_name = "upload/upload_detail.html"
    
    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_delete=False)
        return query


class DownloadView(UpdateView):
    model = Upload
    form_class = DownloadForm
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not os.path.exists(self.object.file.path): # check file exists
            raise PermissionDenied

        return super().post(self, request, *args, **kwargs)
        
    def form_valid(self, form):
        self.object = self.get_object()
        if form.data.__contains__("password"):
            self.object.perform_download(password=form.data["password"])
        else:
            self.object.perform_download()

        return download_file(self.object.file.path, self.object.name)
        # return super().form_valid(form)


def download_file(file_path, file_name):
    # https://gist.github.com/MhmdRyhn/820e3277c157098655dd3ae117be4285
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(
                fh.read(),
            )
            response["Content-Disposition"] = "attachment; filename=%s" % file_name
        return response
    else:
        raise FieldDoesNotExist

class DeleteView(DeleteView):
    model = Upload
    template_name  = "upload/delete.html"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user:
            raise PermissionDenied
        return super().post(self, request, *args, **kwargs)

    def get_success_url(self):
        return reverse("list")

@login_required
def ListView(request):
    upload_object = Upload.objects.filter(user=request.user).exclude(is_delete=True).all()

    current_page = request.GET.get("page", 1)
    paginator = Paginator(upload_object, 10)
    page_obj = paginator.get_page(current_page)
    page_range = paginator.get_elided_page_range(number=current_page)
    
    template = template_loader.get_template("upload/list.html")
    context = {
        "upload": upload_object,
        "page_obj": page_obj,
        "page_range": page_range,
    }
    return HttpResponse(template.render(context, request))