#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Andrew Schillinger"
__version__ = "0.0.0"
__license__ = "GPL-3.0"
__github__ = "https://github.com/doctor-ew/openai-codex-foxtrot"

import json
import logging
import openai

from dotenv import load_dotenv, dotenv_values

load_dotenv("env.env")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = dotenv_values("env.env")
openai.api_key = config["OPENAI_API_KEY"]

codex_prompt = '### READY ###\n\n##### Translate this function from C\n### C\n    \n    #include <stdio.h>\n        ' \
               'int main(void)\n        {\n          int count;\n          for(count=1;count<=500;count++)\n         ' \
               'printf("I will not throw paper airplanes in class.\\n");\n          return 0;\n        }\n          ' \
               '\n### BASIC\n\n10 FOR I=1 TO 500: PRINT "I will not throw paper airplanes in class."\n20 END\n\n### ' \
               'READY ###\n\n### C++\n\n#include <iostream>\nusing namespace std;\n\nint main()\n{\n    int count;\n ' \
               'for(count=1;count<=500;count++)\n        cout << "I will not throw paper airplanes in class." << ' \
               'endl;\n    return 0;\n}\n\n### READY ###\n\n### Python\n\ncount = 1\nwhile count <= 500:\n    print ' \
               '"I will not throw paper airplanes in class."\n    count += 1\n\n### READY ###\n\n '


def hello_world(event, context):
    restart_sequence = "### READY ###\n"

    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"{codex_prompt} \nlanguage: {event}\nreturned_code:",
        temperature=0,
        max_tokens=199,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###", "### READY ###"],
    )

    # return response
    # return f"lowly_human: {event}, Skippy: {response.choices[0].text}"
    return dict(language=event, returned_code=response.choices[0].text)


def handler(event, context):
    logger.info(f"\n |-o-| Event: {event} :: type: {type(event)}")

    msg = "javascript"

    body = dict(message=f"{hello_world(msg, context)}")

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Origin": "https://doctorew.com",
            "Access-Control-Allow-Origin": "https://*.doctorew.com",
            # "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(body),
    }
    logger.info(f"response: {response}")
    return response
