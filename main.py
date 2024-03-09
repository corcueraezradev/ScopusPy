# -*- coding: utf-8 -*-
"""
Created on Thu June 18 2020 for Python 3.7+

Developer resources: https://dev.elsevier.com

This is a demonstration program provided as is. Using the Scopus API,
it retrieves results for a search .

To understand the query parameters used in these examples, please see the
static API documentation located at https://dev.elsevier.com/api_docs.html

@author: MEA, Elsevier | Principal Product Manager, Scopus

"""

import requests
import variables  # module holding authentication keys
from requests import Response


def print_results(results):
    for entry in results:
        print("{} \t {} \t {} \t {}".format(entry["prism:coverDate"], entry["dc:title"], entry["dc:creator"],
                                            entry["citedby-count"]))


def call_next(url):
    nextSearchResponse: Response = requests.get(url)
    nextSearchDict = nextSearchResponse.json()
    print_results(nextSearchDict["search-results"]["entry"])  # call helper function to print results
    for entry in nextSearchDict["search-results"]["link"]:  # iterate over the link object
        if entry["@ref"] == "next":
            call_next(entry["@href"])  # call call_next function with the next results


API_KEY = "d60da027f0e5ab5d5012275c6573e3c8"

query = input("Search: ")

# 1. create url
requestURL = "https://api.elsevier.com/content/search/scopus"

# 2. adding query parameters
queryParams = "query=TITLE-ABS-KEY(" + query+ ")&count=10&sort=citedby-count" + variables.API_KEY # + variables.INST_TOKEN

# 3. send request
searchResponse: Response = requests.get(requestURL, queryParams, headers={"Accept": "application/json"})

# 4. parse response
responseDict = searchResponse.json()

# 5. print some debug information
print("Number of results: {}".format(responseDict["search-results"]["opensearch:totalResults"]))
print("Search query: {}".format(responseDict["search-results"]["opensearch:Query"]["@searchTerms"]))

# 6. print out first results
print_results(responseDict["search-results"]["entry"])

# 7. call helper function to continue iterating over the results
call_next(responseDict["search-results"]["link"][2]["@href"])
