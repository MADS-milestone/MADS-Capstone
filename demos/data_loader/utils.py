def add_field_if_exists(source_dict, target_dict, target_key_name, source_key_name):
    if source_key_name in source_dict:
        target_dict[target_key_name] = source_dict[source_key_name]


def build_target_json(source_json):
    target_json = {}

    protocolSection = source_json["protocolSection"]
    identificationModule = protocolSection["identificationModule"]
    statusModule = protocolSection["statusModule"]
    sponsorCollaboratorsModule = protocolSection["sponsorCollaboratorsModule"]
    descriptionModule = protocolSection["descriptionModule"]
    conditionsModule = protocolSection["conditionsModule"]
    designModule = protocolSection["designModule"]

    target_json["trial id"] = identificationModule["nctId"]
    organizationStruct = identificationModule["organization"]
    target_json["organization"] = organizationStruct["fullName"]
    add_field_if_exists(identificationModule, target_json, "brief title", "briefTitle")
    add_field_if_exists(identificationModule, target_json, "official title", "officialTitle")
    target_json["overall status"] = statusModule["overallStatus"]

    startDateStruct = statusModule["startDateStruct"]
    completionDateStruct = statusModule["completionDateStruct"]
    add_field_if_exists(startDateStruct, target_json, "start date", "date")
    target_json["start date"] = statusModule.get("startDateStruct", {})
    add_field_if_exists(completionDateStruct, target_json, "completion date", "date")

    if "leadSponsor" in sponsorCollaboratorsModule:
        leadSponsorModule = sponsorCollaboratorsModule["leadSponsor"]
        add_field_if_exists(leadSponsorModule, target_json, "lead sponsor", "leadSponsor")
    if "collaborators" in sponsorCollaboratorsModule:
        collaboratorsModule = sponsorCollaboratorsModule["collaborators"]
        add_field_if_exists(collaboratorsModule, target_json, "collaborators", "collaborators")

    oversightModule = protocolSection["oversightModule"]
    add_field_if_exists(oversightModule, target_json, "oversight has DMC", "oversightHasDmc")
    add_field_if_exists(oversightModule, target_json, "oversight has DMC", "isFdaRegulatedDrug")
    add_field_if_exists(oversightModule, target_json, "is FDA regulated device", 'isFdaRegulatedDevice')
    add_field_if_exists(descriptionModule, target_json, "brief summary", "briefSummary")
    add_field_if_exists(descriptionModule, target_json, "detailed description", "detailedDescription")
    add_field_if_exists(conditionsModule, target_json, "conditions", "conditions")
    add_field_if_exists(conditionsModule, target_json, "keywords", "keywords")

    if "armsInterventionsModule" in protocolSection:
        armsInterventionsModule = protocolSection["armsInterventionsModule"]
        add_field_if_exists(armsInterventionsModule, target_json, "arm groups", "argGroups")
        add_field_if_exists(armsInterventionsModule, target_json, "interventions", "interventions")

    if "outcomesModule" in protocolSection:
        outcomesModule = protocolSection["outcomesModule"]
        add_field_if_exists(outcomesModule, target_json, "primary outcomes", "primaryOutcomes")
        add_field_if_exists(outcomesModule, target_json, "secondary outcomes", "secondaryOutcomes")

    eligibilityModule = protocolSection["eligibilityModule"]
    add_field_if_exists(eligibilityModule, target_json, "eligibility criteria", "eligibilityCriteria")
    add_field_if_exists(eligibilityModule, target_json, "sex", "sex")
    add_field_if_exists(eligibilityModule, target_json, "minimum age", "minimumAge")
    add_field_if_exists(eligibilityModule, target_json, "maximum age", "maximumAge")

    contactsLocationsModule = protocolSection["contactsLocationsModule"]
    add_field_if_exists(contactsLocationsModule, target_json, "overall officials", "overallOfficials")

    if "resultsSection" in source_json:
        resultsSection = source_json["resultsSection"]

        if 'participantFlowModule' in resultsSection:
            participantFlowModule = resultsSection['participantFlowModule']
            add_field_if_exists(participantFlowModule, target_json, "pre-assignment details", "preAssignmentDetails")
            add_field_if_exists(participantFlowModule, target_json, "recruitment details", "recruitmentDetails")
            add_field_if_exists(participantFlowModule, target_json, "participant flow groups", "groups")

        if "baselineCharacteristicsModule" in resultsSection:
            baselineCharacteristicsModule = resultsSection['baselineCharacteristicsModule']
            add_field_if_exists(baselineCharacteristicsModule, target_json, "population description",
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
                add_field_if_exists(limitationsAndCaveats, target_json, "limitations and caveats", "description")
            add_field_if_exists(moreInfoModule, target_json, "point of contact", "pointOfContact")

        return target_json

