﻿# Planetarium API 🌌 - Installation and Launch Guide

Welcome to the journey through the stars with the Planetarium API! Follow this guide to smoothly install and launch the application using Docker.

## Features

- **JWT Authenticated:**
  - Secure your cosmic journey with JWT authentication.

- **Admin Panel (`/admin/`):**
  - Navigate through the cosmic dashboard with the Django admin panel.

- **API Documentation (`/api/doc/swagger/`):**
  - Explore the API with comprehensive documentation located at [http://localhost:8000/api/doc/swagger/](http://localhost:8000/api/doc/swagger/).

- **Managing Reservations and Tickets:**
  - Seamlessly handle orders and tickets for a stellar user experience.

- **Creating Astronomy Shows:**
  - Dive into the cinematic universe by creating astronomy shows with title, description and themes!

- **Creating Planetarium Domes:**
  - Establish celestial planetarium domes for immersive viewing experiences.

- **Adding Show Sessions:**
  - Schedule show sessions to bring the cosmic stories to life.

- **Filtering Astronomy Show and Show Sessions:**
  - Effortlessly filter through astronomy shows and show sessions to find the perfect cosmic adventure.

## Installation Guide

### Prerequisites

Before embarking on this cosmic adventure, ensure you have the following tools installed on your machine:

- Docker
- Git (if you choose to clone the repository)


1. **Clone the repository:**

   ```bash
   git clone https://github.com/kostomeister/planetarium_api_service
   ```

2. **Navigate to the project directory:**

   ```bash
   cd planetarium_api_service
   ```

3. **Pull the interstellar project:**

   ```bash
   docker pull kostomeist/planetarium_service
   ```


### Configure Environment

4. **Open the project in your preferred IDE and configure the `.env` file using `.env.sample` as your guide.**

   ```bash
   cp .env.sample .env
   ```

   Edit the `.env` file with the necessary configuration.

### Launch the Cosmic Vessels

5. **Run the following docker-compose command to initiate liftoff:**

   ```bash
   docker-compose up --build
   ```

   This command will build the necessary containers and launch the Planetarium API.

6. **You can create new user at [http://localhost:8000/api/user/register/]**
    
    ### Ex:

   🌌 **Email:** admin@gmail.com  
   🌌 **Password:** 123321


7. **Celestial Navigation**

   - Access the API at [http://localhost:8000/api/planetarium/](http://localhost:8000/api/planetarium/).
   - For authentication tokens, visit [http://localhost:8000/api/user/token/](http://localhost:8000/api/user/token/).


8. You can see swagger documentation at [http://localhost:8000/api/doc/swagger/]
![image](https://github.com/kostomeister/planetarium_api_service/assets/121522005/aeb44f5e-29e4-46d8-943e-24e14ada4c3a)



9. Or redoc [http://localhost:8000/api/doc/redoc/]
![image](https://github.com/kostomeister/planetarium_api_service/assets/121522005/a84bf696-f538-4c1d-a5f6-2c4970db6c8b)



## Conclusion

Congratulations! You've successfully launched the Planetarium API and are now ready to explore the cosmic wonders. Feel free to contribute and make this celestial journey even more extraordinary.

## DB SCHEMA
![image](https://github.com/kostomeister/planetarium_api_service/assets/121522005/9b0ed390-e70d-4ba6-813d-52601628f306)
