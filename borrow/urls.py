from django.urls import path
from . import views


urlpatterns = [
    path('/borrowing', views.borrowing, name='borrow_borrowing'),
    path('/returning', views.returning, name='borrow_returning'),
]
