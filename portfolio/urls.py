from rest_framework.routers import DefaultRouter
from .viewset import *
from . import views
from django.urls import path

router = DefaultRouter()
router.register('Utilisateur', UtilisateurViewSet)
router.register('Projet', ProjetViewSet)
router.register('Experience', ExperienceViewSet)
router.register('Skill', SkillViewSet)
router.register('SocialLink', SocialLinkViewSet)
router.register('Service', ServiceViewSet)
router.register('Localisation', LocalisationViewSet)
router.register('PriseContact', PriseContactViewSet)
router.register('Tool', ToolViewSet)

urlpatterns = router.urls




