from django.urls import  path,include
from . import views
urlpatterns = [

    path('literature/',views.LiteratureView.as_view(),name='literature'),
    path('documentation/',views.Documentation.as_view(),name='documentation'),
    path('plagiarism/',views.Plagiarism_detector.as_view(),name='plagiarism_detector')

]