from django.urls import path
from .import views
urlpatterns = [
    path('',views.login_view,name="login_view"),
    path("loginsubmit/",views.loginsubmit, name="loginsubmit"),
    path('register/',views.register,name="register"),
    path("registersubmit/",views.registersubmit, name="registersubmit"),
    path("logout_view/", views.logout_view, name="logout_view"),

    

    path('home/',views.home,name="home"),
    path('message_Send/',views.message,name="message_Send"),
    path("store-chroma/",views.store_json_data, name="store_chroma"),
    path("chroma-data/",views.get_full_chroma_collection,name="get_full_chroma_collection"),


]
