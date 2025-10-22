# 🔐 CONFIGURATION KEYCLOAK - GIG BENCHMARK

## 📅 Date de sauvegarde
Date : (date 22/10/2025)

---

## 🏢 CONFIGURATION KEYCLOAK

### Realm
- **Nom** : `GigBenchmarkRealm`
- **URL Keycloak local** : `http://localhost:8080`

### Client API
- **Client ID** : `gig-api`
- **Type** : Confidential
- **Client Secret** : `[VOIR .env_backup]`

### Token Settings
- **Access Token Lifespan** : 5 minutes (300s)
- **Refresh Token Lifespan** : 30 minutes (1800s)

### Audience Mapper
- **Mapper Type** : Audience Mapper
- **Name** : `gig-api-audience`
- **Included Client Audience** : `gig-api`
- **Add to access token** : ✅ ON
- **Add to ID token** : ❌ OFF

---

## 👥 UTILISATEURS DE TEST

| Username | Password | Rôle | Accès |
|----------|----------|------|-------|
| `admin1` | `admin1` | admin | Routes privées ✅ |
| `user1` | `user1` | user | Routes publiques uniquement |

---

## 🔧 FICHIERS CRITIQUES

### Authentification
- `core/keycloak_auth.py` → Logique auth custom
- `core/middlewares.py` → Middleware de validation token
- `gig_benchmark/keycloak_public_key.pem` → Clé publique RSA

### Configuration
- `gig_benchmark/settings.py` → Config Django + Keycloak
- `gig_benchmark/urls.py` → Routes protégées
- `.env` → Variables d'environnement sensibles

---

## 🧪 COMMANDES DE TEST QUI FONCTIONNENT

### 1. Obtenir un token (admin)
```bash
curl -X POST "http://localhost:8080/realms/GigBenchmarkRealm/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=gig-api" \
  -d "client_secret=VOIR_.env" \
  -d "username=admin1" \
  -d "password=admin1"
```

### 2. Tester une route privée
```bash
curl -X GET "http://localhost:8000/api/v1/sports/" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 3. Refresh token
```bash
curl -X POST "http://localhost:8080/realms/GigBenchmarkRealm/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=gig-api" \
  -d "client_secret=VOIR_.env" \
  -d "refresh_token=<REFRESH_TOKEN>"
  ```

✅ TESTS VALIDÉS
Test 	Résultat
Routes publiques sans token         ->	    ✅
Routes privées sans token 	        ->      ✅ Refusé (401)
Routes privées avec token admin 	->      ✅ Accès autorisé
Routes privées avec token user 	    ->      ✅ Refusé (403)
Token expiré 	                    ->      ✅ Refusé (401)
Refresh token valide 	            ->      ✅ Nouveau token
Refresh token expiré 	            ->      ✅ Refusé
