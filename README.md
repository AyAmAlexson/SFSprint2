# README.md

## Project Description

This Django project implements a REST API for managing mountain passes. Tourists can submit information about a mountain pass, including coordinates, height, name, images, and user details, through the `submitData` endpoint. The submitted data is stored in a database, and users can retrieve, edit, or list their submitted mountain passes.

## Deployment

The API service is available online at
https://sfsprintapi-25a2a6aeebf2.herokuapp.com/api/

## API Endpoints

### `POST /api/submitData/`

Tourists submit information about a mountain pass through this endpoint.

#### Request:

- Method: `POST`
- Headers: Content-Type: application/json
- Body: JSON data as described in the project specifications

Example (using httpie):
- http POST https://sfsprintapi-25a2a6aeebf2.herokuapp.com/api/submitData/ beauty_title="пер. " title="Пхия" other_titles="Триев" connect="" add_time="2021-09-22 13:18:13" user=4 coords:='{"latitude": "45.3842", "longitude": "7.1525", "height": "1200"}' level:='{"winter": "", "summer": "1А", "autumn": "1А", "spring": ""}' images:='[{"data": "<картинка1>", "title": "Седловина"}, {"data": "<картинка>", "title": "Подъём"}]'

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

### `POST /api/createUser/`

Registers a new user

#### Request:

- Method: `POST`
- Headers: Content-Type: application/json
- Body: JSON data as described in the project specifications

Example (using httpie):
- http POST https://sfsprintapi-25a2a6aeebf2.herokuapp.com/api/createUser/ email="ivan@ivanov.com" phone="+1234567890" name="Иван" fam="Иванов" otc="Фомич"

#### Response:

- Status Codes:
  - 200 OK: Successfully submitted
  - 400 Bad Request: Incomplete or incorrect data
  - 500 Internal Server Error: Database connection error


### `GET /api/getData/<id>/`

Retrieve information about a specific mountain pass by its ID.

#### Request:

- Method: `GET`

Example (using httpie):
- http GET https://sfsprintapi-25a2a6aeebf2.herokuapp.com/api/getData/1/


#### Response:

- Status Code:
  - 200 OK: Successfully retrieved
  - 404 Not Found: Mountain pass not found


### `PATCH /api/editData/<id>/`

Edit an existing mountain pass if it is in the "new" status.

#### Request:

- Method: `PATCH`
- Headers: Content-Type: application/json
- Body: JSON data with fields to be updated

Example (using httpie):
- http PATCH https://sfsprintapi-25a2a6aeebf2.herokuapp.com/api/editData/2/ beauty_title="пер. " title="Боржоми" other_titles="Апсны" connect="Cакартвело" 

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

### `GET /api/userMountainPassList/?user__email=<email>`

List data about all mountain passes submitted by a user with a specific email.

#### Request:

- Method: `GET`

Example (using httpie):
- http GET https://sfsprintapi-25a2a6aeebf2.herokuapp.com/api/userMountainPassList/\?user__email=ivan123@ivanov123.com

#### Response:

- Status Code:
  - 200 OK: Successfully retrieved


## Project Structure

- `mountapi/models.py`: Defines the data models (MountainPass and Image).
- `mountapi/serializers.py`: Serializers for converting complex data types to Python data types.
- `mountapi/managers.py`: Business logic for submitting data.
- `mountapi/views.py`: Defines API views for handling HTTP requests.
- `mountapi/urls.py`: URL patterns for routing requests to the appropriate views.


