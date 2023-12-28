# README.md

## Project Description

This Django project implements a REST API for managing mountain passes. Tourists can submit information about a mountain pass, including coordinates, height, name, images, and user details, through the `submitData` endpoint. The submitted data is stored in a database, and users can retrieve, edit, or list their submitted mountain passes.

## Requirements

- annotated-types (version 0.6.0)
- anyio (version 3.7.1)
- asgiref (version 3.7.2)
- certifi (version 2023.11.17)
- charset-normalizer (version 3.3.2)
- click (version 8.1.7)
- defusedxml (version 0.7.1)
- Django (version 4.2.7)
- django-environ (version 0.11.2)
- django-filter (version 23.5)
- djangorestframework (version 3.14.0)
- dnspython (version 2.4.2)
- email-validator (version 2.1.0.post1)
- environ (version 1.0)
- fastapi (version 0.104.1)
- gunicorn (version 21.2.0)
- h11 (version 0.14.0)
- httpcore (version 1.0.2)
- httpie (version 3.2.2)
- httptools (version 0.6.1)
- httpx (version 0.25.2)
- idna (version 3.6)
- itsdangerous (version 2.1.2)
- Jinja2 (version 3.1.2)
- Markdown (version 3.5.1)
- markdown-it-py (version 3.0.0)
- MarkupSafe (version 2.1.3)
- mdurl (version 0.1.2)
- multidict (version 6.0.4)
- orjson (version 3.9.10)
- packaging (version 23.2)
- Pillow (version 10.1.0)
- psycopg2-binary (version 2.9.9)
- dj-database-url (version 0.5.0)
- pydantic (version 2.5.2)
- pydantic-extra-types (version 2.1.0)
- pydantic-settings (version 2.1.0)
- pydantic_core (version 2.14.5)
- Pygments (version 2.17.2)
- PySocks (version 1.7.1)
- python-dotenv (version 1.0.0)
- python-multipart (version 0.0.6)
- pytz (version 2023.3.post1)
- PyYAML (version 6.0.1)
- requests (version 2.31.0)
- requests-toolbelt (version 1.0.0)
- rich (version 13.7.0)
- sniffio (version 1.3.0)
- sqlparse (version 0.4.4)
- starlette (version 0.27.0)
- typing_extensions (version 4.8.0)
- ujson (version 5.8.0)
- urllib3 (version 2.1.0)
- uvicorn (version 0.24.0.post1)
- uvloop (version 0.19.0)
- watchfiles (version 0.21.0)
- websockets (version 12.0)


## Installation

1. Clone the repository:

```bash
git clone https://github.com/AyAmAlexson/SFSprints/tree/7ddc8d627d62a51d403be1e42e2152fced124732/1Sprint_one/Sprint_One
cd Sprint_One
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Run the development server:

```bash
python manage.py runserver
```

## API Endpoints

### `POST /api/submitData/`

Tourists submit information about a mountain pass through this endpoint.

#### Request:

- Method: `POST`
- Headers: Content-Type: application/json
- Body: JSON data as described in the project specifications

#### Response:

- Status Codes:
  - 200 OK: Successfully submitted
  - 400 Bad Request: Incomplete or incorrect data
  - 500 Internal Server Error: Database connection error

Example:

```json
{
  "status": 200,
  "message": "Submitted successfully",
  "id": 42
}
```

### `GET /api/submitData/<id>/`

Retrieve information about a specific mountain pass by its ID.

#### Request:

- Method: `GET`

#### Response:

- Status Code:
  - 200 OK: Successfully retrieved
  - 404 Not Found: Mountain pass not found

Example:

```json
{
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22 13:18:13",
  "user": {
    "email": "qwerty@mail.ru",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
  },
  "coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {"data": "<картинка1>", "title": "Седловина"},
    {"data": "<картинка>", "title": "Подъём"}
  ]
}
```

### `PATCH /api/submitData/<id>/`

Edit an existing mountain pass if it is in the "new" status.

#### Request:

- Method: `PATCH`
- Headers: Content-Type: application/json
- Body: JSON data with fields to be updated

#### Response:

- Status Codes:
  - 200 OK: Successfully edited
  - 400 Bad Request: Invalid request or cannot edit the record
  - 404 Not Found: Mountain pass not found

Example:

```json
{
  "status": 1,
  "message": "Record successfully edited"
}
```

### `GET /api/submitData/?user__email=<email>`

List data about all mountain passes submitted by a user with a specific email.

#### Request:

- Method: `GET`

#### Response:

- Status Code:
  - 200 OK: Successfully retrieved

Example:

```json
[
  {
    "beauty_title": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "add_time": "2021-09-22 13:18:13",
    "user": {
      "email": "qwerty@mail.ru",
      "fam": "Пупкин",
      "name": "Василий",
      "otc": "Иванович",
      "phone": "+7 555 55 55"
    },
    "coords": {
      "latitude": "45.3842",
      "longitude": "7.1525",
      "height": "1200"
    },
    "level": {
      "winter": "",
      "summer": "1А",
      "autumn": "1А",
      "spring": ""
    },
    "images": [
      {"data": "<картинка1>", "title": "Седловина"},
      {"data": "<картинка>", "title": "Подъём"}
    ]
  },
  // Additional mountain pass entries...
]
```

## Project Structure

- `mountapi/models.py`: Defines the data models (MountainPass and Image).
- `mountapi/serializers.py`: Serializers for converting complex data types to Python data types.
- `mountapi/managers.py`: Business logic for submitting data.
- `mountapi/views.py`: Defines API views for handling HTTP requests.
- `mountapi/urls.py`: URL patterns for routing requests to the appropriate views.


