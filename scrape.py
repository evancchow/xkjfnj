# Scrape the preambles.

from bs4 import BeautifulSoup
import urllib2
import string
import pdb

with open("constitution_links.csv", 'rb') as f:
    all_links = [line for line in f]

final_data = []
for cx, curr_url in enumerate(all_links):
    print "Url #{}".format(cx)

    page = urllib2.urlopen(curr_url.replace('\"',''))
    soup = BeautifulSoup(page.read())

    print "Fetching text ..."

    # Get the preamble which is the entire section under the first title.
    error_status = None
    level = 0
    while error_status is None:
        try:
            raw_preamble = soup.find_all('section',
                {'class':'article-list level%s article-title' % level})[0].get_text()
            error_status = 1
        except:
            # pdb.set_trace()
            level += 1
            pass

    # sometimes this fails because BeautifulSoup fails to parse the page.
    # Should look into this at some point.

    print "Filtering ..."

    # Filter out the nonprintable chars
    preamble = filter(lambda x: x in string.printable, raw_preamble)

    print "Getting rid of newlines ..."

    # Get ride of newlines, words "Preamble" and "Share" at the beginning
    preamble = [i for i in preamble.split('\n') 
        if len(i) > 0 and
        "Share" not in i]

    print "Testing for preamble ..."

    # First word should be "Preamble".
    if "Preamble" not in preamble[0]:
        print "Constitution #%d (zero indexed) has no preamble" % cx
        continue
    preamble = ' '.join(preamble[1:])

    print "Formatting for CSV ..."

    # Add for csv data
    country_date_info = curr_url.replace("https://www.constituteproject.org/constitution/","").replace('?lang=en','').lower().rstrip().split('_')
    country, date = '_'.join(country_date_info[:-1]), country_date_info[-1]
    entry = '%s\t%s\t%s' % (country, date, preamble)
    print entry[0:120]
    final_data.append(entry)

    print

print "Successfully extracted preambles!"

# Write out to text file
with open("preambles.csv", 'wb') as f:
    for line in final_data:
        f.write("%s\n" % line)