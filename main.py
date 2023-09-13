import argparse
import scraper
import requests

def PDCInspectorMain(args):
    # try catch error and re-login here

    ENROLL_STATE_TEXT = "--"
    # ENROLL_STATE_TEXT = "Enrol"

    eventInfos = scraper.dataProcessing(scraper.loginAndNavigation(args.path, args.domain))
    
    eventEnrollAvailArr = [eventEl[-1] for eventEl in eventInfos]

    availCount = 0
    for availBool in eventEnrollAvailArr:
        if(ENROLL_STATE_TEXT in availBool):
            availCount += 1
    if(availCount != 0):    
        requests.post("https://ntfy.sh/HKUSTPDCInspector",
            data="{} new wild PDC {}.".format(availCount, "event emerges" if availCount == 1 else "events emerge").encode(encoding='utf-8'))

    # if("DLE" in eventServiceUnits):
    #     requests.post("https://ntfy.sh/HKUSTPDCInspector",
    #         data="A new wild PDC event emerges".encode(encoding='utf-8'))
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default='./account_info.ini', help="Path to the user account information, if none, defaults to the account_info.ini")
    parser.add_argument("--domain", type=str, default='hkustgz', help="Domain, determines email suffix, hkust or hkustgz")

    args = parser.parse_args()

    PDCInspectorMain(args=args)