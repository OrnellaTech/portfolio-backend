from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Utilisateur
from django.contrib import admin
from .models import Utilisateur, Projet, SocialLink, Experience, Service, PriseContact, Localisation, Tool, Skill, GalleryImage


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    search_fields = ('nom',)

admin.site.register(GalleryImage)
class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['image', 'order']
    ordering = ['order']


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    list_display = ('titre', 'role', 'category', 'lien', 'github_url', 'image_tag')
    search_fields = ('titre', 'role', 'category')
    list_filter = ['category',]
    readonly_fields = ['image_tag' , 'titre', 'resume']
    filter_horizontal = ('tools',)  # ça devient pratique pour ajouter plusieurs outils







# Admin pour SocialLink
@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('nom', 'lien')
    search_fields = ('nom',)

# Admin pour Experience
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('description', 'type_contrat', 'duree', 'date_debut', 'date_fin', 'nom_entreprise', 'role')
    search_fields = ('description', 'nom_entreprise', 'role')
    list_filter = ('type_contrat',)

# Admin pour Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'detail')
    search_fields = ('nom', 'detail')
    
class SkillAdmin(admin.ModelAdmin):
    list_display = ('label', 'value')
    search_fields = ('label',)

# Admin pour PriseContact
@admin.register(PriseContact)
class PriseContactAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'objet')
    search_fields = ('nom_complet', 'email', 'objet')

# Admin pour Localisation
@admin.register(Localisation)
class LocalisationAdmin(admin.ModelAdmin):
    list_display = ('pays', 'ville', 'quartier', 'longitude', 'latitude')
    search_fields = ('pays', 'ville', 'quartier')



class ProjetInline(admin.TabularInline):
    model = Projet
    extra = 1  # combien de lignes vides pour ajouter
    readonly_fields = ('image_tag',)

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    
class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1
    
class PriseContactInline(admin.TabularInline):
    model = PriseContact
    extra = 1
    
class LocalisationInline(admin.TabularInline):
    model = Localisation
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'age')
    search_fields = ('nom', 'prenom', 'email', 'telephone')
    list_filter = ('age',)
    inlines = [SkillInline, ProjetInline, SocialLinkInline, ServiceInline, ExperienceInline, PriseContactInline, LocalisationInline]
    
    
    

