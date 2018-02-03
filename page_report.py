import re
import sys
import pandas as pd


def get_url(l: str):
    """get URL address from log line l."""
    p = re.compile('(www\.)?[a-zA-Z.]+\.\w+((/\w+)+)?')
    url = re.search(p, l)
    return url.group()


def is_valid(l: str):
    """check if log line l has the valid format."""
    p = re.compile('(\d+\.){3}\d+ \[\d{,2}/\w+/\d{4}(:\d{2}){3} \+\d{4}\] ".*?" \d{3} \d+')
    result = re.search(p, l)
    if result:
        return result.group()
    else:
        return None


def to_sorted_df(urls_dict: dict):
    """Create pandas DataFrame from given dictionary and sort by occurrences and lexicographically."""
    df = pd.DataFrame(columns=["url", "number"], index=[])
    df["url"] = list(urls_dict.keys())
    df["number"] = list(urls_dict.values())
    df.sort_values(by=["number", "url"], inplace=True, ascending=[False, True])
    return df


with open(sys.argv[1]) as log_file:
    urls = {}
    invalid_lines = 0

    for line in log_file:
        if not is_valid(line):
            invalid_lines += 1
            continue
        url = get_url(line)
        if url is not None:
            if url in urls:
                urls[url] += 1
            else:
                urls[url] = 1

    urls = to_sorted_df(urls)

for index, row in urls.iterrows():
    print('"{}",{}'.format(row["url"], row["number"]))

if invalid_lines > 0:
    sys.stderr.write("Invalid log lines: {}\n".format(invalid_lines))
