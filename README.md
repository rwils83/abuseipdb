# AbuseIPDB API Scripts

## What is it?
Scripts to use the abuseIPDB.com api

## How do I use it?
AbuseIPDB API Shim. Examples mentioned is future release feature.  

optional arguments:  
  -h, --help            show this help message and exit  
  -c, --check-endpoint  Check single IP address using the check endpoint. Use with -f/--file to check multiple IPs from a line separated list. use --examples -check for examples on use.  
  -b, --blacklist-endpoint
                        Blacklist Endpoint. Generate a blacklist. Defaults to 90 Confidence or better and 1000 IPs. Based on subscription. use --examples -blacklist for examples on use  
  -r, --report-endpoint
                        Report Endpoint. Use to report IPs. Use --examples -report for examples on use  
  -cb, --check-block-endpoint
                        Check-block endpoint. Use to check network block. use --examples -check-block for examples on use  
  -br, --bulk-report-endpoint
                        Bulk Report Endpoint. Use to submit a csv file of IPs, see bulk_report_example.csv for structure. Not tested
  -ca, --clear-address-endpoint
                        Clear Address Endpoint. Use for removing a reported IP from your account. Use --examples -clear for examples on use  
  -f FILE, --file FILE  File  
  -i IP, --ip IP        IP address  
  -cr [CONFIDENCE_RATING], --confidence-rating [CONFIDENCE_RATING]
                        Define minimum Confidence Rating for black list, must be above 25. This is a paid subscription feature  
  -o, --output          Write to file. Does not use custom names, writes file to <report_for_ip.txt>  
  -do, --display-category-options
                        Use this to explain the categories for use with reporting  
  -cat [CATEGORY], --category [CATEGORY]
                        Use comma seperated list of category IDs. Run app with -do/--display-category-options to get list of options. To load from list, use -catf/--category-file instead. use --examples -categoryfor examples on
                        use  
  -catf CATEGORY_FILE, --category-file CATEGORY_FILE
                        Load a line seperated list of categories to report IPs with.  
  -sn NET_BLOCK, --net-block NET_BLOCK
                        Enter a subnet block with CIDR notation, ie 10.0.0.0/24. Free plan max is /24, basic Subscription is /20, premium is /16.  

## How can I help? 
:shrug: I will get to this part later