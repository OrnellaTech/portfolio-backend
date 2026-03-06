# serializers.py
from rest_framework import serializers
from .models import (Utilisateur, Projet, Tool, SocialLink, Experience, Service, PriseContact, Localisation, Skill)


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'nom']

class UtilisateurSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'nom', 'prenom', 'email', 'photo_profil']


class SkillSerializer(serializers.ModelSerializer):
    utilisateur_details = UtilisateurSimpleSerializer(source='utilisateur', read_only=True)
    class Meta:
        model = Skill
        fields = ['id', 'label', 'value', 'utilisateur', 'utilisateur_details']  # Ajoute 'id' et 'utilisateur'

class SocialLinkSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSimpleSerializer(read_only=True)  # Inclure les détails de l'utilisateur
    class Meta:
        model = SocialLink
        fields = ['id', 'nom', 'lien', 'utilisateur']  # Spécifie les champs


class ProjetSerializer(serializers.ModelSerializer):
    tools = ToolSerializer(many=True, read_only=True)
    utilisateur = UtilisateurSimpleSerializer(read_only=True)
    class Meta:
        model = Projet
        fields = [
            'id', 'titre', 'resume', 'image', 'lien',
            'role', 'category', 'github_url',
            'media_type', 'media_url', 'gallery',
            'tools', 'utilisateur'
        ]

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    utilisateur_details = UtilisateurSimpleSerializer(source='utilisateur', read_only=True) # Inclure les détails de l'utilisateur
    class Meta:
        model = Service
        fields = [
            'id',
            'nom',
            'detail',
            'utilisateur','utilisateur_details'
        ]

class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = '__all__'





class PriseContactSerializer(serializers.ModelSerializer):
    # Inclure les détails de l'utilisateur associé
    utilisateur_details = UtilisateurSimpleSerializer(source='utilisateur', read_only=True)
    
    class Meta:
        model = PriseContact
        fields = [
            'id', 
            'nom_complet', 
            'email', 
            'objet', 
            'message', 
            'utilisateur',  
            'utilisateur_details' 
        ]


# Serializer principal pour Utilisateur
class UtilisateurSerializer(serializers.ModelSerializer):
   
    projets = ProjetSerializer(many=True, read_only=True)
    sociallinks = SocialLinkSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    skills_fk = SkillSerializer(many=True, read_only=True)
    localisation = LocalisationSerializer(read_only=True)
    messages_recus = PriseContactSerializer(many=True, read_only=True)
    
    class Meta:
        model = Utilisateur
        fields = [
            'id', 'nom', 'prenom', 'photo_profil', 'photo_intro',
            'description', 'age', 'email', 'telephone', 'lien_cv',
            'titles_text',
            'projets',          
            'sociallinks',      
            'experiences',      
            'services',         
            'skills_fk',        
            'localisation',     
            'messages_recus',   
        ]