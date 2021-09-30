import json
import argparse
import requests

config = {}

with open("config.json", "r") as f:
    config.update(json.load(f))


def check_endpoint(base_url, ip, write_to_file, bulk_write, file=None):
    url = base_url
    querystring = {
        'ipAddress': f'{ip}',
        'maxAgeInDays': '90'
    }
    headers = {
        'Accept': 'application/json',
        'Key': config['api-key']
    }
    r = requests.get(url=url+"/check", headers=headers, params=querystring)
    response = r.json()['data']
    display = f"Report for {ip}\n_________________\nLast Reported: {response['lastReportedAt'].split('T')[0]}\nPublic IP: {response['isPublic']}\nAbuse Confidence: {response['abuseConfidenceScore']}%\nCountry: {response['countryCode']}\nTotal Reports: {response['totalReports']}"
    if write_to_file:
        if not bulk_write:
            with open(f"report_for_{ip.replace('.', '_')}.txt", 'w+') as f:
                f.write(display.strip())
        else:
            file = file.replace('\\', '').replace('.','_')
            with open(f'consolidated_report_for_{file}.txt', 'a') as f:
                f.write(display.strip()+"\n")
    else:
        return display


def blacklist_endpoint(base_url, ip):
    pass


def report_endpoint(base_url, ip):
    pass


def bulk_report_endpoint(base_url, ip):
    pass


def check_block_endpoint(base_url, ip):
    pass


def clear_address_endpoint(base_url, ip):
    pass


def parse_args():
    description = "AbuseIPDB API Shim"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-c", "--check-endpoint", action="store_true", help="Check single IP address using the check endpoint")
    parser.add_argument("-b", "--blacklist-endpoint", action="store_true", help="Blacklist Endpoint")
    parser.add_argument("-r", "--report-endpoint", action="store_true", help="Report Endpoint")
    parser.add_argument("-cb", "--check-block-endpoint", action="store_true", help="Check-block endpoint")
    parser.add_argument("-br", "--bulk-report-endpoint", action="store_true", help="Bulk Report Endpoint")
    parser.add_argument("-ca", "--clear-address-endpoint", action="store_true", help="Clear Address Endpoint")
    parser.add_argument("-f", "--file", action="store", help="File")
    parser.add_argument("-i", "--ip", action="store", help="IP address")
    parser.add_argument("-o", "--output", action="store_true", default=False, help="Write to file")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    if args.check_endpoint:
        if not args.file:
            print(check_endpoint(config['base-url'], args.ip, args.output, bulk_write=False))
        else:
            with open(args.file, 'r') as f:
                for line in f.readlines():
                    result = check_endpoint(config['base-url'], line.strip(), args.output, bulk_write=True, file=args.file)
                    if result is not None:
                        print(result)
    if args.blacklist_endpoint:
        pass
    if args.report_endpoint:
        pass
    if args.check_block_endpoint:
        pass
    if args.bulk_report_endpoint:
        pass
    if args.clear_address_endpoint:
        pass
