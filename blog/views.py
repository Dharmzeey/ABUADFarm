from django.urls import reverse_lazy, reverse
from utils.mixins import AdminRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

from .models import Blog


class BlogView(ListView):
    template_name = "blog/blog.html"
    model = Blog
    context_object_name = "blog"
    paginate_by = 20
blog = BlogView.as_view()

class BlogDetailsView(DetailView):
    model = Blog
    template_name = 'blog/blog-details.html'
    def get_context_data(self, **kwargs):
        random_blogs = Blog.objects.all().order_by('?')[:3]
        data = super().get_context_data(**kwargs)
        data['random_blogs'] = random_blogs
        return data
blog_details = BlogDetailsView.as_view()

class CreateBlog(AdminRequiredMixin, CreateView):
  model = Blog
  template_name = "blog/blog_form.html"
  success_url = reverse_lazy("blog:blogs")
  fields = ["title", "image", "body"]
create_blog = CreateBlog.as_view()
  
class UpdateBlog(AdminRequiredMixin, UpdateView):
  model = Blog
  fields = ["title", "image", "body"]
  template_name = "blog/blog_form.html"
  success_url = reverse_lazy("blog:blogs")
  
  def get_success_url(self):
    if 'slug' in self.kwargs:
      slug = self.kwargs['slug']
    else:
      return reverse_lazy("blog:blogs")
    return reverse('blog:blog_details', kwargs={'slug': slug})
update_blog = UpdateBlog.as_view()
  
class DeleteBlog(AdminRequiredMixin, DeleteView):
  model = Blog
  success_url = reverse_lazy("blog:blogs")
  template_name = "blog/delete_blog.html"
delete_blog = DeleteBlog.as_view()