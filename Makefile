.PHONY: apollo

define SENSORS_MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temp INTEGER,
    humidity DECIMAL(5,2),
    moisture DECIMAL(5,2),
    moisture DECIMAL(5,2),
    luminosity DECIMAL(5,2),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export SENSORS_MIGRATION_SCRIPT
migrate:
	sqlite3 /home/pi/apollo/data/db.sqlite "$$SENSORS_MIGRATION_SCRIPT"


export FLASK_DEBUG=1
export TEMPLATES_AUTO_RELOAD=1
run:
	cd apollo/ && flask run --host=0.0.0.0

pip:
	pip install -Ur requirements/dev.txt

venv:
	rm -rf ../venv/apollo/
	virtualenv -p python3.8 --no-site-packages --prompt=apollo- ../venv/apollo

check:
	black --line-length 89 --target-version py38 apollo/
	isort apollo/**/*.py
	flake8 apollo/
