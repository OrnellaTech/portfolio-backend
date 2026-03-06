# populate_db.py
import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_portofolio.settings')
django.setup()

from portfolio.models import (
    Utilisateur, Skill, Tool, Projet, 
    SocialLink, Experience, Service, 
    PriseContact, Localisation, GalleryImage
)

def create_tools():
    print("\n🔧 Création des outils...")
    tools_data = ['Python', 'Django', 'Flutter', 'HTML', 'CSS', 
                  'JavaScript', 'Bootstrap', 'Dart', 'Canva', 
                  'Figma', 'React', 'Vue.js', 'Node.js', 'MongoDB']
    
    tools = []
    for tool_name in tools_data:
        tool, created = Tool.objects.get_or_create(nom=tool_name)
        tools.append(tool)
        print(f"  - {tool_name}")
    
    return tools

def create_users():
    print("\n🚀 Création des utilisateurs...")
    
    # Utilisateur 1 - Ornella
    user1, created = Utilisateur.objects.get_or_create(
        email='ornella05koffi@gmail.com',
        defaults={
            'nom': 'Koffi',
            'prenom': 'Ornella',
            'photo_profil': 'images/about-person_0b7ZobQ.jpeg',
            'photo_intro': 'images/intro_bg.jpg',
            'description': 'Développeuse full-stack passionnée par la création d\'applications innovantes',
            'age': '20',
            'telephone': '+225 07 10 17 28 41',
            'lien_cv': 'https://example.com/cv-ornella.pdf',
            'titles_text': 'Future Software Engineer, Computer Science Student, Web and Mobile Developer, UI/UX Enthusiast'
        }
    )
    print(f"✅ Utilisateur 1: {user1.prenom} {user1.nom} ({user1.email})")

    # Utilisateur 2 - Océane
    user2, created = Utilisateur.objects.get_or_create(
        email='oceane.konan@gmail.com',
        defaults={
            'nom': 'Konan',
            'prenom': 'Océane',
            'photo_profil': 'images/oceane_profil.jpg',
            'photo_intro': 'images/oceane_intro.jpg',
            'description': 'Data Scientist & AI Specialist, passionnée par l\'intelligence artificielle',
            'age': '22',
            'telephone': '+225 05 55 55 55',
            'lien_cv': 'https://example.com/cv-oceane.pdf',
            'titles_text': 'AI Student, Web Developer, Frontend dev, Data Scientist'
        }
    )
    print(f"✅ Utilisateur 2: {user2.prenom} {user2.nom} ({user2.email})")

    return user1, user2

def create_skills(user1, user2, tools):
    print("\n📚 Création des compétences...")
    
    # Compétences pour Ornella
    skills_data_user1 = [
        ('Languages & Frameworks', 'Python, Java, Django, Flutter'),
        ('Web & Front-end', 'HTML, CSS, JavaScript, Bootstrap'),
        ('Databases', 'SQL, MySQL, PostgreSQL'),
        ('Tools & Software', 'GitHub, VS Code, Canva, Figma'),
        ('Languages', 'Français (natif), Anglais (intermédiaire)'),
    ]
    
    for label, value in skills_data_user1:
        skill, created = Skill.objects.get_or_create(
            utilisateur=user1,
            label=label,
            value=value
        )
    print(f"✅ {len(skills_data_user1)} compétences pour {user1.prenom}")
    
    # Compétences pour Océane
    skills_data_user2 = [
        ('AI & Machine Learning', 'TensorFlow, PyTorch, Scikit-learn'),
        ('Data Science', 'Pandas, NumPy, Matplotlib'),
        ('Web Development', 'Django, React, Node.js'),
        ('Databases', 'MongoDB, PostgreSQL'),
        ('Languages', 'Français (natif), Anglais (avancé)'),
    ]
    
    for label, value in skills_data_user2:
        skill, created = Skill.objects.get_or_create(
            utilisateur=user2,
            label=label,
            value=value
        )
    print(f"✅ {len(skills_data_user2)} compétences pour {user2.prenom}")

