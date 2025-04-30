# tekktrik.dev

Code and infrastructure for https://tektkrik.dev

## Backend

The website backend is implemented in Python using Flask, using a mixture of static pages and
templates rendered using the Jinja engine. Static files like images and CSS are found within
the Flask app, but additional files used by templates such as JSON files can be found in the
``assets/`` folder.  Everything is containerized via Docker containers.

## Web Server

NGINX is used as a reverse proxy web server to serve content to clients. NGINX is also set up
to serve the static assets more efficiently. Gunicorn is used as the WSGI HTTP server that
actually runs the Flask code. Supervisor and systemd are used to startup the site on bootup,
as well as restart it if needed. All of this runs on a shared Linode Compute instance.

## UI

The UI is implemented using Bootstrap, which has plenty of available components to use. It
also allows customization of the design from mobile to desktop.

## Publishing Workflow & Test Server

This repository uses GitHub Actions to for it's CI/CD pipeline.  Any pull requests into ``main``
trigger spinning up the test subdomain https://test.tekktrik.dev, which will run the associated
test Flask app container. Closing the pull request (through merging or otherwise) will turn off
the supervisor task running the testing subdomain.  Pushes and merges into ``main`` cause the
CI to update the Flask app running the main site with the new additions.

## Tooling

Ojne of the Docker containers has a cronjob that updates the server by saving the results of a
GraphQL query to GitHub to download information about contributions every hour (as well as delete
outdated information).  It uses a tool I created called
[cronberry](https://github.com/tekktrik/cronberry), which manages updating the crontab during
updates to ``main``, though this is partially a holdover from pre-containerization.  I use
pre-commit for ensuring code is formatted, linted, and conforms to REUSE specifications.
