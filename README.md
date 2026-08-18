# E-Card-Generator

Deployment-ready Flask application based on the upstream E-Card Generator project.

## Included

- User registration and secure password hashing
- Login/logout with session authentication
- Admin-only dashboard and request review
- Aadhar, PAN, Driving License and Voter ID workflow screens
- Request → verification → generated status flow
- Simulated card-key generation
- Search and summary pages
- Gunicorn production server configuration
- Render deployment blueprint
- PostgreSQL support through `DATABASE_URL`
- SQLite fallback for local development

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set SECRET_KEY=change-this
set ADMIN_USERNAME=admin
set ADMIN_PASSWORD=ChangeThisPassword123!
python app.py
```

Open `http://127.0.0.1:5000`.

## Production environment variables

- `SECRET_KEY` — long random application secret
- `DATABASE_URL` — PostgreSQL connection string for persistent production data
- `ADMIN_USERNAME` — initial administrator username
- `ADMIN_PASSWORD` — initial administrator password
- `ADMIN_EMAIL` — initial administrator email

The initial administrator is created only when no admin exists.

## Render deployment

The repository contains `render.yaml`. Connect the repository to Render and configure the four environment variables above. For production, use PostgreSQL rather than SQLite because a normal web-service filesystem should not be treated as persistent application storage.

## Important legal/product note

This is a workflow/demo application for generating and managing card-style records. It does **not** connect to UIDAI, Income Tax/PAN, Parivahan, Election Commission, or any other official government database. Generated numbers are simulated identifiers and must never be represented as official government document numbers.

## Source

The project was copied from `Aayush-kotwani/E-Card-Generator` and then adapted for production deployment and safer authentication/authorization.

## Deployment

This copy is prepared for production deployment with Gunicorn. Set `SECRET_KEY` to a strong random value and configure `DATABASE_URL` in your hosting provider. Render can deploy this repository using the included `render.yaml`.

**Important:** This application is a document-card workflow/demo. It does not connect to UIDAI, PAN, Parivahan, or Election Commission databases and must not be presented as an official government portal.

## Deployment

This copy is prepared for production deployment with Gunicorn. Set `SECRET_KEY` to a strong random value and configure `DATABASE_URL` in your hosting provider. Render can deploy this repository using the included `render.yaml`.

**Important:** This application is a document-card workflow/demo. It does not connect to UIDAI, PAN, Parivahan, or Election Commission databases and must not be presented as an official government portal.

## Deployment

This copy is prepared for production deployment with Gunicorn. Set `SECRET_KEY` to a strong random value and configure `DATABASE_URL` in your hosting provider. Render can deploy this repository using the included `render.yaml`.

**Important:** This application is a document-card workflow/demo. It does not connect to UIDAI, PAN, Parivahan, or Election Commission databases and must not be presented as an official government portal.

## Deployment

This copy is prepared for production deployment with Gunicorn. Set `SECRET_KEY` to a strong random value and configure `DATABASE_URL` in your hosting provider. Render can deploy this repository using the included `render.yaml`.

**Important:** This application is a document-card workflow/demo. It does not connect to UIDAI, PAN, Parivahan, or Election Commission databases and must not be presented as an official government portal.

## Deployment

This copy is prepared for production deployment with Gunicorn. Set `SECRET_KEY` to a strong random value and configure `DATABASE_URL` in your hosting provider. Render can deploy this repository using the included `render.yaml`.

**Important:** This application is a document-card workflow/demo. It does not connect to UIDAI, PAN, Parivahan, or Election Commission databases and must not be presented as an official government portal.

## Deployment

This copy is prepared for production deployment with Gunicorn. Set `SECRET_KEY` to a strong random value and configure `DATABASE_URL` in your hosting provider. Render can deploy this repository using the included `render.yaml`.

**Important:** This application is a document-card workflow/demo. It does not connect to UIDAI, PAN, Parivahan, or Election Commission databases and must not be presented as an official government portal.

## Deployment

This copy is prepared for production deployment with Gunicorn. Set `SECRET_KEY` to a strong random value and configure `DATABASE_URL` in your hosting provider. Render can deploy this repository using the included `render.yaml`.

**Important:** This application is a document-card workflow/demo. It does not connect to UIDAI, PAN, Parivahan, or Election Commission databases and must not be presented as an official government portal.

## Deployment

This copy is prepared for production deployment with Gunicorn. Set `SECRET_KEY` to a strong random value and configure `DATABASE_URL` in your hosting provider. Render can deploy this repository using the included `render.yaml`.

**Important:** This application is a document-card workflow/demo. It does not connect to UIDAI, PAN, Parivahan, or Election Commission databases and must not be presented as an official government portal.

## Deployment

This copy is prepared for production deployment with Gunicorn. Set `SECRET_KEY` to a strong random value and configure `DATABASE_URL` in your hosting provider. Render can deploy this repository using the included `render.yaml`.

**Important:** This application is a document-card workflow/demo. It does not connect to UIDAI, PAN, Parivahan, or Election Commission databases and must not be presented as an official government portal.
