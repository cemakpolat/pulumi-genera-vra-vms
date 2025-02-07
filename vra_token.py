#!/usr/bin/env python3
import argparse
import requests
import urllib3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="Set vRA Username <user.name>", required=True)
    parser.add_argument("-p", "--password", help="Set vRA Password", required=True)
    parser.add_argument(
        "-r", "--raw", help="Print raw refresh_token", action="store_true"
    )
    parser.add_argument("-d", "--domain", help="Set vRA Domain", default="lab.server.de")
    parser.add_argument(
        "-U",
        "--url",
        help="Set vRA Endpoint",
        default="https://vra.labwi.server.de/csp/gateway/am/api/login",
    )
    parser.add_argument(
        "-i",
        "--insecure",
        help="Use insecure when vra endpoint uses selfsigned certificates",
        action="store_true",
    )

    args = parser.parse_args()

    params = (("access_token", ""),)

    data = {
        "username": args.username,
        "password": args.password,
        "domain": args.domain,
    }

    if args.insecure:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(args.url, params=params, json=data, verify=False)
    else:
        response = requests.post(args.url, params=params, json=data, verify=True)

    json_response = response.json()
    try:
        token = json_response["refresh_token"]
    except KeyError:
        raise RuntimeError(
            "Unable to get the token. Returned message: {}".format(json_response)
        )

    if args.raw:
        print(token)
    else:
        print("Please copy/replace the following generated lines in the Pulumi.yaml file")
        print("vra:refresh_token = {0}".format(token))
        print("vra:url", args.domain)
        print("vra:insecure", args.insecure)


if __name__ == "__main__":
    main()
