# SIH Prototype - AI Sports Talent Assessment

## Quick start

1. Create virtualenv and activate:
   - Windows:
     ```
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Mac/Linux:
     ```
     python -m venv venv
     source venv/bin/activate
     ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run backend:
   ```
   cd backend
   python app.py
   ```

4. Open `frontend/index.html` in browser and upload a short video (10-30s).  
   Results will be shown and saved to the SQLite DB (`backend/sports.db`).

Notes:
- Keep videos short for CPU-only processing.
- For mobile demo, you can use the frontend page on device and upload recorded videos.
