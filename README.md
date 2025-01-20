# Capy Habits
[![Project Version][version-image]][version-url]
[![Backend][Backend-image]][Backend-url]
 
This is the back-end side of Capy Habits, a capybara habit tracker built with Next.js, TypeScript, and TailwindCSS. Users can log habits, track progress, and earn rewards for completing goals. Features include a dynamic capybara stack visualization, streak tracking, and a gacha system for customizing capybaras. 

---
## Author

***Johnathan Tuong Luong***
* *Released on* [Railway](https://capy-habit.up.railway.app/)
* *My professional profile on* [LinkedIn](https://www.linkedin.com/in/johnathan-luong/)

## Showcase

This project was designed to demonstrate:

* Python
* Django
  * Django Ninja
* PostgreSQL
* Railway

## Installation

### Prerequisites

Ensure the following are installed on your machine:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional but recommended)

---

### Setup and Deployment

#### 1. Clone the Repository
Clone the backend repository to your local machine:
```
git clone https://github.com/<your-username>/capy-habits-backend.git
cd capy-habits-backend
```
---
#### 2. Create .env File
Create .env file in the root to configure environment variables. For example:
```
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@host:port/dbname
```
---
#### 3. Build the Docker Image
Use the Dockerfile to build the backend image:
```
docker build -t capy-habits-backend .
```
---
#### 4. Run the Docker Container
Start the container with the following command:
```
docker run -p 8000:8000 --env-file .env capy-habits-backend
```


If you encounter any issues or have questions, feel free to open an issue in this repository and let me know!

<!-- Markdown link & img dfn's -->

[header-url]: github-template.png
[header-link]: https://github.com/alexandrerosseto

[repository-url]: https://github.com/alexandrerosseto/wbshopping

[cloud-provider-url]: https://wbshopping.herokuapp.com

[linkedin-url]: https://www.linkedin.com/in/alexandrerosseto

[wiki]: https://github.com/yourname/yourproject/wiki

[version-image]: https://img.shields.io/badge/Version-1.0.0-brightgreen?style=for-the-badge&logo=appveyor
[version-url]: https://img.shields.io/badge/version-1.0.0-green
[Frontend-image]: https://img.shields.io/badge/Frontend-Ionic-blue?style=for-the-badge
[Backend-image]: https://img.shields.io/badge/Backend-Django-important?style=for-the-badge
[Backend-url]: https://img.shields.io/badge/Backend-Django-important?style=for-the-badge
