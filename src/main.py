from application.app import app
from routing.kaiten import kaiten_router

app.include_router(kaiten_router)
