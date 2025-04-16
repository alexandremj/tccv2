from fastapi import FastAPI

from router import health, posts, users

app = FastAPI()

app.include_router(health.router)
app.include_router(posts.router)
app.include_router(users.router)

