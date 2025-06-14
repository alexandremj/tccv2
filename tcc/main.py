from fastapi import FastAPI

from router import check, health, posts, token, users

app = FastAPI()

app.include_router(check.router)
app.include_router(health.router)
app.include_router(posts.router)
app.include_router(token.router)
app.include_router(users.router)
