def add_field_if_exists(source_dict, target_dict, target_key_name, source_key_name):
    if source_key_name in source_dict:
        target_dict[target_key_name] = source_dict[source_key_name]


def build_target_json(source_json):
    taget_json = {}

    protocolSection = source_json["protocolSection"]
    identificationModule = protocolSection["identificationModule"]
    statusModule = protocolSection["statusModule"]
    sponsorCollaboratorsModule = protocolSection["sponsorCollaboratorsModule"]
    descriptionModule = protocolSection["descriptionModule"]
    conditionsModule = protocolSection["conditionsModule"]
    designModule = protocolSection["designModule"]

    taget_json["trial id"] = identificationModule["nctId"]
    organizationStruct = identificationModule["organization"]
    taget_json["organization"] = organizationStruct["fullName"]
    add_field_if_exists(identificationModule, taget_json, "brief title", "briefTitle")
    add_field_if_exists(identificationModule, taget_json, "official title", "officialTitle")
    taget_json["overall status"] = statusModule["overallStatus"]

    startDateStruct = statusModule["startDateStruct"]
    completionDateStruct = statusModule["completionDateStruct"]
    add_field_if_exists(startDateStruct, taget_json, "start date", "date")
    taget_json["start date"] = statusModule.get("startDateStruct", {})
    add_field_if_exists(completionDateStruct, taget_json, "completion date", "date")

    if "leadSponsor" in sponsorCollaboratorsModule:
        leadSponsorModule = sponsorCollaboratorsModule["leadSponsor"]
        add_field_if_exists(leadSponsorModule, taget_json, "lead sponsor", "leadSponsor")
    if "collaborators" in sponsorCollaboratorsModule:
        collaboratorsModule = sponsorCollaboratorsModule["collaborators"]
        add_field_if_exists(collaboratorsModule, taget_json, "collaborators", "collaborators")

    oversightModule = protocolSection["oversightModule"]
    add_field_if_exists(oversightModule, taget_json, "oversight has DMC", "oversightHasDmc")
    add_field_if_exists(oversightModule, taget_json, "oversight has DMC", "isFdaRegulatedDrug")
    add_field_if_exists(oversightModule, taget_json, "is FDA regulated device", 'isFdaRegulatedDevice')
    add_field_if_exists(descriptionModule, taget_json, "brief summary", "briefSummary")
    add_field_if_exists(descriptionModule, taget_json, "detailed description", "detailedDescription")
    add_field_if_exists(conditionsModule, taget_json, "conditions", "conditions")
    add_field_if_exists(conditionsModule, taget_json, "keywords", "keywords")

    if "armsInterventionsModule" in protocolSection:
        armsInterventionsModule = protocolSection["armsInterventionsModule"]
        add_field_if_exists(armsInterventionsModule, taget_json, "arm groups", "argGroups")
        add_field_if_exists(armsInterventionsModule, taget_json, "interventions", "interventions")

    if "outcomesModule" in protocolSection:
        outcomesModule = protocolSection["outcomesModule"]
        add_field_if_exists(outcomesModule, taget_json, "primary outcomes", "primaryOutcomes")
        add_field_if_exists(outcomesModule, taget_json, "secondary outcomes", "secondaryOutcomes")

    eligibilityModule = protocolSection["eligibilityModule"]
    add_field_if_exists(eligibilityModule, taget_json, "eligibility criteria", "eligibilityCriteria")
    add_field_if_exists(eligibilityModule, taget_json, "sex", "sex")
    add_field_if_exists(eligibilityModule, taget_json, "minimum age", "minimumAge")
    add_field_if_exists(eligibilityModule, taget_json, "maximum age", "maximumAge")

    contactsLocationsModule = protocolSection["contactsLocationsModule"]
    add_field_if_exists(contactsLocationsModule, taget_json, "overall officials", "overallOfficials")

    if "resultsSection" in source_json:
        resultsSection = source_json["resultsSection"]

        if 'participantFlowModule' in resultsSection:
            participantFlowModule = resultsSection['participantFlowModule']
            add_field_if_exists(participantFlowModule, taget_json, "pre-assignment details", "preAssignmentDetails")
            add_field_if_exists(participantFlowModule, taget_json, "recruitment details", "recruitmentDetails")
            add_field_if_exists(participantFlowModule, taget_json, "participant flow groups", "groups")

        if "baselineCharacteristicsModule" in resultsSection:
            baselineCharacteristicsModule = resultsSection['baselineCharacteristicsModule']
            add_field_if_exists(baselineCharacteristicsModule, taget_json, "population description",
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
                add_field_if_exists(limitationsAndCaveats, taget_json, "limitations and caveats", "description")
            add_field_if_exists(moreInfoModule, taget_json, "point of contact", "pointOfContact")

        return taget_json

