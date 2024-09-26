from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import auth, foods, users
from app.db.session import engine
from app.models.user import Base

app = FastAPI(
    title="User Management API",
    description=(
        "This API provides endpoints for managing user profiles. "
        "Users can be created, updated, deleted, and retrieved by their ID or email. "
        "The API supports uploading profile pictures, which are stored on the server. "
        "Key features include:\n"
        "- **User Registration**: Create new user profiles.\n"
        "- **User Retrieval**: Fetch user details.\n"
        "- **Profile Updates**: Update user information.\n"
        "- **Image Uploads**: Upload and store profile pictures securely.\n"
        "- **Automatic Validation**: Ensure input data meets specified criteria.\n"
        "- **Interactive Documentation**: Access API docs via Swagger UI at `/docs`.\n"
        "- **Asynchronous Processing**: Efficient request handling."
    ),
    version="1.0.0",
    contact={
        "name": "Penh Seyha",
        "url": "https://www.facebook.com/seyha.soul.3152/",
        "email": "penhseyha4980@gmail.com",
    },
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
    # terms_of_service="http://example.com/terms",
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include the users API
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(foods.router, prefix="/api/v1", tags=["Foods"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
