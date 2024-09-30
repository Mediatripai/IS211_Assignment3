import argparse 
import csv
import re
from urllib.request import urlretrieve
from urllib.error import URLError
from datetime import datetime
from collections import Counter

def download_file(url, filename='weblog.csv'):
    try:
        urlretrieve(url, filename)
        return filename
    except URLError as e:
        print(f"Failed to download the file. Error: {e}")
        return None

def process_file(filename):
    image_hits = 0
    total_hits = 0
    browsers = Counter()
    hour_hits = Counter()

    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                # Check if row has enough columns
                if len(row) < 3:
                    continue

                total_hits += 1
                
                # Part III - Check for image hits
                if re.search(r'\.(jpg|gif|png)$', row[0], re.I):
                    image_hits += 1
                
                # Part IV - Browser popularity
                browser = get_browser(row[2])
                if browser:
                    browsers[browser] += 1
                
                # Part VI - Hits per hour
                try:
                    dt = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')  # Updated format
                    hour_hits[dt.hour] += 1
                except ValueError as e:
                    print(f"Error parsing date: {e}")
                    continue

        return image_hits, total_hits, browsers, hour_hits
    except FileNotFoundError:
        print("The file does not exist.")
        return None, None, None, None

def get_browser(user_agent):
    if 'Firefox' in user_agent:
        return 'Firefox'
    elif 'Chrome' in user_agent:
        return 'Chrome'
    elif 'MSIE' in user_agent or 'Trident' in user_agent:
        return 'Internet Explorer'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        return 'Safari'
    return None

def main():
    parser = argparse.ArgumentParser(description='Web Log Analysis')
    parser.add_argument('--url', required=True, help='URL of the web log file')  # Explicit --url parameter
    args = parser.parse_args()

    # Part I - Download the file
    filename = download_file(args.url)
    if not filename:
        return
    
    print(f"File downloaded as {filename}")

    # Part II & III - Process the file and search for image hits
    image_hits, total_hits, browsers, hour_hits = process_file(filename)
    if total_hits is None:
        return
    
    if total_hits > 0:
        image_percentage = (image_hits / total_hits) * 100
        print(f"Image requests account for {image_percentage:.1f}% of all requests")
    else:
        print("No hits recorded.")

    # Part IV - Most popular browser
    if browsers:
        most_popular_browser = browsers.most_common(1)[0][0]
        print(f"The most popular browser is {most_popular_browser}")
    else:
        print("No browser data available.")

    # Part VI - Extra Credit: Hits per hour
    if hour_hits:
        print("\nHits per hour:")
        for hour in sorted(hour_hits, key=hour_hits.get, reverse=True):
            print(f"Hour {hour:02d} has {hour_hits[hour]} hits")
    else:
        print("No hits per hour data available.")

if __name__ == "__main__":
    main()