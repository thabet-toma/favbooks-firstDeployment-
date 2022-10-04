from django.urls import path,include
from . import views 

urlpatterns = [
    path('',views.logandRegs),
    path('regsProcess',views.regs),
    path('success1',views.success1),
    path('login',views.login),
    path('logout',views.logout),
    path('books',views.book),
    path('addbook',views.addbook),
    path('books/<int:id>',views.bookDe),
    path('addfav/<int:id>',views.addfav),
    path('delfav/<int:id>',views.delfav),
    path('edit',views.edit),

   
    
]
