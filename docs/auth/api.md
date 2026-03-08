# Auth API Reference

## Overview

The Auth API provides endpoints for managing authentication and authorization, enabling secure access to resources.

## Endpoints

### POST /auth/login

Authenticate a user and generate an access token.

#### Parameters

| Name       | Type   | Required | Description                |
|------------|--------|----------|----------------------------|
| username   | string | Yes      | The username of the user.  |
| password   | string | Yes      | The password of the user.  |

#### Response

On success, returns an access token to be used for authenticated requests.

---

### POST /auth/logout

Invalidate the current access token, logging the user out.

#### Parameters

| Name       | Type   | Required | Description                |
|------------|--------|----------|----------------------------|
| token      | string | Yes      | The access token to revoke.|

#### Response

Returns a confirmation of successful logout.

---

### GET /auth/status

Check the authentication status of the current token.

#### Parameters

| Name       | Type   | Required | Description                |
|------------|--------|----------|----------------------------|
| token      | string | Yes      | The access token to verify.|

#### Response

Returns the authentication status of the token.

## Error Handling

The Auth API returns standard HTTP status codes to indicate the success or failure of an API request. Common error codes include:

- `400 Bad Request`: The request was invalid or cannot be served.
- `401 Unauthorized`: Authentication failed or access token is missing/invalid.
- `403 Forbidden`: The user does not have permission to access the resource.
- `500 Internal Server Error`: An unexpected error occurred on the server.
