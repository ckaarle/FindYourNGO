delete_all_query = '''
    DELETE FROM restapi_ngo_topics;
    DELETE FROM restapi_ngotopic;
    DELETE FROM restapi_ngo_branches;
    DELETE FROM restapi_ngo_accreditations;
    DELETE FROM restapi_ngoreview;
    DELETE FROM restapi_ngoconnection;
    DELETE FROM restapi_ngoaccount;
    DELETE FROM restapi_ngofavourites;
    DELETE FROM restapi_ngofavourites_favourite_ngo;
    DELETE FROM restapi_ngopendingconnection;
    DELETE FROM restapi_ngo;
    DELETE FROM restapi_ngoaccreditation;
    DELETE FROM restapi_ngobranch;
    DELETE FROM restapi_ngo_topics;
    DELETE FROM restapi_ngocontact;
    DELETE FROM restapi_ngoaddress;
    DELETE FROM restapi_ngometadata_info_source;
    DELETE FROM restapi_ngodatasource;
    DELETE FROM restapi_ngometadata;
    DELETE FROM restapi_ngotwscore_tw_series;
    DELETE FROM restapi_ngotwscore;
    DELETE FROM restapi_ngorepresentative;
    DELETE FROM restapi_ngostats_type_of_organization;
    DELETE FROM restapi_ngostats;
    DELETE FROM restapi_ngotype;
    DELETE FROM restapi_ngocountry;
'''

delete_background_tasks_query = '''
    DELETE FROM background_task; 
'''
