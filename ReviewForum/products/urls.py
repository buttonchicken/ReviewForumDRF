from django.urls import path
from .views import *

urlpatterns = [
    path('view',ViewProducts.as_view()),
    path('viewbyID',ViewProductbyID.as_view()),
    path('create',CreateProduct.as_view()),
    path('edit',EditProduct.as_view()),
    path('delete',DeleteProduct.as_view()),
    path('add_review',AddReview.as_view()),
    path('edit_review',EditReview.as_view()),
    path('delete_review',DeleteReview.as_view()),
    path('add_reply',AddReply.as_view())
]
