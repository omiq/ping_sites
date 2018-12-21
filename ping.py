import socket
import requests
from bs4 import BeautifulSoup
import csv
import tldextract

# Turn on debugging to print an
# annoying amount of test data
debugging = False


def debug(err):
    if(debugging): print(err)


# Check the chosen site for datas
# URL can be a URL or just domain
def ping(url):

    # Defaults
    theme = "theme not found"
    genesis_found = 'N'
    ip = "404"

    # Have I been passed a URL or a domain?
    if(url.find("/") > 0):
        parsed = tldextract.extract(url)
        domain = parsed.domain + "." + parsed.suffix

    else:
        domain = url

    # Try to get the IP address
    try:
        ip = socket.gethostbyname(domain)
    except:
        ip = "404"


    # If we managed to get the IP then get the HTML and parse it
    if ("404" != ip):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        headers = {'User-Agent': user_agent}

        # Can we get the HTML?
        try:
            result = requests.get("http://" + domain, headers=headers)
        except:
            return

        # Get the CSS lines from the html
        # Fix needed for Minified
        html = result.text
        soup = BeautifulSoup(html, 'lxml')
        link_list = soup.find_all("link", rel="stylesheet")

        # Did we get a list back?
        if(len(link_list) == 0):
            debug(html)
        else:
            debug(link_list)

        # Look for the relevant lines:
        for item in link_list:
            if (str(item).find("stylesheet") > 0):
                if (str(item).find("themes") > 0):
                    atts = item['href'].split("/")
                    debug(len(atts))
                    if(len(atts) > 4):
                        if(atts[4]=="themes"):
                            theme = atts[5]
                        else:
                            debug("Att4: {}".format(atts[4]))
                    else:
                        debug("Atts: {}".format(atts))
                else:
                    debug("No themes")
            else:
                debug("No stylesheet")

        if (html.find("genesis")):
            genesis_found = 'Y'
        else:
            genesis_found = 'N'

    # Output the results to screen
    print(domain, end='')
    print(",{}".format(genesis_found), end='')
    print(",{}".format(theme), end='')
    print(",{}".format(ip))

    # Append to the output CSV
    with open('genesis_usage.csv', mode='a') as csv_w_file:
        csv_writer = csv.writer(csv_w_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([domain, genesis_found, theme, ip])


# Are we processing an input file?
run_csv = True
if(run_csv):
    with open('genesis-domains.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            ping(row[1])
else:
    # This domain will fail
    ping("andrenell.me")

