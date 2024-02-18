def rename_key(struct, old_name, new_name):
    if not struct:
        return
    if isinstance(struct, list):
        for d in struct:
            d[new_name] = d.pop(old_name)
    else:
        struct[new_name] = struct.pop(old_name)


def doc_append_text_if_exists(study_dict, doc, header, key_text):
    text = ""

    if key_text in study_dict:
        text = study_dict[key_text]

    if header:
        header = ["\n\n", header, "\n"]
    doc.extend(header)
    doc.append(text)


def add_meta_if_exists(study_dict, meta, meta_key_name, key_name):
    if key_name in study_dict:
        meta[meta_key_name] = study_dict[key_name]


def add_field_if_exists(source_dict, target_dict, target_key_name, source_key_name):
    if source_key_name in source_dict:
        target_dict[target_key_name] = source_dict[source_key_name]


def build_target_json(trial_json):
    doc_json = {}

    protocolSection = trial_json["protocolSection"]
    identificationModule = protocolSection["identificationModule"]
    statusModule = protocolSection["statusModule"]
    sponsorCollaboratorsModule = protocolSection["sponsorCollaboratorsModule"]
    descriptionModule = protocolSection["descriptionModule"]
    conditionsModule = protocolSection["conditionsModule"]
    designModule = protocolSection["designModule"]

    doc_json["trial id"] = identificationModule["nctId"]
    organizationStruct = identificationModule["organization"]
    doc_json["organization"] = organizationStruct["fullName"]
    add_field_if_exists(identificationModule, doc_json, "brief title", "briefTitle")
    add_field_if_exists(identificationModule, doc_json, "official title", "officialTitle")
    doc_json["overall status"] = statusModule["overallStatus"]

    startDateStruct = statusModule["startDateStruct"]
    completionDateStruct = statusModule["completionDateStruct"]
    add_field_if_exists(startDateStruct, doc_json, "start date", "date")
    add_field_if_exists(completionDateStruct, doc_json, "completion date", "date")

    if "leadSponsor" in sponsorCollaboratorsModule:
        leadSponsorModule = sponsorCollaboratorsModule["leadSponsor"]
        add_field_if_exists(leadSponsorModule, doc_json, "lead sponsor", "leadSponsor")
    if "collaborators" in sponsorCollaboratorsModule:
        collaboratorsModule = sponsorCollaboratorsModule["collaborators"]
        add_field_if_exists(collaboratorsModule, doc_json, "collaborators", "collaborators")
    oversightModule = protocolSection["oversightModule"]

    add_field_if_exists(oversightModule, doc_json, "oversight has DMC", "oversightHasDmc")
    add_field_if_exists(oversightModule, doc_json, "oversight has DMC", "isFdaRegulatedDrug")
    add_field_if_exists(oversightModule, doc_json, "is FDA regulated device", 'isFdaRegulatedDevice')
    add_field_if_exists(descriptionModule, doc_json, "brief summary", "briefSummary")
    add_field_if_exists(descriptionModule, doc_json, "detailed description", "detailedDescription")
    add_field_if_exists(conditionsModule, doc_json, "conditions", "conditions")
    add_field_if_exists(conditionsModule, doc_json, "keywords", "keywords")

    if "armsInterventionsModule" in protocolSection:
        armsInterventionsModule = protocolSection["armsInterventionsModule"]
        add_field_if_exists(armsInterventionsModule, doc_json, "arm groups", "argGroups")
        add_field_if_exists(armsInterventionsModule, doc_json, "interventions", "interventions")

    if "outcomesModule" in protocolSection:
        outcomesModule = protocolSection["outcomesModule"]
        add_field_if_exists(outcomesModule, doc_json, "primary outcomes", "primaryOutcomes")
        add_field_if_exists(outcomesModule, doc_json, "secondary outcomes", "secondaryOutcomes")

    eligibilityModule = protocolSection["eligibilityModule"]
    add_field_if_exists(eligibilityModule, doc_json, "eligibility criteria", "eligibilityCriteria")
    add_field_if_exists(eligibilityModule, doc_json, "sex", "sex")
    add_field_if_exists(eligibilityModule, doc_json, "minimum age", "minimumAge")
    add_field_if_exists(eligibilityModule, doc_json, "maximum age", "maximumAge")

    contactsLocationsModule = protocolSection["contactsLocationsModule"]
    add_meta_if_exists(contactsLocationsModule, doc_json, "overall officials", "overallOfficials")

    if "resultsSection" in trial_json:
        resultsSection = trial_json["resultsSection"]

        if 'participantFlowModule' in resultsSection:
            participantFlowModule = resultsSection['participantFlowModule']
            add_field_if_exists(participantFlowModule, doc_json, "pre-assignment details", "preAssignmentDetails")
            add_field_if_exists(participantFlowModule, doc_json, "recruitment details", "recruitmentDetails")
            add_field_if_exists(participantFlowModule, doc_json, "participant flow groups", "groups")

        if "baselineCharacteristicsModule" in resultsSection:
            baselineCharacteristicsModule = resultsSection['baselineCharacteristicsModule']
            add_field_if_exists(baselineCharacteristicsModule, doc_json, "population description",
                                      "populationDescription")

        # if 'outcomeMeasuresModule' in resultsSection:
        #     outcomeMeasuresModule = resultsSection['outcomeMeasuresModule']
        #     add_field_if_exists(outcomeMeasuresModule, doc_json, "outcome measures", "outcomeMeasures")

        # if 'adverseEventsModule' in resultsSection:
        #     add_field_if_exists(resultsSection, doc_json, "adverse events", 'adverseEventsModule')

        if 'moreInfoModule' in resultsSection:
            moreInfoModule = resultsSection['moreInfoModule']
            if "limitationsAndCaveats" in moreInfoModule:
                limitationsAndCaveats = moreInfoModule["limitationsAndCaveats"]
                add_field_if_exists(limitationsAndCaveats, doc_json, "limitations and caveats", "description")
            add_field_if_exists(moreInfoModule, doc_json, "point of contact", "pointOfContact")

        return doc_json

