# from django.urls import path
# from . import views

# urlpatterns=[
    

#     path('nextQuestion/',views.nextQuestion),
#     path('previousQuestion/',views.previousQuestion),
#     path('endexam/',views.endexam),
#     path('startTest/',views.startTest),
#     path('addQuestion/',views.addQuestion),
#     path('viewQuestion/',views.viewQuestion),
#     path('updateQuestion/',views.updateQuestion),
#     path('deleteQuestion/',views.deleteQuestion),

# ]


from django.urls import path

from . import views


urlpatterns = [

    path('search1/',views.search1),
    
    path('search/<pageno>',views.search),

    path('giveMePage1/',views.giveMePage1),

    path('Analysis/',views.giveMePage2),

    path('main_page/',views.giveMePage3),
    
    path('startTest/',views.startTest),

    path('nextQuestion/',views.nextQuestion),

    path('previousQuestion/',views.previousQuestion),

    path('endexam/',views.endexam),

    path('addQuestion/',views.addQuestion),
    path('viewQuestion/',views.viewQuestion),
    path('updateQuestion/',views.updateQuestion),
    path('deleteQuestion/',views.deleteQuestion),
    
    # in html :- action="/testapp/login/"
]