
import json
import os
import re
from utils_17 import extract_from_json, flatten_dict, replace_double_newline, format_flattened_dict, pfizer_ncts
import requests as req
import urllib.request

def get_trial(nct_id):
    """
    Return: the JSON data for a clinical trial given its NCT ID.
    """
    trial = req.get(f"https://clinicaltrials.gov/api/v2/studies/{nct_id}")
    trial_json = trial.json()
    return trial_json


def get_downloaded_json(list_of_nct_id):
    """
    Downloads and saves JSON file(s) locally for reference.
    """
    downloaded_json = []
    for nct_id in list_of_nct_id:
        trial = get_trial(nct_id)
        downloaded_json.append(trial)
        with open(f"{nct_id}.json", "w") as f:
            json.dump(trial, f, indent=4)
    return downloaded_json


def list_from_extracted_json(downloaded_json): 
    """
    Processes and saves extracted JSON file(s) locally for review
    Return: a list of documents.
    """
    documents_list  = []
    for json_file in downloaded_json:
        extracted_json = extract_from_json(json_file)
        nct_id = json_file['protocolSection']['identificationModule']['nctId']
        save_path = f"{nct_id}_extracted.json"
        with open(save_path, "w") as f:
            json.dump(extracted_json, f, indent=4)
        documents_list.append(extracted_json)
    return documents_list

def max_keys(documents_list):
    """
    Identifies the document with the maximum number of keys in a list of dictionaries.
    Return: a list of keys from the document with the maximum number of keys. 
    """
    max_index, _ = max(enumerate(documents_list), key=lambda x: len(x[1].keys()))
    all_keys = list(documents_list[max_index].keys())
    return all_keys


def adjust_metadata_keys(all_keys, keys_to_include):
    """
    To adjust the metadata keys used.
    Return: keys to exclude from list of all_keys not in list of keys_to_include.
    """
    keys_to_exclude = [key for key in all_keys if key not in keys_to_include]
    return keys_to_exclude