def create_projects(user1, user2, tools):
    print("\n📁 Création des projets...")
    
    # Projets pour Ornella
    projects_data_user1 = [
        {
            'titre': 'Scoop 3B website',
            'resume': 'Site web pour une coopérative agricole ivoirienne',
            'role': 'Fullstack Developer',
            'category': 'Web App',
            'github_url': 'https://github.com/OrnellaTech/scoop3b',
            'media_type': None,
            'tools': ['HTML', 'CSS', 'JavaScript', 'Bootstrap']
        },
        {
            'titre': 'Ivoire Fashion',
            'resume': 'Site e-commerce de mode',
            'role': 'Fullstack Developer',
            'category': 'E-commerce',
            'github_url': 'https://github.com/OrnellaTech/ivoire-fashion',
            'media_type': 'gallery',
            'tools': ['HTML', 'CSS', 'Python', 'Django']
        },
        {
            'titre': 'Health Search',
            'resume': 'Application mobile de recherche de pharmacies',
            'role': 'Frontend Developer',
            'category': 'Mobile App',
            'github_url': 'https://github.com/OrnellaTech/health-search',
            'media_type': 'video',
            'tools': ['Flutter', 'Dart']
        },
    ]
    
    for proj_data in projects_data_user1:
        tools_list = proj_data.pop('tools')
        projet, created = Projet.objects.get_or_create(
            utilisateur=user1,
            titre=proj_data['titre'],
            defaults=proj_data
        )
        # Ajouter les outils
        for tool_name in tools_list:
            tool = Tool.objects.get(nom=tool_name)
            projet.tools.add(tool)
        print(f"  - {projet.titre} (Ornella)")
    
    # Projets pour Océane
    projects_data_user2 = [
        {
            'titre': 'AI Image Recognition',
            'resume': 'Application de reconnaissance d\'images avec TensorFlow',
            'role': 'Data Scientist',
            'category': 'AI App',
            'github_url': 'https://github.com/oceane/ai-image-recog',
            'media_type': 'gallery',
            'tools': ['Python', 'Django']
        },
        {
            'titre': 'DataViz Dashboard',
            'resume': 'Dashboard interactif de visualisation de données',
            'role': 'Frontend Developer',
            'category': 'Web App',
            'github_url': 'https://github.com/oceane/dataviz',
            'media_type': None,
            'tools': ['HTML', 'CSS', 'JavaScript', 'React']
        },
    ]
    
    for proj_data in projects_data_user2:
        tools_list = proj_data.pop('tools')
        projet, created = Projet.objects.get_or_create(
            utilisateur=user2,
            titre=proj_data['titre'],
            defaults=proj_data
        )
        for tool_name in tools_list:
            tool = Tool.objects.get(nom=tool_name)
            projet.tools.add(tool)
        print(f"  - {projet.titre} (Océane)")

def create_social_links(user1, user2):
    print("\n🌐 Création des réseaux sociaux...")
    
    # Réseaux pour Ornella
    socials_user1 = [
        ('linkedin', 'https://www.linkedin.com/in/ornella-koffi/'),
        ('github', 'https://github.com/OrnellaTech'),
        ('twitter', 'https://twitter.com/ornella_dev'),
    ]
    
    for nom, lien in socials_user1:
        SocialLink.objects.get_or_create(
            utilisateur=user1,
            nom=nom,
            lien=lien
        )
    print(f"✅ {len(socials_user1)} réseaux pour {user1.prenom}")
    
    # Réseaux pour Océane
    socials_user2 = [
        ('linkedin', 'https://www.linkedin.com/in/oceane-konan/'),
        ('github', 'https://github.com/oceane-ai'),
        ('twitter', 'https://twitter.com/oceane_data'),
    ]
    
    for nom, lien in socials_user2:
        SocialLink.objects.get_or_create(
            utilisateur=user2,
            nom=nom,
            lien=lien
        )
    print(f"✅ {len(socials_user2)} réseaux pour {user2.prenom}")

def create_services(user1, user2):
    print("\n🛠️ Création des services...")
    
    # Services pour Ornella
    services_user1 = [
        ('Web Development', 'Création de sites web responsives et modernes'),
        ('Mobile App Development', 'Développement d\'applications mobiles cross-platform'),
        ('UI/UX Design', 'Design d\'interfaces intuitives et attrayantes'),
        ('Consulting', 'Conseil en architecture technique'),
    ]
    
    for nom, detail in services_user1:
        Service.objects.get_or_create(
            utilisateur=user1,
            nom=nom,
            detail=detail
        )
    print(f"✅ {len(services_user1)} services pour {user1.prenom}")
    
    # Services pour Océane
    services_user2 = [
        ('Data Science', 'Analyse de données et machine learning'),
        ('AI Consulting', 'Conseil en intelligence artificielle'),
        ('Data Visualization', 'Création de dashboards interactifs'),
        ('Formation', 'Formation en data science'),
    ]
    
    for nom, detail in services_user2:
        Service.objects.get_or_create(
            utilisateur=user2,
            nom=nom,
            detail=detail
        )
    print(f"✅ {len(services_user2)} services pour {user2.prenom}")

