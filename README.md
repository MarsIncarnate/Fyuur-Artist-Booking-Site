# Artist Booking Site: Fyyur

**Table of Contents**
- [Introduction](#introduction)
- [Overview](#overview)
- [Tech Stack (Dependencies)](#tech-stack-dependencies)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Acceptance Criteria](#acceptance-criteria)
- [Stand Out](#stand-out)

## Introduction

Fyyur is a web application for connecting artists and venues for live shows. It serves as a platform for artists to create profiles, venues to list their spaces, and users to discover and book shows. This project focuses on building the backend data models and interactions for Fyyur, utilizing a PostgreSQL database.

## Overview

Fyyur is designed to manage real data for artists, venues, and shows. It connects to a PostgreSQL database to provide functionality for creating new profiles, discovering artists and venues, and booking shows. By the end of this project, the application is expected to perform the following:

- Create new venues, artists, and shows.
- Search for venues and artists.
- View detailed information about a specific artist or venue.
- Distinguish between past and upcoming shows.
- Provide a functional platform for artists and venues to interact seamlessly.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
The project relies on the following technologies:
- **virtualenv**: Tool for creating isolated Python environments.
- **SQLAlchemy ORM**: Database Object-Relational Mapping library.
- **PostgreSQL**: Chosen as the primary database system.
- **Python3**: The server language.
- **Flask**: The web framework for building the application.
- **Flask-Migrate**: Used for managing database schema migrations.

You can install these dependencies using pip:
```bash
pip install virtualenv SQLAlchemy postgres Flask Flask-Migrate
```

### 2. Frontend Dependencies
The frontend is built using HTML, CSS, and JavaScript, with Bootstrap 3 for styling. Bootstrap is installed using Node Package Manager (NPM).

Ensure you have Node.js installed, and then install Bootstrap:

```bash
npm init -y
npm install bootstrap@3
```

## Project Structure
The project structure is organized as follows:

app.py: The main driver of the app, including SQLAlchemy models.
config.py: Configuration file for database URLs, CSRF generation, and more.
forms.py: Forms for creating new artists, shows, and venues.
requirements.txt: List of Python dependencies for the project.
static/: Contains static assets such as CSS, fonts, images, and JavaScript.
templates/: Templates for rendering pages.

## Development Setup
Clone the project repository to your local machine:
```bash
git clone https://github.com/MarsIncarnate/Fyuur-Artist-Booking-Site.git
cd fyyur
```
Set up a virtual environment and activate it:
```bash
python -m virtualenv env
source env/bin/activate
```

Install project dependencies using pip:
```bash
pip install -r requirements.txt
```

Run the development server:
```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Open your browser and access the project at http://127.0.0.1:5000/.

## Application Functionality
Fyyur is a feature-rich web application designed to facilitate the booking of artists and venues for live shows. The application provides a seamless user experience by harnessing real data for artists, venues, and shows. Key functionalities include:

Create and Manage: Users can create new artist and venue profiles, as well as manage shows and bookings.

Discover and Search: Fyyur empowers users to discover and search for artists and venues, providing a robust search experience.

Artist and Venue Details: Detailed artist and venue pages offer insights into their profiles, helping users make informed choices.

Show Management: Fyyur distinguishes between past and upcoming shows, enhancing the event organization process.

Search Enhancements: The search feature supports partial string matching and is case-insensitive, ensuring users find what they're looking for effortlessly.

## Contributing
Contributions are welcome! If you'd like to improve this project or have ideas for enhancements, please submit a pull request or open an issue.

## License
This project is licensed under the terms of the MIT License. You are free to use, modify, and distribute the code as per the license terms.




