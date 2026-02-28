# Automotive Lubricants

This repository contains a full-stack application for managing and browsing automotive lubricant products.

## Structure

- `automotive-lubricants-backend/` - FastAPI backend with SQLite database
  - `main.py` - API definitions
  - `crud.py`, `models.py`, `schemas.py` - database logic
  - `auth.py` - authentication helpers
  - `database.py` - SQLAlchemy session and engine setup

- `automotive-lubricants-frontend/` - React Native (Expo) mobile app
  - Screens and components under `src/`
  - API client at `src/api/client.js`
  - Uses `react-native-vector-icons` for icons

## Getting Started

### Backend

1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r automotive-lubricants-backend/requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
4. API is available at `http://localhost:8000`.

### Frontend

1. Navigate to the frontend directory and install packages:
   ```bash
   cd automotive-lubricants-frontend
   npm install
   ```
2. Start the Expo development server:
   ```bash
   npx expo start -c
   ```
3. Open the app on a simulator or device via Expo.

## Adding Products

- Use the POST `/api/products` endpoint to insert new products. Example JSON:
  ```json
  {
    "name": "New Oil",
    "category": "Cars",
    "price": 29.99,
    "image": "https://example.com/image.jpg"
  }
  ```

## Dynamic Categories

Categories are fetched dynamically from the backend. New product categories automatically appear in the app once at least one product uses them.

---

Feel free to customize and extend the application as needed.