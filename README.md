# Photo and Video Sharing API

A robust, production-grade backend application built with **FastAPI** and **Python** that handles user authentication, database persistence, and cloud-based media handling. Inspired by early-stage social platforms, this project serves as a comprehensive demonstration of secure backend architecture, RESTful API design, and media pipeline integration.

---

## Key Features

* **Secure Authentication & Authorization:** Implements robust user registration, login workflows, and protected routes.
* **RESTful API Architecture:** Cleanly structured endpoints built with **FastAPI** for managing user profiles, posts, and interactions.
* **Automated Data Validation:** Utilizes **Pydantic** to enforce strict type checking and validate request/response payloads.
* **Cloud Media Management & Transformations:** Integrated with **ImageKit** for cloud storage, fast asset delivery, and on-the-fly media manipulation (such as dynamic resizing, cropping, quality adjustments, and text overlays via URL parameters).
* **Database Integration:** Relational database setup handling structured user data and media metadata.

---

## Tech Stack

* **Framework:** FastAPI (Python)
* **Data Validation:** Pydantic
* **Media Storage & Processing:** ImageKit
* **Database & ORM:** SQL-based relational database integration

---

## Getting Started

### Prerequisites

* Python 3.10+
* pip (Python package manager)
* An active **ImageKit** account (for media storage and transformation features)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your configuration details (database URLs, secret keys, and ImageKit API keys):
   ```env
   DATABASE_URL=database_connection_string
   SECRET_KEY=secret_key
   IMAGEKIT_PUBLIC_KEY=imagekit_public_key
   IMAGEKIT_PRIVATE_KEY=imagekit_private_key
   IMAGEKIT_URL_ENDPOINT=imagekit_url_endpoint
   ```

5. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available locally at `http://127.0.0.1:8000`. You can access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

---
