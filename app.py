from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn


main_app = FastAPI(
    title="DARPA PARSER FastAPI", description="https://prosto-web.agency/darpa_fastapi/"
)


main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "All good",
                        "value": {
                            "code": 200,
                            "status": "success",
                            "content": [
                                {
                                    1: [],
                                    2: [],
                                    3: [],
                                    4: [],
                                    5: [],
                                },
                                {
                                    1: [],
                                    2: [],
                                    3: [],
                                    4: [],
                                    5: [],
                                },
                                {
                                    1: [],
                                    2: [],
                                    3: [],
                                    4: [],
                                    5: [],
                                },
                                "...",
                            ],
                        },
                    },
                }
            }
        },
    },
    500: {
        "description": "Server error",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Server error",
                        "value": {
                            "code": 500,
                            "status": "internal server error",
                        },
                    },
                }
            }
        },
    },
}


example = {
    "first": "str or None",
    "second": "str or None",
    "third": "str or None",
    "fourth": "str or None",
    "fifth": "str or None",
}


@main_app.post("/arpa_fastapi/get_programs", responses=responses)
async def get_programs(request_data: dict = example):
    try:
        tags = {
            "first": request_data["first_tag"],
            "second": request_data["second_tag"],
            "third": request_data["third_tag"],
            "fourth": request_data["fourth_tag"],
            "fifth": request_data["fifth_tag"],
        }
        match = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
        }
        with open("result.txt", "r", encoding="utf-8") as file:
            for line in file:
                counter = 0
                for key in tags.keys():
                    if tags[key] is not None and tags[key] in line:
                        counter += 1
                if counter > 0:
                    line_dict = {
                        "Name": line.split("|")[0],
                        "Lead_Paragraph": line.split("|")[1],
                        "Program_URL": line.split("|")[2],
                        "Office_Abbreviation": line.split("|")[3],
                        "Last_Modified": line.split("|")[4],
                        "PM_Name": line.split("|")[5],
                        "PM_URL": line.split("|")[6],
                        "Tags": line.split("|")[7],
                        "Description_Body": line.split("|")[8],
                        "Related_Content": line.split("|")[9],
                    }
                    match[counter].append(line_dict)
    except Exception:
        return JSONResponse({"code": 500, "status": "error"}, status_code=500)
    else:
        return JSONResponse(
            {"code": 200, "status": "success", "content": match},
            status_code=200,
        )


if __name__ == "__main__":
    uvicorn.run(main_app, host="0.0.0.0", port=8082)
