import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.main:create_app", host="127.0.0.1", port=54, factory=True, log_level="info")