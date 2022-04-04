from dotenv import load_dotenv
import uvicorn
from main import app
from config import Settings as ST

if __name__ == "__main__":
    uvicorn.run(app, host=ST.HOST, port=ST.PORT)
