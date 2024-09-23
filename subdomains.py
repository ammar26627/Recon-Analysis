import subprocess, re

class Subdomains():
    def __init__(self, url) -> None:
        self.unfiltured_subdomains = []
        self.subdomains = {}
        self.url = url
        self.subdomainsList()
        self.subdomainsDetails()
    
    def subdomainsList(self):
        subprocess.run(["python3", "../FinalRecon/finalrecon.py", "--sub", "--url", self.url, "-cd", './assets/', "-of", "subdomains"],
                       capture_output=True, text=True)
        with open("subdomains/subdomains.txt", 'r') as txt:
            subd = txt.readlines()
            self.unfiltured_subdomains = subd
            


    def subdomainsDetails(self):
        subdomains_jsonl = subprocess.run(["httpx", "--sc", "--cl", "-fep", "-list", "./assets/subdomains/subdomains.txt", "j"],
    capture_output=True, text=True)
        content_length = set()
        for item in subdomains_jsonl.stdout.split("\n"):
            cleaned_output = re.sub(r'\x1b\[[0-9;]*m', '', item)
            match = re.match(r'(https?://[^\s]+)\s*\[(\d+)\]\s*\[(\d+)\]', cleaned_output)

            if match:
                url = match.group(1)
                status_code = match.group(2)
                content = match.group(3)
            if int(status_code) < 400 and content not in content_length:
                content_length.add(content)
                self.subdomains[url] = [status_code, content]


if __name__ == "__main__":
    subd = Subdomains("www.leetcode.com")        