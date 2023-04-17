# Tipul mobile backend

## Local run manual

- Clone this repository
- Optionally run command `git checkout develop` if you want to launch develop version of the backend
- Run command `python -m venv venv` to create virtual environment
- Activate virtual environment
    - On Windows run command `venv\Scripts\activate.bat`
    - On Unix run command `source venv\bin\activate`
- Run command `pip install -r requirements.txt` to install necessary packages
- Get .env from developers
- Start the db server using command `docker compose up`
- That is it, now `cd api` and you can run any django command using `python manage.py ...`
