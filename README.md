# Django Image Repository

Django Image Repository



## Objective:

    Build a Django backend and database to store approximately 300 photos.

    Provide an API with login functionality and authentication (bearer token) to retrieve images from the server.


### Existing URL Structure

    /about/: About page

    /api/register/: User registration

    /api/login/: User login

    /api/token/refresh/: Token refresh

    /api/retrieve-photos/: API to retrieve and store photos (requires authentication)


### API Usage

    Registration: POST /api/register/
        Send username and password data.
        Receive a token for use with APIs requiring authentication.

    Login: POST /api/login/
        Send username and password data.
        Receive a new token.

    Token Refresh: POST /api/token/refresh/
        Send the old token in the header Authorization: Bearer <your_token>.
        Receive a new token.

    Retrieve Photos: GET /api/retrieve-photos/
        Send the token in the header Authorization: Bearer <your_token>.
        Receive a list of photos from the server.
        