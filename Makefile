define SENSORS_MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temp DECIMAL(5,2),
    humidity TINYINT,
    moisture TINYINT,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export SENSORS_MIGRATION_SCRIPT
migrate_sensors_data:
	sqlite3 deploy/db.sqlite "$$SENSORS_MIGRATION_SCRIPT"

define CURRENCY_MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usd_buy DECIMAL(5,2),
    usd_sell DECIMAL(5,2),
    eur_buy DECIMAL(5,2),
    eur_sell DECIMAL(5,2),
    rur_buy DECIMAL(5,2),
    rur_sell DECIMAL(5,2),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export CURRENCY_MIGRATION_SCRIPT
migrate_currency_data:
	sqlite3 deploy/db.sqlite "$$CURRENCY_MIGRATION_SCRIPT"

define WEATHER_MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temp DECIMAL(5,2),
    pressure TINYINT,
    icon VARCHAR(15),
    wind_speed TINYINT,
    wind_direction TINYINT,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export WEATHER_MIGRATION_SCRIPT
migrate_weather_data:
	sqlite3 deploy/db.sqlite "$$WEATHER_MIGRATION_SCRIPT"


remigrate:
	rm -f db.sqlite
	make migrate
	make seed

export FLASK_APP=server
export FLASK_DEBUG=1
export TEMPLATES_AUTO_RELOAD=1
apollo:
	cd apollo && flask run --host=0.0.0.0

apollo-pip:
	pip install -Ur deploy/requirements/apollo.dev.txt

apollo-venv:
	rm -rf ../venv/apollo/
	virtualenv -p python3.8 --no-site-packages --prompt=apollo- ../venv/apollo

apollo-check:
	black --line-length 89 --target-version py38 apollo/
	isort apollo/**/*.py
	flake8 apollo/

helios-build:
	p4a apk --private=$$(pwd)/helios --sdk-dir=$$HOME/android/home/ --ndk-dir=$$HOME/android/ndk/android-ndk-r21b-linux-x86_64/android-ndk-r21b --android-api=26 --ndk-api=21

helios-clean:
	p4a clean builds

helios-pip:
	pip install -Ur deploy/requirements/helios.dev.txt

helios-venv:
	rm -rf ../venv/helios/
	virtualenv -p python3.8 --no-site-packages --prompt=helios- ../venv/helios

helios-check:
	black --line-length 89 --target-version py38 helios/
	isort helios/**/*.py
	flake8 helios/