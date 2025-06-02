# SheetToDB

A Django REST API for bulk uploading Employee and Company data from Excel/CSV files into a relational database.

## Features

- Upload `.csv` or `.xlsx` files containing employee data.
- Automatically creates companies and links employees to them.
- Uses efficient bulk database operations.
- Handles errors gracefully and reports them clearly.
- Transactional: all-or-nothing data import.

## Requirements

- Python 3.11+
- Django 5.1+
- djangorestframework
- pandas
- openpyxl (for `.xlsx` support)

## Setup

1. **Clone the repository and install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Create a superuser (optional, for admin):**
    ```bash
    python manage.py createsuperuser
    ```

4. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

### Bulk Upload API

- **Endpoint:** `POST /employee/upload/`
- **Payload:** `multipart/form-data` with a `file` field containing your `.csv` or `.xlsx` file.

#### Example using `curl`:

```bash
curl -X POST -F "file=@your_employees.xlsx" http://127.0.0.1:8000/employee/upload/
```

#### Expected columns in the file:

| EMPLOYEE_ID | FIRST_NAME | LAST_NAME | PHONE_NUMBER | COMPANY_NAME | SALARY | MANAGER_ID | DEPARTMENT_ID |
|-------------|------------|-----------|--------------|--------------|--------|------------|---------------|
| ...         | ...        | ...       | ...          | ...          | ...    | ...        | ...           |

### Error Handling

- Missing columns, file errors, or database errors will be reported in the API response with clear messages.
- If any error occurs during import, **no data will be saved** (transactional).

## Admin

- Access the Django admin at `/admin/` to view and manage companies and employees.
