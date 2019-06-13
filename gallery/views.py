from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Image, PhotoBook
from .forms import ImageCreateForm

# Create your views here.
class ImageView(DetailView):
    model = Image
    template_name = 'image_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        context['photobook_images'] = []
        context['ppk'] = self.kwargs.get('ppk')
        
        context['next_image'] = None
        context['previous_image'] = None
        
        """
        if there is a photobook in the context, look up the images in it
        """
        if context['ppk']:
            context['photobook'] = PhotoBook.objects.get(pk=context['ppk'])
            images = context['photobook'].images.all()
            photobook_images = sorted(images, key=lambda i: i.date_taken)
            context['photobook_images'] = photobook_images
            for i in range(len(photobook_images)):
                if self.object.pk == photobook_images[i].pk:
                    if i > 0:
                        context['previous_image'] = photobook_images[i - 1]
                    if i < len(photobook_images) - 1:
                        context['next_image'] = photobook_images[i + 1]
        else:
            """ look for photobooks this image appears in """
            context['photobooks'] = self.object.image_photobooks.all()
            
        return context
    

class ImageList(ListView):
    model = Image
    context_object_name = 'images_list'
    template_name = 'image_list.html'
    
    def get_queryset(self):
        """ order by latest first """
        return super(ImageList, self).get_queryset().order_by('-pk')
    
    
class ImageCreate(LoginRequiredMixin, FormView):
    
    login_url = reverse_lazy('login')
    form_class = ImageCreateForm
    template_name = 'image_upload.html'
    
    def form_valid(self, form):
        """
        Bulk create images based on form data
        """
        image_data = form.files.getlist('data')
        for data in image_data:
            image = Image.objects.create(data=data)
            image.image_photobooks.add(form.data['ppk'])
        messages.success(self.request, "Images added successfully")
        return super().form_valid(form)
        
    def get_success_url(self):
        next_url = self.request.POST.get('next')
        return_url = reverse('gallery:images_list')
        if next_url:
            return_url = next_url
        return return_url
        
    def form_invalid(self, form):
        response = super().form_invalid(form)
        next_url = self.request.POST.get('next')
        if next_url:
            """ TODO: preserve error message """
            return redirect(next_url)
        else:
            return response
        
        
class PhotoBookView(DetailView):
    model = PhotoBook
    context_object_name = 'photobook'
    template_name = 'photobook_detail.html'
    
    def get_queryset(self):
        photobook = super(PhotoBookView, self).get_queryset()
        return photobook
        
    def get_context_data(self, **kwargs):
        context = super(PhotoBookView, self).get_context_data(**kwargs)
        images = context['photobook'].images.all()
        context['images'] = sorted(images, key=lambda i: i.date_taken)
        return context
    
    
class PhotoBookList(ListView):
    model = PhotoBook
    context_object_name = 'photobooks_list'
    template_name = 'photobook_list.html'