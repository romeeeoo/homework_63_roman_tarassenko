from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView

from posts.forms import PostForm
from posts.models import Post


class PostIndexView(ListView):
    template_name = "index.html"
    model = Post
    context_object_name = "posts"

class CreatePostView(CreateView):
    model = Post
    template_name = "form_post.html"
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            description = form.cleaned_data.get('description')
            image = form.cleaned_data.get('image')
            Post.objects.create(author=user, description=description, image=image)
            return redirect('index')
        context = {}
        context["form"] = form
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse("index")









