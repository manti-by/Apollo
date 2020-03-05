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
local:
	cd apollo && flask run --host=0.0.0.0

pip:
	pip install -Ur deploy/requirements.txt

venv:
	deactivate | true
	rm -rf ../venv/
	virtualenv -p python3 --no-site-packages --prompt=apollo- ../venv
	. ../venv/bin/activate

check:
	black --line-length 89 --target-version py36 apollo/
	isort apollo/**/*.py
	flake8 apollo/
