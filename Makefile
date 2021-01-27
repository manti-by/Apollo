.PHONY: apollo

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

export FLASK_DEBUG=1
export TEMPLATES_AUTO_RELOAD=1
run:
	cd apollo/ && flask run --host=0.0.0.0

pip:
	pip install -Ur requirements/apollo.dev.txt

venv:
	rm -rf ../venv/apollo/
	virtualenv -p python3.8 --no-site-packages --prompt=apollo- ../venv/apollo

check:
	black --line-length 89 --target-version py38 apollo/
	isort apollo/**/*.py
	flake8 apollo/
