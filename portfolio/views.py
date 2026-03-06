from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')
# views.py - Version améliorée avec logs
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .models import PriseContact, Utilisateur
from .serializers import PriseContactSerializer
import logging

logger = logging.getLogger(__name__)

class PriseContactViewSet(viewsets.ModelViewSet):
    queryset = PriseContact.objects.all()
    serializer_class = PriseContactSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Sauvegarder le message
        self.perform_create(serializer)
        logger.info(f"Message sauvegardé: {serializer.data}")
        
        # Récupérer l'utilisateur concerné
        user_id = request.data.get('utilisateur')
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
                    
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=False,
                        )
                        logger.info(f"Email envoyé à {user.email}")
                    except BadHeaderError:
                        logger.error("BadHeaderError: En-tête invalide")
                    except Exception as e:
                        logger.error(f"Erreur envoi email: {str(e)}")
                    
                    # Envoyer une copie à l'expéditeur
                    try:
                        send_mail(
                            f"Copie de votre message - {serializer.data['objet']}",
                            f"Bonjour {serializer.data['nom_complet']},\n\nVoici une copie de votre message :\n\n{serializer.data['message']}\n\nNous vous répondrons dans les plus brefs délais.",
                            settings.DEFAULT_FROM_EMAIL,
                            [serializer.data['email']],
                            fail_silently=False,
                        )
                        logger.info(f"Copie envoyée à {serializer.data['email']}")
                    except Exception as e:
                        logger.error(f"Erreur envoi copie: {str(e)}")
                else:
                    logger.warning("L'utilisateur n'a pas d'email")
                    
            except Utilisateur.DoesNotExist:
                logger.error(f"Utilisateur {user_id} non trouvé")
            except Exception as e:
                logger.error(f"Erreur inattendue: {str(e)}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    