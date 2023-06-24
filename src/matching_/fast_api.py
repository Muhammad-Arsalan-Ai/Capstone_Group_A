import uvicorn
from fastapi import FastAPI
from match import match_councillor

app = FastAPI()

@app.get("/councillors/{report_id}/{number_of_doctors}")

def get_councillors(report_id: int, number_of_doctors: int = 10):
    result = match_councillor(report_id, number_of_doctors)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)