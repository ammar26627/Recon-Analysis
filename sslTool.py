import subprocess, re
from collections import defaultdict
from subdomains import Subdomains


class Ssl(Subdomains):
    def __init__(self, url) -> None:
        self.url = url
        super().__init__(url)
        self.ssl_output = defaultdict(list)

    def sslSubdomain(self):
        self.subdomains[self.url] = []
        for subdomain in self.subdomains:
            pattern = r'^(?:https?://)?([^/]+)'
            match = re.match(pattern, subdomain)
            if match:
                url = match.group(1)
            else:
                raise ValueError("Invalid url")
            result = subprocess.run(["python3", "-m", "sslyze", url], capture_output=True, text=True, shell=False)
            self.checkForVuln(result.stdout, subdomain)
        self.subdomains.pop(self.url)

    def checkForVuln(self, result, subdomain):
        for line in result.split("\n"):
            for j in range(len(line[:-9])):
                if line[j+4:j+12].lower() == 'vulnerab' and line[j:j+3].lower() == 'not':
                    self.ssl_output[subdomain].append(line)               



if __name__ == '__main__':
    ssl = Ssl("leetcode.com")