import mechanize
from BeautifulSoup import BeautifulSoup

def parse_table(html):
    """
    Returns a list of lists. Each list is a row in the table.
    """
    soup = BeautifulSoup(html)
    # The 9th table down the page is the one with all the info.
    table = soup.findAll('table')[9]
    rows = table.findAll('tr')
    # Grab all the rows except for the first one, which is the 
    # header. Then grab all the cells except the last one, which 
    # is the form for the further information.
    return [
        [ cell.text for cell in row.findAll('td')[:-1] ]
        for row in rows[1:]
    ]

br = mechanize.Browser()
# Open up the main page
br.open('http://publichealth.lacounty.gov/rating/')
# Now grab the form on the main page that runs the database query
br.select_form(predicate=lambda x: x.action == 'http://publichealth.lacounty.gov/phcommon/public/eh/rating/ratesearchaction.cfm')
# Fill out the info on the form
br.form['type'] = ['Restaurant',]
br.form['sort'] = ['inspdt',]
# And submit
br.submit()

fin = []
i=0
# Now we grab the first 10 pages. At 100 per page,
# we should wind up with 1,000 restaurants.
while i< 20:
    # Collect the HTML 
    html = br.response().read()
    # Append to our big list
    fin.append(parse_table(html))
    # For some reason there are 130 or 131 forms on the page.
    # we want to grab and submit the last one, which is the 
    # one that has the big NEXT button.
    # It's 131 after the first page, because there's a PREVIOUS button.
    if i < 1:
        br.select_form(nr=129)
    else:
        br.select_form(nr=130)
    br.submit()
    i += 1

# Now let's write the file out.
with open("/Users/kschwen/Dev/personal/ona-mapping-talk/project/data/raw_inspections.csv", "w") as f:
    for page in fin:
        for row in page:
            # for each value in the row, we want to quote the string
            # (but replace any stray quotes in the existing value), 
            # join everything with a comma, and add a newline.
            f.write(",".join(map(lambda s: '"%s"' % s.replace('"',''), row)) + "\n")
