Property data scrapers
    - Scrape property websites for data. NEED TO ADD LINK TO EACH PROPERTY SAVED TO DB
    - Save properties to a database
    - Creates a table for each city searched for in the database
    - If a record already exists in the DB, it does not save a duplicate
    - Can also save to a spreadsheet, and records average price in a txt file. Will do more with that later.
    - Could combine the scripts to do one large search
        - Could make a scraper "class" with the various soup selectors as class attributes and links/hrefs also? 
        - Or just use separate functions, one for each website, and call them sequentially?
        - Making a parent scraper class may help me avoid writing a whole new script for each property website I want to add though...or will it? Scraping has to be so specially customised...