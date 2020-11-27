delete_all_query = '''
    DELETE FROM restapi_ngo;
    DELETE FROM restapi_ngo_accreditations;
    DELETE FROM restapi_ngoaccreditation;
    DELETE FROM restapi_ngo_branches;
    DELETE FROM restapi_ngobranch;
    DELETE FROM restapi_ngo_topics;
    DELETE FROM restapi_ngocontact;
    DELETE FROM restapi_ngoaddress;
    DELETE FROM restapi_ngometadata_info_source;
    DELETE FROM restapi_ngodatasource;
    DELETE FROM restapi_ngometadata;
    DELETE FROM restapi_ngorepresentative;
    DELETE FROM restapi_ngostats;
    DELETE FROM restapi_ngotopic;
'''