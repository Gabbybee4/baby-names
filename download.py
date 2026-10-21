import io
import re
import urllib.request
import zipfile

URL = "https://www.ssa.gov/oact/babynames/names.zip"
OUTPUT_CSV = "ssa-baby-names.csv"

# Browser-like headers so the SSA server allows the download
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}


def main():
    req = urllib.request.Request(URL, headers=HEADERS)
    with urllib.request.urlopen(req) as response:
        zip_bytes = response.read()

    # Open the zip archive in memory and combine all yobYYYY.txt files
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf, open(
        OUTPUT_CSV, "w", encoding="utf-8", newline="\n"
    ) as out_file:
        out_file.write("year,name,sex,count\n")

        for filename in sorted(zf.namelist()):
            match = re.fullmatch(r"yob(\d{4})\.txt", filename)
            if not match:
                continue
            year = match.group(1)

            with zf.open(filename) as f:
                for raw_line in f:
                    line = raw_line.decode("utf-8").strip()
                    if line:
                        out_file.write(f"{year},{line}\n")

    print(f"Saved {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
