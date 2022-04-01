from dotenv import load_dotenv
import uvicorn
from main import app
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="127.0.0.1", port=8000)
