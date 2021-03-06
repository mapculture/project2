'''
File Name: querywolfram.py
Authors: Kelemen Szimonisz
Organization: Math Culture

Most code borrowed from: https://towardsdatascience.com/build-your-next-project-with-wolfram-alpha-api-and-python-51c2c361d8b9

This python file defines the function that query Wolfram|Alpha's API for the step by step solution to an algebraic equation.
Last Modified: 11/29/2021
'''

from pprint import pprint
import requests
import os
import urllib.parse
import argparse
from flask import current_app


#########################################################################################
# FUNCTION: getStepByStep
# 
# Query Wolfram|Alpha's Step-by-Step API for a given equation
# The results are parsed and returned as a string.
#########################################################################################
def getStepByStep(equation):
    appid = "7WEQV6-Q7WGAPL9KE" 

    # URL quoting
    # encodes non-ASCII text to be used in a URL
    # also replaces spaces with plus signs, as required when building up a URL query string
    # Example: quote_plus('/El Niño/') yields '%2FEl+Ni%C3%B1o%2F'.
    query = urllib.parse.quote_plus(f"solve {equation}")

    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={appid}" \
                f"&input={query}" \
                f"&scanner=Solve" \
                f"&podstate=Result__Step-by-step+solution" \
                "&format=plaintext" \
                f"&output=json"

    r = requests.get(query_url).json()
    current_app.logger.info(r);
    success = r["queryresult"]["success"]
    if success == False:
        current_app.logger.info("Query returned with success=False. Likely a syntax error.")
        return "No solution. Improper syntax!"

    data = r["queryresult"]["pods"][0]["subpods"]
    num_subpods = r["queryresult"]["pods"][0]["numsubpods"]
    if num_subpods == 2:
        # there is a result and step-by-step solution
        result = data[0]["plaintext"]
        steps = data[1]["plaintext"]
        print(f"Result of {equation} is '{result}'.")
        print(f"Possible steps to solution:\n\n{steps}")
        return steps
    elif num_subpods == 1:
        # there is likely only a result
        # this happens in cases like: 65x + y, where the solution is one step: y= -65x
        result = data[0]["plaintext"]
        print(f"Result of {equation} is '{result}'.")
        return result

