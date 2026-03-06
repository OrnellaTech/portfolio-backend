from rest_framework import viewsets
from portfolio.models import Utilisateur, Projet, SocialLink, Experience, Service, PriseContact, Localisation, Tool, Skill
from portfolio.serializers import (UtilisateurSerializer, ProjetSerializer, SocialLinkSerializer, SkillSerializer,
                                  ExperienceSerializer, ServiceSerializer, PriseContactSerializer, LocalisationSerializer, ToolSerializer)
# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import PriseContact, Utilisateur
from .serializers import PriseContactSerializer
import logging

logger = logging.getLogger(__name__)

class PriseContactViewSet(viewsets.ModelViewSet):
    queryset = PriseContact.objects.all()
    serializer_class = PriseContactSerializer
    
    def create(self, request, *args, **kwargs):
        # Copie des données pour éviter de modifier l'original
        data = request.data.copy()
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Sauvegarder le message
        self.perform_create(serializer)
        logger.info(f"Message sauvegardé: {serializer.data}")
        
        # Récupérer l'utilisateur concerné
        user_id = data.get('utilisateur')
        logger.info(f"User ID reçu: {user_id}")
        
        if user_id:
            try:
                user = Utilisateur.objects.get(id=user_id)
                logger.info(f"Utilisateur trouvé: {user.email}")
                
                # Vérifier que l'utilisateur a un email
                if user.email:
                    # Envoyer un email à l'utilisateur
                    subject = f"Nouveau message de {serializer.data['nom_complet']}"
                    message = f"""
Vous avez reçu un nouveau message via votre portfolio.

De: {serializer.data['nom_complet']}
Email: {serializer.data['email']}
Sujet: {serializer.data['objet']}

Message:
{serializer.data['message']}
                    """
                    
                    # Envoi à l'utilisateur (propriétaire du portfolio)
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    logger.info(f"Email envoyé à {user.email}")
                    
                    # Envoyer une copie à l'expéditeur
                    send_mail(
                        f"Copie de votre message - {serializer.data['objet']}",
                        f"""
Bonjour {serializer.data['nom_complet']},

Voici une copie du message que vous avez envoyé :

Sujet: {serializer.data['objet']}
Message:
{serializer.data['message']}

Nous vous répondrons dans les plus brefs délais.

Cordialement,
L'équipe
                        """,
                        settings.DEFAULT_FROM_EMAIL,
                        [serializer.data['email']],
                        fail_silently=False,
                    )
                    logger.info(f"Copie envoyée à {serializer.data['email']}")
                else:
                    logger.warning("L'utilisateur n'a pas d'email")
                    
            except Utilisateur.DoesNotExist:
                logger.error(f"Utilisateur {user_id} non trouvé")
            except Exception as e:
                logger.error(f"Erreur envoi email: {str(e)}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    
# views.py
from rest_framework import viewsets
from .models import Projet
from .serializers import ProjetSerializer

class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    
    def get_queryset(self):
        queryset = Projet.objects.all()
        # Récupère le paramètre 'utilisateur' de l'URL
        utilisateur_id = self.request.query_params.get('utilisateur')
        
        if utilisateur_id is not None:
            # Filtre par utilisateur_id
            queryset = queryset.filter(utilisateur_id=utilisateur_id)
            print(f"Filtrage par utilisateur {utilisateur_id}: {queryset.count()} projets trouvés")
        
        return queryset
    
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    
class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    
class SocialLinkViewSet(viewsets.ModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    
    def get_queryset(self):
        queryset = SocialLink.objects.all()
        utilisateur_id = self.request.query_params.get('utilisateur')
        if utilisateur_id:
            queryset = queryset.filter(utilisateur_id=utilisateur_id)
        return queryset
    
class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    
    def get_queryset(self):
        queryset = Experience.objects.all()
        utilisateur_id = self.request.query_params.get('utilisateur')
        if utilisateur_id:
            queryset = queryset.filter(utilisateur_id=utilisateur_id)
        return queryset

    
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    def get_queryset(self):
        queryset = Service.objects.all()
        utilisateur_id = self.request.query_params.get('utilisateur')
        if utilisateur_id:
            queryset = queryset.filter(utilisateur_id=utilisateur_id)
        return queryset 

class LocalisationViewSet(viewsets.ModelViewSet):
    queryset = Localisation.objects.all()
    serializer_class = LocalisationSerializer