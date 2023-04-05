import argparse
import scraper


if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--path", type=str, default='./account_info.ini', help="if none, defaults to the account_info.ini")

    eventInfos = scraper.dataProcessing(scraper.loginAndNavigation(""))
    
    # TODO: check whether non-CLE events in the eventInfos, use ntfy to send notification