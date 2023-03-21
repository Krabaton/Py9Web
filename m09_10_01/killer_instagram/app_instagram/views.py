import os

from django.shortcuts import render, redirect
from django.conf import settings

from .forms import PictureForm
from .models import Picture


# Create your views here.
def main(request):
    return render(request, 'app_instagram/index.html', context={"title": "Web 9 Group!"})


def upload(request):
    form = PictureForm(instance=Picture())
    if request.method == "POST":
        form = PictureForm(request.POST, request.FILES, instance=Picture())
        if form.is_valid():
            form.save()
            return redirect(to="app_instagram:pictures")
    return render(request, 'app_instagram/upload.html', context={"title": "Web 9 Group!", "form": form})


def pictures(request):
    pictures = Picture.objects.all()
    return render(request, 'app_instagram/pictures.html',
                  context={"title": "Web 9 Group!", "pictures": pictures, "media": settings.MEDIA_URL})


def remove(request, pic_id):
    picture = Picture.objects.filter(pk=pic_id)
    try:
        os.unlink(os.path.join(settings.MEDIA_ROOT, str(picture.first().path)))
    except OSError as e:
        print(e)
    picture.delete()
    return redirect(to="app_instagram:pictures")


def edit(request, pic_id):
    if request.method == 'POST':
        description = request.POST.get('description')
        Picture.objects.filter(pk=pic_id).update(description=description)
        return redirect(to="app_instagram:pictures")

    picture = Picture.objects.filter(pk=pic_id).first()
    return render(request, "app_instagram/edit.html",
                  context={"title": "Web 9 Group!", "pic": picture, "media": settings.MEDIA_URL})
