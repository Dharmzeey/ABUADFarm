from django.urls import reverse_lazy, reverse
from utils.mixins import AdminRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import News


class NewsView(ListView):
    template_name = "news/news.html"
    model = News
    context_object_name = "news"
    paginate_by = 20
news = NewsView.as_view()

class NewsDetailsView(DetailView):
    model = News
    template_name = 'news/news-details.html'
news_details = NewsDetailsView.as_view()

class CreateNews(AdminRequiredMixin, CreateView):
  model = News
  fields = ["title", "body"]
  template_name = "news/news_form.html"
  success_url = reverse_lazy("news:news")
create_news = CreateNews.as_view()
  
class UpdateNews(AdminRequiredMixin, UpdateView):
  model = News
  fields = ["title", "body"]
  template_name = "news/news_form.html"
  success_url = reverse_lazy("news:news")
  
  def get_success_url(self):
    if 'slug' in self.kwargs:
      slug = self.kwargs['slug']
    else:
      return reverse_lazy("news:news")
    return reverse('news:news_details', kwargs={'slug': slug})
update_news = UpdateNews.as_view()

class DeleteNews(AdminRequiredMixin, DeleteView):
  model = News
  success_url = reverse_lazy("news:news")
  template_name = "news/delete_news.html"
delete_news = DeleteNews.as_view()