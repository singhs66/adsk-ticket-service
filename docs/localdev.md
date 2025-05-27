# Local Development & Testing

## 1. Clone the Repository
```bash
git clone <your-repo-url>
cd tickets
```

## 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Configure the Database
- Ensure you have a PostgreSQL database running.
- Update the `DATABASE_URL` in `app/daoLayer/database.py` to match your database credentials:
  ```python
  DATABASE_URL = "postgresql://<user>:<password>@<host>:<port>/<dbname>"
  ```
- Example:
  ```python
  DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/tickets_db"
  ```
- Create the database in PostgreSQL if it does not exist:
  ```bash
  createdb tickets_db
  ```

## 5. Run the Application Locally
```bash
uvicorn main:app --reload
```
- The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 6. Environment Variables
- Copy `.env.example` to `.env` and fill in your local values.
- For AWS/production, use ECS secrets and SSM Parameter Store as described in [secrets.md](./secrets.md).

## 7. How to run the service
- http://127.0.0.1:8000/tickets

For Docker/ECS deployment, see [docker.md](./docker.md).
