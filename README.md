## 📘 Development Journal – Gig Benchmark Project`

### Step 1 – Environment setup

✅ Installed Python 3 and pip.
✅ Created a virtual environment (venv):

````
python3 -m venv venv
source venv/bin/activate   # (Ubuntu WSL)
````

✅ Installed main dependencies:

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

Step 3 – Database prepared by teammate

✅ Local database GIG created with tables:

- Sports

- MarketNames

- Leagues

- Teams

- Players

✅ Referential constraints in place (Foreign Keys, UNIQUE).

✅ This schema is the reference for building Django models.

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

✅ Current project tree:

````
.
├── README.md
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── gig_benchmark
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
````

✅ Models defined:

- Sport

- MarketName

- League

- Team

- Player
