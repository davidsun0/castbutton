import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

#gets build for youtube searcher
def get_authenticated_service():
    return build(API_SERVICE_NAME, API_VERSION, developerKey="YOUTUBE API KEY");

#Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if value:
                good_kwargs[key] = value
    return good_kwargs

#search method from google APIs. searches with kwargs
def search_list_by_keyword(service, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    results = service.search().list(
        **kwargs
    ).execute()
    return results

#search method for single query string. maxres is results per page
def search_by_keyword(query, maxres=10):
    service = get_authenticated_service()
    return search_list_by_keyword(service,
        part='snippet',
        maxResults=maxres,
        q=query,
        type='')

if __name__ == "__main__":
    service = get_authenticated_service()
    results = search_list_by_keyword(service,
        part='snippet',
        maxResults=1,
        q='never gonna give you up',
        type='')
    print(results)
