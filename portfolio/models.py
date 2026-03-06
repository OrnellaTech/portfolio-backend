from django.db import models
class Skill(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='skills_fk')
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.label}: {self.value}"
    
# Create your models here.
class Utilisateur(models.Model):
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        
    nom = models.CharField(max_length=100, verbose_name= "Nom Utilisateur")
    prenom = models.CharField(max_length=100, verbose_name= "Prénom Utilisateur")
    photo_profil = models.ImageField(upload_to='images/', verbose_name= "Photo de profil", blank=True, null=True)
    photo_intro = models.ImageField(upload_to='images/', verbose_name= "Photo d'introduction", blank=True, null=True)
    description = models.CharField(max_length=100, verbose_name= "Description", blank=True, null=True)
    age = models.CharField(max_length=100, verbose_name= "age", blank=True, null=True)
    email = models.EmailField(verbose_name= "Email", blank=True, null=True)
    telephone = models.CharField(max_length=100, verbose_name= "Téléphone", blank=True, null=True)
    lien_cv = models.CharField(max_length=100, verbose_name= "Lien CV", blank=True, null=True)
    # skills = models.ManyToManyField(Skill, blank=True, related_name='utilisateurs', verbose_name="Compétences")
    # projets = models.ManyToManyField('Projet', blank=True)
    # sociallinks = models.ManyToManyField('SocialLink', blank=True)
    # experiences = models.ManyToManyField('Experience', blank=True)
    # services = models.ManyToManyField('Service', blank=True)
    
    # message_recu = models.ManyToManyField('PriseContact', blank=True, related_name='utilisateurs')
    # localisation = models.ForeignKey('Localisation', on_delete=models.CASCADE, blank=True, null=True)
    titles_text = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Titres (séparés par des virgules)",
        help_text="Ex: Future Software Engineer, Computer Science Student, Web Developer"
    )
    def __str__(self):
        return self.nom



from django.db import models
from django.utils.html import format_html



class Tool(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de l’outil")

    def __str__(self):
        return self.nom
   
  
class GalleryImage(models.Model):
    class Meta:
        verbose_name = "Image de galerie"
        verbose_name_plural = "Images de galerie"
    
    projet = models.ForeignKey('Projet', on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='gallery/', verbose_name="Image")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    
    def __str__(self):
        return f"Image pour {self.projet.titre}"
    
     
    
    
class Projet(models.Model):
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='projets', blank=True, null=True)
    titre = models.CharField(max_length=100, verbose_name="Titre")
    resume = models.CharField(max_length=200, verbose_name="Résumé")
    image = models.ImageField(upload_to='images/', verbose_name="Image principale", blank=True, null=True)
    lien = models.URLField(verbose_name="Lien du projet", blank=True, null=True)
    
    # Nouveaux champs
    tools = models.ManyToManyField(Tool, blank=True, related_name='projets', verbose_name="Outils utilisés")
    role = models.CharField(max_length=100, blank=True, null=True, verbose_name="Rôle")
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name="Catégorie")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub URL")
    media_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[('gallery','Gallery'),('video','Video')],
        verbose_name="Type de média"
    )
    media_url = models.URLField(blank=True, null=True, verbose_name="URL Média (Vidéo ou Galerie)")
    # gallery = models.JSONField(blank=True, null=True, verbose_name="Galerie images (JSON)")
    gallery = models.ManyToManyField(
        'GalleryImage',  # ← Change ici (au lieu de 'ProjetImage')
        blank=True, 
        related_name='projets', 
        verbose_name="Galerie d'images"
    )
    copyright_author = models.CharField(
        max_length=200, 
        verbose_name="Auteur copyright", 
        blank=True, 
        null=True,
        help_text="Nom qui apparaîtra dans le copyright du footer"
    )
    def __str__(self):
        return self.titre

    # Affichage miniature dans l’admin
    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', self.image.url)
        return "-"
    image_tag.short_description = 'Image'
    
    
  
class SocialLink(models.Model):
    class Meta:
        verbose_name = "Réseau social",
        verbose_name_plural = "Réseaux sociaux"
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='sociallinks', blank=True, null=True)
    nom = models.CharField(max_length=100, verbose_name= "Nom de la plateforme")
    lien = models.CharField(max_length=100, verbose_name= "Lien social", blank=True, null=True)
   
    
    def __str__(self):
        return self.nom
    
    
    
class Experience(models.Model):
    class Meta:
        verbose_name = "Expérience"
        verbose_name_plural = "Expérience"
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='experiences', blank=True, null=True)
    description = models.CharField(max_length=200, verbose_name= "description de l'éxpérience")
    type_contrat = models.CharField(max_length=100, verbose_name= "Type de contrat")
    duree = models.CharField(max_length=50, verbose_name= "Durée"),
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(verbose_name="Date de fin")
    nom_entreprise = models.CharField(max_length=100, verbose_name= "Nom de l'entreprise")
    role = models.CharField(max_length=100, verbose_name= "Rôle", blank=True, null=True)
    
    
    def __str__(self):
       return self.description
   
   
   
class Service(models.Model):
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='services', blank=True, null=True)
    nom = models.CharField(max_length=100, verbose_name= "Nom du service")
    detail = models.CharField(max_length=100, verbose_name= "Détail", blank=True, null=True)
    # type_service = models.CharField(max_length=100, verbose_name= "Type", blank=True, null=True) 
    # outils = models.CharField(max_length=100, verbose_name= "Détail", blank=True, null=True)
    
    def __str__(self):
       return self.nom
    
    
    
class PriseContact(models.Model):
    class Meta:
        verbose_name = "Prise de contact"
        verbose_name_plural = "Prises de contact"
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, blank=True, null=True, related_name='messages_recus')
    nom_complet = models.CharField(max_length=100, verbose_name= "Nom complet")
    email = models.EmailField(verbose_name= "Email du contact")
    objet = models.CharField(max_length=100, verbose_name= "Objet")
    message = models.CharField(max_length=500, verbose_name= "Message")
    
    def __str__(self):
       return self.nom_complet
   
   
   
class Localisation(models.Model):
    class Meta:
        verbose_name = "Localisation"
        verbose_name_plural = "Localisations"
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, blank=True, null=True, related_name='localisations')
    pays = models.CharField(max_length=100, verbose_name= "Pays" , blank = True, null = True)
    ville = models.CharField(max_length=100, verbose_name= "Ville" , blank = True, null = True)
    longitude = models.DecimalField(max_digits=10 , decimal_places=2, verbose_name= "Longitude" , blank = True, null = True)
    latitude = models.DecimalField(max_digits=10, decimal_places=2, verbose_name= "Latitude", blank = True, null = True)    
    quartier = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.pays
    
        
    