## 📘 Development Journal – Gig Benchmark Project`

### Step 1 – Environment setup

✅ Installed Python 3 and pip.
✅ Created a virtual environment (venv):

````
python3 -m venv venv
source venv/bin/activate   # (Ubuntu WSL)
````

✅ Core Dependencies Installed:

- Django 5.2.5
- Django REST Framework 3.16.1
- mysqlclient (for Django ↔ MySQL connection)

---

### Step 2 – MySQL configuration

🚨 Initial issue: root access blocked.

🔧 Fix: started MySQL in --skip-grant-tables mode + created /var/run/mysqld directory.

✅ Reset root password:

````
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
````

✅ Created dedicated Django user:

````
CREATE USER 'giguser'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON GIG.* TO 'giguser'@'localhost';
FLUSH PRIVILEGES;
````

✅ Verified connection with:

````
mysql -u giguser -p
````

---

### Step 3 – Database prepared by teammate

✅ Tables Created by Teammate (GIG database):

- Sports (reference)

- MarketNames (with code UNIQUE)

- Leagues (FK → Sports)

- Teams (FK → Leagues)

- Players (FK → Teams)

✅ Constraints: Foreign Keys + UNIQUE fields.

---

### Step 4 – Django initialization

✅ Project created:

````
django-admin startproject gig_benchmark .
````

✅ Main app created:

````
python manage.py startapp core
````

✅ Models Synchronized with MySQL:

- Sport (code, name)

- MarketName (code UNIQUE, name, sport FK)

- League, Team, Player (with FK constraints)

````
class Sport(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'Sports'

    def __str__(self):
        return self.name

class MarketName(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="markets")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ('sport', 'code')
        db_table = 'MarketNames'

    def __str__(self):
        return f"{self.sport.name} - {self.name}"


class League(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="leagues")
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('sport', 'name')
        db_table = 'Leagues'

    def __str__(self):
        return self.name
````

✅ Migrations Applied:

````
python manage.py makemigrations
python manage.py migrate
````

→ 3 migrations (0001_initial, 0002_alter_tables, 0003_rename_player_field).

---

### Step 5 – API Setup & Keycloak Integration (Not finish)

📦 Dependencies Added:
````
pip install djangorestframework-simplejwt django-cors-headers mozilla-django-oidc
````

⚙️ Configuration in settings.py:
````
# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oidc_auth.authentication.JSONWebTokenAuthentication',  # Keycloak
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # All endpoints protected
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS (for Symfony frontend)
CORS_ALLOWED_ORIGINS = ["http://localhost:8001"]
CORS_ALLOW_HEADERS = ["authorization", "content-type"]

# Keycloak (TO CONFIGURE)
OIDC_AUTH = {
    'OIDC_ENDPOINT': 'https://keycloak.example.com/realms/mon-realm',  # ⚠ Replace with real URL
    'OIDC_CLAIMS_OPTIONS': {
        'aud': {'values': ['gig-django-api']},  # ⚠ Must match Keycloak client_id
    },
}
````

---

### Step 6 – Serializers & ViewSets

🔄 serializers.py (No Nesting for Simplicity):

````
from rest_framework import serializers
from .models import Sport, MarketName, League, Team, Player

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'code', 'name']  # Flat structure (no nested objects)

class MarketNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketName
        fields = ['id', 'code', 'name']  # 'code' is required (UNIQUE in DB)
````

Note: No nesting means we only return IDs for relationships (e.g., sport_id instead of embedding the full Sport object). This keeps responses lightweight.

🖥 views.py (CRUD Endpoints):

````
from rest_framework import viewsets
from .models import Sport, MarketName
from .serializers import SportSerializer, MarketNameSerializer

class SportViewSet(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer

class MarketNameViewSet(viewsets.ModelViewSet):
    queryset = MarketName.objects.all()
    serializer_class = MarketNameSerializer
````

---

### Step 7 – URL Routing

🌐 urls.py (Auto-generated API Routes):

````
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import SportViewSet, MarketNameViewSet

router = DefaultRouter()
router.register(r'sports', SportViewSet)        # → `/api/sports/`
router.register(r'market-names', MarketNameViewSet)  # → `/api/market-names/`

urlpatterns = [
    path('api/', include(router.urls)),  # All endpoints under `/api/`
]
````

### Step 8 - Current Project Tree (Updated)

````
.
├── README.md
├── core/
│   ├── admin.py          # ✅ MarketName registered
│   ├── apps.py           # ✅ App config
│   ├── migrations/       # ✅ 3 migrations applied
│   ├── models.py         # ✅ All models synced with MySQL
│   ├── serializers.py    # ✅ Flat serializers (no nesting)
│   ├── tests.py          # ❌ TODO: Add unit tests
│   ├── views.py          # ✅ ViewSets for all models
│   └── ...
├── gig_benchmark/
│   ├── settings.py       # ✅ DRF + Keycloak config (pending final OIDC_ENDPOINT)
│   ├── urls.py           # ✅ API routes under `/api/`
│   └── wsgi.py
└── manage.py
````

---

### Next Steps

Finalize Keycloak:
- Replace OIDC_ENDPOINT and aud.values in settings.py.
- Test authentication with Symfony frontend.

Add Tests:
- Write unit tests for MarketNameSerializer and MarketNameViewSet.

Optimize Queries (if needed):
- Use .select_related() in ViewSets to avoid N+1 queries.

Document API:
- Add Swagger/Redoc for interactive docs (e.g., drf-yasg).

### Key Decisions


- No Nesting in Serializers: Chosen for simplicity and performance. Can be added later if needed.
- Keycloak Integration: Centralized auth for Django + Symfony.
- Flat Structure: Easy to maintain and extend.
