from rest_framework.routers import SimpleRouter

from .views import AuthViewSet, ProfileViewSet

router = SimpleRouter(trailing_slash=False)

router.register(r"account", AuthViewSet, basename="account")
router.register(r"profile", ProfileViewSet, basename="profile")
