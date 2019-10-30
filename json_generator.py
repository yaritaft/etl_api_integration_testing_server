import requests
import json
import os
import logging
import dotenv
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
dotenv.load_dotenv()






ENDPOINTS=['/cadences.json',
'/steps.json',
'/people.json',
'/cadence_memberships.json',
'/actions.json',
'/activities/emails.json',
]


def get_request(ENDPOINT, number_of_page):
    """Get data from one end point with a given page. """

    SALESLOFT_TOKEN = "Bearer " + os.getenv("SALESLOFT_API_KEY")
    SALESLOFT_HEADERS = {
        "Authorization": SALESLOFT_TOKEN,
        "Content-Type": "application/json",
    }
    SALESLOFT_API_URL="https://api.salesloft.com/v2"
    SALESLOFT_MAX_ENTRIES_PER_PAGE = 100
    response = requests.get(
        SALESLOFT_API_URL + ENDPOINT,
        params={
            "per_page": SALESLOFT_MAX_ENTRIES_PER_PAGE,
            "page": number_of_page,
        },
        headers=SALESLOFT_HEADERS,
    )
    return response

def get_from_endpoint(ENDPOINT, number_of_page=1):
    """Get data from one end point with a given page. """
    try:
        response = get_request(ENDPOINT, number_of_page)
        if response.status_code == 200:
            return response.json()
        else:
            counter = 0
            while (
                response.status_code != 200 and counter < 6
            ):  # retry if get was not successful
                response = get_request(ENDPOINT, number_of_page)
                counter = counter + 1
            if response.status_code == 200:
                return response.json()
            else:
                log.info(
                    f"There was an error accessing to this endpoint {ENDPOINT}. Page {number_of_page}. HTTP Code {response.status_code}"
                )
                return None
    except:
        log.info(
            f"There was an error accessing to this endpoint {ENDPOINT}. Page {number_of_page}"
        )
        return None

def get_everything_from_endpoint(ENDPOINT):
    # """Get data from one end point looping all pages. """
    try:
        page_number = 1
        response = get_from_endpoint(ENDPOINT, page_number)
        if response is not None:
            list_of_responses=['Null value']
            list_of_responses.append(response)
            while response["metadata"]["paging"]["next_page"] != None:
                # We  dont have everything
                page_number = page_number + 1
                response = get_from_endpoint(ENDPOINT, page_number)
                if response is not None:
                    list_of_responses.append(response)
                else:
                    log.info(
                        f"There was an error accessing to this endpoint {ENDPOINT} and this page number: {page_number}"
                    )
                    continue
            return list_of_responses
    except Exception as e:
        raise Exception(f'Could not work {e}')

def get_endpoints_data(ENDPOINTS):
    my_dict={}
    for endpoint in ENDPOINTS:
        list_of_responses=get_everything_from_endpoint(endpoint)
        my_dict[endpoint]=list_of_responses
    my_dict["/users.json"]=get_request("/users.json",1).json()
    return my_dict

my_dict=get_endpoints_data(ENDPOINTS)
with open("responses.json","w") as f:
    json.dump(my_dict,f)