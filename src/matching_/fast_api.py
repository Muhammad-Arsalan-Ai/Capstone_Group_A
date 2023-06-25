import uvicorn # type: ignore
from fastapi import FastAPI
from match import find_top_councillors

app = FastAPI()

@app.get("/councillors/{report_id}/{number_of_doctors}")

def get_councillors(report_id: int, number_of_doctors: int = 10):
    """
    This function retrieves the top councillors based on a report ID and number of doctors.

    Parameters:
    - report_id (int): The ID of the report for which the top councillors are to be retrieved.
    - number_of_doctors (int): The number of top councillors to retrieve. Defaults to 10 if not specified.

    Returns:
    - list: A list of the top councillors based on the given report ID and number of doctors.

    Usage:
    - Call this function with the desired report ID and optionally specify the number of doctors.
    - The function internally calls the "find_top_councillors" function to retrieve the top councillors.
    - The retrieved top councillors are returned as the function's result.
    """

    results = find_top_councillors(report_id, number_of_doctors)
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)