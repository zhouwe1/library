from django.urls import path
from .views import BookView


urlpatterns = [
    path('', BookView.as_view(), name='book_add'),
    path('', BookView.as_view(), name='book_search'),
    path('/<int:book_id>', BookView.as_view(), name='book_edit'),
    path('/<int:book_id>', BookView.as_view(), name='book_delete'),
]
