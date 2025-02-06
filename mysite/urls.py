from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from myapp import views  # views をインポート



urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),  # 'myapp/' 以下のURLは 'myapp.urls' のURLパターンにマッチ
    path('', views.home, name='home'),  # ルート ('/') に 'home' ビューをマッチさせる


]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#     # パスワードリセット関連のURL
#     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
#     # 他のURLパターン...
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)