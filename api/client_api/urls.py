from django.urls import include, path as url
from rest_framework.routers import SimpleRouter
from api.client_api.auth.urls import router as AuthRouter

router = SimpleRouter(trailing_slash=False)

urlpatterns = [
    url(r'auth/', include((AuthRouter.urls, 'auth-api'), namespace='client-auth-api')),
    # url(r'transaction/', include((TranscationRouter.urls, 'transaction-api'), namespace='transaction-api')),
    # path(
    #     'generate-token',
    #     get_token,
    #     name='generate-token',
    # ),

]
