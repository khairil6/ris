#!/usr/bin/env sh
set -e

# 0) Ensure our code folder exists
[ -d /app/data ] || mkdir -p /app/data

# Move into the project folder
cd /app/data

# Install psycopg2 build dependencies only if missing
if ! dpkg -s build-essential libpq-dev python3-dev >/dev/null 2>&1; then \
  echo "🔧 Build deps missing: installing build-essential, libpq-dev, python3-dev"; \
  apt-get update && \
  apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev && \
  rm -rf /var/lib/apt/lists/*; \
else \
  echo "✔ Build deps already installed"; \
fi

# 1) Create requirements.txt if it doesn't exist
if [ ! -f requirements.txt ]; then
  cat > requirements.txt <<EOF
Django>=4.2
djangorestframework
pydicom
requests
EOF
fi

# 2) Check & install each Python dependency
echo "🔍 Checking Python dependencies..."
while IFS= read -r req || [ -n "$req" ]; do
  # skip empty lines or comments
  case "$req" in
    ''|\#*) continue ;;
  esac

  # strip version specifiers for the package name
  pkg=$(printf '%s' "$req" | sed 's/[<>=].*//')

  if pip show "$pkg" >/dev/null 2>&1; then
    echo "✔ $pkg already installed"
  else
    echo "⬇ $pkg not found; installing $req"
    pip install --no-cache-dir "$req"
  fi
done < requirements.txt

# 3) Scaffold the Django project if missing
if [ ! -d ris_project ]; then
  echo "⟳ scaffolding Django project 'ris_project'…"
  django-admin startproject ris_project
fi

# Move into the ris_project folder
cd /app/data/ris_project

# 4) create ris_app
if [ ! -d ris_app ]; then
  echo "⟳ creating ris API app 'ris_app'…"
  python manage.py startapp ris_app
fi

# 5) Apply database migrations
echo "⚙️  Applying migrations…"
python manage.py makemigrations accounts
python manage.py makemigrations ris_app 
python manage.py makemigrations
python manage.py migrate

# 6) Only create the superuser if none exists
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && \
   [ -n "$DJANGO_SUPERUSER_EMAIL" ] && \
   [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && \
   ! python manage.py shell -c "from django.contrib.auth import get_user_model; \
      print(get_user_model().objects.filter(is_superuser=True).exists())" | grep -q True
then
  echo "🔑 Creating Django superuser ${DJANGO_SUPERUSER_USERNAME}"
  python manage.py createsuperuser --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL"
  # Set its password
  python manage.py shell -c "from django.contrib.auth import get_user_model; \
    u = get_user_model().objects.get(username='${DJANGO_SUPERUSER_USERNAME}'); \
    u.set_password('${DJANGO_SUPERUSER_PASSWORD}'); u.save()"
fi

# 7) Launch the Django development server (PID 1)
echo "🚀 Starting Django dev server on 0.0.0.0:8000"
exec python manage.py runserver 0.0.0.0:8000
