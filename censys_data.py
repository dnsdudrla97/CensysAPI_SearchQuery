import censys.data

c = censys.data.CensysData(api_id="API", api_secret="SECRET")

series_name = '22-ssh-banner-full_ipv4'

# Get a Series
ssh_series = c.view_series(series_name)

# View metadata for all the files in each scan
for scan in ssh_series['results']['historical']:
    print (c.view_result(series_name, scan['id']))