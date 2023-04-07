import argparse
import scraper
import requests

def PDCInspectorMain(args):
    # try catch error and re-login here
    eventInfos = scraper.dataProcessing(scraper.loginAndNavigation(args.path, args.domain))
    
    eventServiceUnits = [eventEl[2] for eventEl in eventInfos]
    if("DLE" in eventServiceUnits):
        requests.post("https://ntfy.sh/HKUSTPDCInspector",
            data="A new wild PDC event emerges".encode(encoding='utf-8'))
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default='./account_info.ini', help="Path to the user account information, if none, defaults to the account_info.ini")
    parser.add_argument("--domain", type=str, default='hkustgz', help="Domain, determines email suffix, hkust or hkustgz")

    args = parser.parse_args()

    PDCInspectorMain(args=args)