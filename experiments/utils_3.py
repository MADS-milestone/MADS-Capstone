def safe_get(d, keys, default=None):
    """
    Attempt to get a value from a nested dictionary(d) using a list of keys.
    Returns the value if found, else returns default (None).
    """
    for key in keys:
        try:
            d = d.get(key, default)
        except AttributeError:
            return default
    return d

def extract_from_json(clinical_study):
    # 0. Subset JSON
    extracted_json = {}

    # 1. PROTOCOL SECTION
    protocol_section = clinical_study.get("protocolSection", {})

    # 1.1. IDENTIFICATION MODULE
    identification_module = protocol_section.get("identificationModule", {})
    extracted_json = {
        "National Clinical Identification (NCT ID)": safe_get(identification_module, ["nctId"]),
        "Organization study identification": safe_get(identification_module, ["orgStudyIdInfo", "id"]),
        "EudraCT number": safe_get(identification_module, ["secondaryIdInfos", 0, "id"]),
        "Organization": safe_get(identification_module, ["organization", "fullName"]),
        "Organization class": safe_get(identification_module, ["organization", "class"]),
        "Brief title": safe_get(identification_module, ["briefTitle"]),
        "Official title": safe_get(identification_module, ["officialTitle"]),
    }

    # 1.2. STATUS MODULE
    status_module = protocol_section.get("statusModule", {})  # Make sure this is correctly pointing to your data structure
    extracted_json.update({
        "Overall status": safe_get(status_module, ["overallStatus"]),
        "Start date": safe_get(status_module, ["startDateStruct", "date"]),
        "Primary completion date": safe_get(status_module, ["primaryCompletionDateStruct", "date"]),
        "Completion date": safe_get(status_module, ["completionDateStruct", "date"]),
        "Verification date": safe_get(status_module, ["statusVerifiedDate"]),  
        
        "Study first submitted date": safe_get(status_module, ["studyFirstSubmitDate"]),
        "Results first submitted date": safe_get(status_module, ["resultsFirstSubmitDate"]),
        "Last update submitted date": safe_get(status_module, ["lastUpdateSubmitDate"]),
        "Last update posted date": safe_get(status_module, ["lastUpdatePostDateStruct", "date"]),
    
    })

    # 1.3. SPONSOR/COLLABORATORS MODULE
    sponsor_collaborators_module = protocol_section.get("sponsorCollaboratorsModule", {})
    extracted_json.update({
        "Lead sponsor": safe_get(sponsor_collaborators_module, ["leadSponsor","name"]),
        "Lead sponsor class": safe_get(sponsor_collaborators_module, ["leadSponsor","class"]),
    })

    # 1.4. DESCRIPTION MODULE
    description_module = protocol_section.get("descriptionModule", {})
    extracted_json.update({
        "Brief summary": safe_get(description_module, ["briefSummary"]),
        "Detailed description": safe_get(description_module, ["detailedDescription"]),
    })

    # 1.5. CONDITIONS MODULE
    conditions_module = protocol_section.get("conditionsModule", {})
    extracted_json.update({
        "Condition": safe_get(conditions_module, ["conditions"]),
        "Condition's keywords": safe_get(conditions_module, ["keywords"]),
    })

    # 1.6. DESIGN MODULE
    design_module = protocol_section.get("designModule", {})
    extracted_json.update({
        "Study type": safe_get(design_module, ["studyType"]),
        "Phases" : safe_get(design_module, ["phases"]),
        "Allocation": safe_get(design_module, ["designInfo", "allocation"]),
        "Intervention model": safe_get(design_module, ["designInfo", "interventionModel"]),
        "Primary purpose": safe_get(design_module, ["designInfo", "primaryPurpose"]),
        "Masking": safe_get(design_module, ["designInfo", "maskingInfo","masking"]),
        "Who is masked": safe_get(design_module, ["designInfo", "maskingInfo","whoMasked"]),
        "Enrollment count": safe_get(design_module, ["enrollmentInfo", "count"]),
        "Enrollment type": safe_get(design_module, ["enrollmentInfo", "type"]),
    })

    # 1.7. ARMS INTERVENTIONS MODULE
    arms_interventions_module = protocol_section.get("armsInterventionsModule", {})
    extracted_json.update({
        "Arms group 0 label": safe_get(arms_interventions_module, ["armGroups"])[0]["label"],
        "Arms group 0 type": safe_get(arms_interventions_module, ["armGroups"])[0]["type"],
        # "Arms group 0 description": safe_get(arms_interventions_module, ["armGroups"])[0]["description"],
        "Arms group 0 intervention names": safe_get(arms_interventions_module, ["armGroups"])[0]["interventionNames"],
        "Arms group 1 label": safe_get(arms_interventions_module, ["armGroups"])[1]["label"],
        "Arms group 1 type": safe_get(arms_interventions_module, ["armGroups"])[1]["type"],
    #     "Arms group 1 description": safe_get(arms_interventions_module, ["armGroups"])[1]["description"],
        "Arms group 1 intervention names": safe_get(arms_interventions_module, ["armGroups"])[1]["interventionNames"],

        "Arms group 0 intervention type": safe_get(arms_interventions_module, ["interventions"])[0]["type"],
        "Arms group 0 intervention name": safe_get(arms_interventions_module, ["interventions"])[0]["name"],
        # "Arms group 0 intervention description": safe_get(arms_interventions_module, ["interventions"])[0]["description"],
        "Arms group 0 intervention labels": safe_get(arms_interventions_module, ["interventions"])[0]["armGroupLabels"],
        "Arms group 1 intervention type": safe_get(arms_interventions_module, ["interventions"])[1]["type"],
        "Arms group 1 intervention name": safe_get(arms_interventions_module, ["interventions"])[1]["name"],
        # "Arms group 1 intervention description": safe_get(arms_interventions_module, ["interventions"])[1]["description"],
        "Arms group 1 intervention labels": safe_get(arms_interventions_module, ["interventions"])[1]["armGroupLabels"],    
    })

    # 1.8. OUTCOMES MODULE
    outcomes_module = protocol_section.get("outcomesModule", {})
    extracted_json.update({
        "Primary outcome": safe_get(outcomes_module, ["primaryOutcomes"])[0]["measure"],
        # "Primary outcome description": safe_get(outcomes_module, ["primaryOutcomes"])[0]["description"],
        "Primary outcome time frame": safe_get(outcomes_module, ["primaryOutcomes"])[0]["timeFrame"],
    })
    try:
        for i in range(len(safe_get(outcomes_module, ["secondaryOutcomes"]))):
            extracted_json.update({
            f"Secondary outcome {i} measure": safe_get(outcomes_module, ["secondaryOutcomes"])[i]["measure"],
            # f"Secondary outcome {i} description": safe_get(outcomes_module, ["secondaryOutcomes"])[i]["description"],
            f"Secondary outcome {i} time frame": safe_get(outcomes_module, ["secondaryOutcomes"])[i]["timeFrame"],
            })
    except: pass

    # 1.9. ELIGIBILITY MODULE
    eligibility_module = protocol_section.get("eligibilityModule", {})
    extracted_json.update({
        "Eligibility criteria": safe_get(eligibility_module, ["eligibilityCriteria"]).replace("\n", " "),
        "Eligibility of healthy volunteer": safe_get(eligibility_module, ["healthyVolunteers"]),
        "Eligibility sex": safe_get(eligibility_module, ["sex"]),
        "Eligibility minimum age": safe_get(eligibility_module, ["minimumAge"]),
        "Eligibility standard age": safe_get(eligibility_module, ["stdAges"]),
    })

    # 2. RESULTS SECTION
    results_section = clinical_study.get("resultsSection", {})
    extracted_json.update({
        "Pre-assignment details": safe_get(results_section, ["participantFlowModule", "preAssignmentDetails"]),
        "Recruitment details": safe_get(results_section, ["participantFlowModule", "recruitmentDetails"]),
        "Recruitment group 0 id": safe_get(results_section, ["participantFlowModule", "groups"])[0]["id"],
        "Recruitment group 0 title": safe_get(results_section, ["participantFlowModule", "groups"])[0]["title"],
        "Recruitment group 0 description": safe_get(results_section, ["participantFlowModule", "groups"])[0]["description"],
        "Recruitment group 1 id": safe_get(results_section, ["participantFlowModule", "groups"])[1]["id"],
        "Recruitment group 1 title": safe_get(results_section, ["participantFlowModule", "groups"])[1]["title"],
        "Recruitment group 1 description": safe_get(results_section, ["participantFlowModule", "groups"])[1]["description"],    

    })

    # 2.1. OUTCOMES MEASURES MODULE
    outcome_measures_module = results_section.get("outcomeMeasuresModule", {})
    try:
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["groupIds"],
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["groupDescription"],

        extracted_json.update({
        "Primary outcome group identifications": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["groupIds"],
        "Primary outcome group description": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["groupDescription"],
        })
    except: pass

    try:
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["pValue"],
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["statisticalMethod"],
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["paramType"],
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["paramValue"],

        extracted_json.update({
        "Primary outcome group p-value": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["pValue"],
        "Primary outcome group statistical method": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["statisticalMethod"],
        "Primary outcome group statistical method parameter type": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["paramType"],
        "Primary outcome group statistical method parameter value": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["paramValue"],
        })
    except: pass
    
    try:
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["ciPctValue"]
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["ciPctValue"],
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["ciLowerLimit"],
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["ciUpperLimit"],
        safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["estimateComment"],
        extracted_json.update({
        "Primary outcome group confidence interval percentage value": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["ciPctValue"],
        "Primary outcome group confidence interval lower limit": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["ciLowerLimit"],
        "Primary outcome group confidence interval upper limit": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["ciUpperLimit"],
        "Primary outcome group estimate comment": safe_get(outcome_measures_module, ["outcomeMeasures"])[0]["analyses"][0]["estimateComment"],
        })
    except: pass

    # 2.2. MORE INFO MODULE
    more_info_module = results_section.get("moreInfoModule", {})
    extracted_json.update({
        "Limitations and caveats": safe_get(more_info_module, ["limitationsAndCaveats", "description"] ),
    })

    # 3 HAS RESULTS SECTION
    has_results_section = clinical_study.get("hasResults", {})
    extracted_json.update({
        "Has results": has_results_section

    })

    return extracted_json

def flatten_data(data, path=""):
    flattened = []
    if isinstance(data, str):
        # Extract the last part of the path as the key
        key = path.split("/")[-1]
        # Remove the key and colon from the output
        flattened.append(f"{key}: {data}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
              flattened.extend(flatten_data(item, path + f"/{i}"))
    elif isinstance(data, dict):
        for key, value in data.items():
              flattened.extend(flatten_data(value, path + f"/{key}"))
    return flattened


