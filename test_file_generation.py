
import json
import dotenv
import os
import requests
import logging
from salesloft_dictionary import SALESLOFT_PARAMETER_DICT
from json_generator import get_endpoints_data,get_everything_from_endpoint
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
dotenv.load_dotenv()
##############FILTERED FILES GENERATION
with open("responses.json","r") as f:
    api_data=json.load(f)

def unpack_parameters_generic_endpoint(endpoint_name):
    parameters_dict=SALESLOFT_PARAMETER_DICT
    parameters_dict=parameters_dict['data'][endpoint_name]
    multipage=(endpoint_name!='user') #every endpoint but user are multipage
    return (
        parameters_dict["endpoint"],
        parameters_dict["valid_keys"],
        parameters_dict["dictionary_fields"],
        parameters_dict["fields_to_rename"],
        multipage
    )

def filter_data(
    valid_keys, dictionary_fields, fields_to_rename, data
):
    data=data[1:]
    for one_data_endpoint in data:  #in testing file it is not a generator
        filtered_data = []
        print(one_data_endpoint)
        for one_dict_resource in one_data_endpoint['data']:
            # Drop unnecesary keys
            print(type(one_dict_resource))
            one_resource_filtered = {}
            for key in one_dict_resource.keys():
                if key in valid_keys:
                    one_resource_filtered[key] = one_dict_resource[key]

            # This is because these fields are dictionaries with href and id and we only want the ID field
            for key in dictionary_fields:
                log.debug("Value to undict: %s", one_resource_filtered[key])
                if one_resource_filtered[key] != None:
                    one_resource_filtered[key] = one_resource_filtered[key]["id"]
                    log.debug("Value undicted: %s", one_resource_filtered[key])
            # Key is old value, and Value is new value
            for field_to_rename in fields_to_rename:
                one_resource_filtered[field_to_rename["new"]] = one_resource_filtered[
                    field_to_rename["old"]
                ]
                del one_resource_filtered[field_to_rename["old"]]
            filtered_data.append(one_resource_filtered)
        yield filtered_data


def filter_user(
    valid_keys, dictionary_fields, fields_to_rename, data
):
    data=data['data']  
    filtered_data = []
    for one_dict_resource in data:
        # Drop unnecesary keys
        one_resource_filtered = {}
        for key in one_dict_resource.keys():
            if key in valid_keys:
                one_resource_filtered[key] = one_dict_resource[key]

        # This is because these fields are dictionaries with href and id and we only want the ID field
        for key in dictionary_fields:
            log.debug("Value to undict: %s", one_resource_filtered[key])
            if one_resource_filtered[key] != None:
                one_resource_filtered[key] = one_resource_filtered[key]["id"]
                log.debug("Value undicted: %s", one_resource_filtered[key])
        # Key is old value, and Value is new value
        for field_to_rename in fields_to_rename:
            one_resource_filtered[field_to_rename["new"]] = one_resource_filtered[
                field_to_rename["old"]
            ]
            del one_resource_filtered[field_to_rename["old"]]
        filtered_data.append(one_resource_filtered)
    yield filtered_data


_,valid_keys,dictionary_fields,field_to_rename,_=unpack_parameters_generic_endpoint("user")
user_filtered_data=list(filter_user(valid_keys,dictionary_fields,field_to_rename,api_data["/users.json"]))
_,valid_keys,dictionary_fields,field_to_rename,_=unpack_parameters_generic_endpoint("people")
people_filtered_data=list(filter_data(valid_keys,dictionary_fields,field_to_rename,api_data["/people.json"]))
_,valid_keys,dictionary_fields,field_to_rename,_=unpack_parameters_generic_endpoint("cadence_membership")
cad_mem_filtered_data=list(filter_data(valid_keys,dictionary_fields,field_to_rename,api_data["/cadence_memberships.json"]))

test_file_dict={"user":user_filtered_data,"people":people_filtered_data,"cadence_membership":cad_mem_filtered_data}

with open("test_file.json","w") as f:
    json.dump(test_file_dict,f)