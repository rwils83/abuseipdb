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


def blacklist_endpoint(base_url, confidenceRating="90"):
    url = base_url+"/blacklist"
    querystring = {'confidenceMinimum': confidenceRating,
                   'limit': '9999999'}
    headers = {
        "Accept": 'application/json',
        'Key': config['api-key']
    }
    r = requests.get(url, headers=headers, params=querystring)
    response = r.json()['data']
    with open(f"Black_List_created_{r.json()['meta']['generatedAt'].split('T')[0]}", "w+") as f:
        for entry in response:
            f.write(entry['ipAddress']+"\n")
    print("Generated Blacklist")


def report_endpoint(base_url, ip, cats, comment, cat_file):
    cat_list = []
    url = base_url+"/report"
    if cat_file is not None:
        with open(cat_file, 'r') as f:
            for line in f.readlines():
                cat_list.append(line.strip())
    else:
        for category in cats.split(","):
            cat_list.append(category)
    params = {
        "ip": ip,
        'categories': ",".join(cat_list),
        'comment': comment
              }


def bulk_report_endpoint(base_url, csv_file):
    url = base_url+"/bulk-report"
    files = {
        'csv': (csv_file, open(csv_file, 'rb'))
    }
    headers = {
        'Accept': 'application/json',
        'Key': config['api-key']
    }
    r = requests.post(url=url, headers=headers, files=files)
    if r.status_code != 200:
        return "Bulk Report Failed"
    else:
        return f"Successfully reported {r.json()['data']['savedReports']}"


def check_block_endpoint(base_url, ip):
    url = base_url+"/check-block"
    if "/" not in ip:
        return "Please use CIDR notation for block. Use -h for example"
    querystring = {
        'network':ip,
        'maxAgeInDays':"30"
    }
    headers = {
        'Accept': 'application/json',
        'Key':config['api-key']
    }
    r = requests.get(
        url=url,
        headers=headers,
        params=querystring
    )
    print(r.status_code)
    if r.status_code == 402:
        return "Please review help file for max block. API returned Payment Required"
    else:
        response = r.json()
        file = f'reported_for_netblock_{ip.replace("/", "_")}.txt'
        with open(file, 'w') as f:
            f.write(f"Network Address: {response['data']['networkAddress']}\nNetmask: {response['data']['netmask']}\nReported Address:\n")
            for line in response['data']['reportedAddress']:
                f.write(f'_____________________\nAddress: {line["ipAddress"]}\nLast Reported: {line["mostRecentReport"].split("T")[0]}\nAbuse Confidence: {line["abuseConfidenceScore"]}\nCountry: {line["countryCode"]}\n')
        return f"[+] Complete. View {file} for report."


def clear_address_endpoint(base_url, ip):
    url = base_url+"/clear-address"
    querystring = {
        'ipAddress': ip
    }
    headers = {
        'Accept': 'application/json',
        'Key': config['api-key']
    }
    r = requests.get(url=url, headers=headers, params=querystring)
    return r.content


def display_categories():
    cats = {}
    with open('cats.json', 'r') as f:
        cats.update(json.load(f))
    for category in cats['data']:
        print(f'Category ID: {category["id"]}\nCategory Name: {category["Information"]["Name"]}\nCategory Description: {category["Information"]["Description"]}')


def parse_args():
    description = "AbuseIPDB API Shim. Examples mentioned is future release feature."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-c",
        "--check-endpoint",
        action="store_true",
        help="Check single IP address using the check endpoint. Use with -f/--file to "
             "check multiple IPs from a line separated list. use --examples -check for examples on use."
    )
    parser.add_argument(
        "-b",
        "--blacklist-endpoint",
        action="store_true",
        help="Blacklist Endpoint. Generate a blacklist. Defaults to 90 Confidence or better and 1000 IPs. "
             "Based on subscription. use --examples -blacklist for examples on use"
    )
    parser.add_argument(
        "-r",
        "--report-endpoint",
        action="store_true",
        help="Report Endpoint. Use to report IPs. Use --examples -report for examples on use"
    )
    parser.add_argument(
        "-cb",
        "--check-block-endpoint",
        action="store_true",
        help="Check-block endpoint. Use to check network block. use --examples -check-block for examples on use"
    )
    parser.add_argument(
        "-br",
        "--bulk-report-endpoint",
        action="store_true",
        help="Bulk Report Endpoint. Use to submit a csv file of IPs, "
             "see bulk_report_example.csv for structure. Not tested"
    )
    parser.add_argument(
        "-ca",
        "--clear-address-endpoint",
        action="store_true",
        help="Clear Address Endpoint. Use for blah. Use --examples -clear for examples on use")
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        help="File"
    )
    parser.add_argument(
        "-i",
        "--ip",
        action="store",
        help="IP address"
    )
    parser.add_argument(
        "-cr", "--confidence-rating",
        action="store",
        nargs="?",
        default="90",
        help="Define minimum Confidence Rating for black list, must be above 25. This is a paid subscription feature"
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store_true",
        default=False,
        help="Write to file. Does not use custom names, writes file to <report_for_ip.txt>"
    )
    parser.add_argument(
        "-do",
        "--display-category-options",
        action="store_true",
        help="Use this to explain the categories for use with reporting"
    )
    parser.add_argument(
        "-cat",
        "--category",
        action="store",
        nargs="?",
        default="15",
        help="Use comma seperated list of category IDs. Run app with -do/--display-category-options "
             "to get list of options. To load from list, use -catf/--category-file instead. use --examples -category"
             "for examples on use"
    )
    parser.add_argument(
        "-catf",
        "--category-file",
        action="store",
        default=None,
        help="Load a line seperated list of categories to report IPs with."
    )
    parser.add_argument(
        "-sn",
        "--net-block",
        action="store",
        help="Enter a subnet block with CIDR notation, ie 10.0.0.0/24. "
             "\nFree plan max is /24, basic Subscription is /20, premium is /16."
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    if args.check_endpoint:
        if not args.file:
            print(check_endpoint(
                config['base-url'],
                args.ip,
                args.output,
                bulk_write=False)
            )
        else:
            with open(args.file, 'r') as f:
                for line in f.readlines():
                    result = check_endpoint(
                        config['base-url'],
                        line.strip(),
                        args.output,
                        bulk_write=True,
                        file=args.file
                    )
                    if result is not None:
                        print(result)
    if args.blacklist_endpoint:
        blacklist_endpoint(
            config['base-url'],
            confidenceRating=str(args.confidence_rating)
        )
    if args.report_endpoint:
        report_endpoint(
            config['base-url'],
            "127.0.0.2",
            cats=args.category,
            comment="From automated scanning results",
            cat_file=args.category_file
        )
    if args.check_block_endpoint:
        print("[+] Checking Subnet block, this may take a few minutes.")
        print(check_block_endpoint(
            base_url=config['base-url'],
            ip=args.net_block
        ))
    if args.bulk_report_endpoint:
        print(bulk_report_endpoint(
            base_url=config['base-url'],
            csv_file=args.bulk_report_file))
    if args.clear_address_endpoint:
        print(clear_address_endpoint(base_url=config['base-url'], ip=args.ip))
    if args.display_category_options:
        display_categories()
