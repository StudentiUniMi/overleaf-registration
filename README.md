# Overleaf registration worker

Public user registration for a self-hosted 
[Overleaf](https://github.com/overleaf/overleaf) instance.

### Why?
We are planning to offer a public Overleaf instance to our users (students and teachers), 
but the Community Edition does not support autonomous user registration: only the site
administrator can create users via the admin panel.

This limitation is unacceptable for our use case, so we implemented it ourselves.

### How?
A simple form (available on `/register` path) is offered to the user asking for its email; 
the application then logs into the Overleaf instance with the administrator account
and sends a request to create a user. 

The user can now create an account by clicking the confirmation link on its mailbox.

## Deployment
There is a Docker image available on 
[ghcr.io/studentiunimi/overleaf-registration](https://ghcr.io/studentiunimi/overleaf-registration),
automatically built by GitHub Actions.
You can check the example `docker-compose.yml` file and tweak it with your configuration.

### Environment variables
The Docker container needs all the following environment variables to function properly:

| Environment variable | Description                                          |
|----------------------|------------------------------------------------------|
| `CAPTCHA_SERVER_KEY` | reCAPTCHA v2 server key                              |
| `CAPTCHA_CLIENT_KEY` | reCAPTCHA v2 client key                              |
| `OL_INSTANCE`        | Overleaf self-hosted instance (without trailing `/`) |
| `OL_ADMIN_EMAIL`     | Overleaf administrator account email                 |
| `OL_ADMIN_PASSWORD`  | Overleaf administrator account password              |