def create_localisation(user1, user2):
    print("\n📍 Création des localisations...")
    
    # Localisation Ornella
    Localisation.objects.get_or_create(
        utilisateur=user1,
        defaults={
            'pays': 'Côte d\'Ivoire',
            'ville': 'Grand-Bassam',
            'quartier': 'MockeyVille',
            'longitude': -3.7333,
            'latitude': 5.2
        }
    )
    print(f"✅ Localisation pour {user1.prenom}")
    
    # Localisation Océane
    Localisation.objects.get_or_create(
        utilisateur=user2,
        defaults={
            'pays': 'Côte d\'Ivoire',
            'ville': 'Abidjan',
            'quartier': 'Cocody',
            'longitude': -4.0167,
            'latitude': 5.3333
        }
    )
    print(f"✅ Localisation pour {user2.prenom}")

def create_experiences(user1, user2):
    print("\n💼 Création des expériences...")
    
    # Expériences Ornella
    experiences_user1 = [
        {
            'description': 'Stage développeur full-stack',
            'type_contrat': 'Stage',
            'date_debut': timezone.now() - timedelta(days=180),
            'date_fin': timezone.now() - timedelta(days=30),
            'nom_entreprise': 'Tech Start-up',
            'role': 'Développeur full-stack'
        },
    ]
    
    for exp in experiences_user1:
        Experience.objects.get_or_create(
            utilisateur=user1,
            description=exp['description'],
            defaults=exp
        )
    print(f"✅ Expériences pour {user1.prenom}")
    
    # Expériences Océane
    experiences_user2 = [
        {
            'description': 'Data Scientist Junior',
            'type_contrat': 'CDI',
            'date_debut': timezone.now() - timedelta(days=365),
            'date_fin': timezone.now(),
            'nom_entreprise': 'AI Solutions',
            'role': 'Data Scientist'
        },
    ]
    
    for exp in experiences_user2:
        Experience.objects.get_or_create(
            utilisateur=user2,
            description=exp['description'],
            defaults=exp
        )
    print(f"✅ Expériences pour {user2.prenom}")

def create_prise_contact(user1, user2):
    print("\n📧 Création des messages de contact...")
    
    messages = [
        {
            'utilisateur': user1,
            'nom_complet': 'Jean Dupont',
            'email': 'jean.dupont@email.com',
            'objet': 'Demande de devis',
            'message': 'Bonjour, je suis intéressé par vos services de développement web.'
        },
        {
            'utilisateur': user2,
            'nom_complet': 'Marie Claire',
            'email': 'marie.claire@email.com',
            'objet': 'Collaboration',
            'message': 'Je souhaiterais discuter d\'une potentielle collaboration.'
        },
    ]
    
    for msg in messages:
        PriseContact.objects.get_or_create(
            utilisateur=msg['utilisateur'],
            email=msg['email'],
            defaults=msg
        )
    print(f"✅ Messages de contact créés")

def main():
    print("=" * 50)
    print("🚀 DÉBUT DU PEUPLEMENT DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    # Création des données
    tools = create_tools()
    user1, user2 = create_users()
    create_skills(user1, user2, tools)
    create_projects(user1, user2, tools)
    create_social_links(user1, user2)
    create_services(user1, user2)
    create_localisation(user1, user2)
    create_experiences(user1, user2)
    create_prise_contact(user1, user2)
    
    print("\n" + "=" * 50)
    print("✅ PEUPLEMENT TERMINÉ AVEC SUCCÈS !")
    print("=" * 50)
    print(f"\n📊 Récapitulatif:")
    print(f"  - Utilisateurs: {Utilisateur.objects.count()}")
    print(f"  - Outils: {Tool.objects.count()}")
    print(f"  - Compétences: {Skill.objects.count()}")
    print(f"  - Projets: {Projet.objects.count()}")
    print(f"  - Réseaux sociaux: {SocialLink.objects.count()}")
    print(f"  - Services: {Service.objects.count()}")
    print(f"  - Expériences: {Experience.objects.count()}")
    print(f"  - Localisations: {Localisation.objects.count()}")
    print(f"  - Messages: {PriseContact.objects.count()}")

if __name__ == "__main__":
    main()