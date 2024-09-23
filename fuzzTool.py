import subprocess, re
from collections import defaultdict
from subdomains import Subdomains

class Fuzz(Subdomains):
    def __init__(self, url) -> None:
        super().__init__(url)
        self.fuzz_output = defaultdict(list)
        
    def fuzzSubdomain(self, wordlist):
        word_set = set()
        for subdomain in self.subdomains:
            fuzzer = subdomain + "/FUZZ"
            # result = subprocess.run(["ffuf", "-w", wordlist, "-u", fuzzer, "-mc", "all", "-fc", "403"],
            #                         shell=False, text=True, capture_output=True)
            result = subprocess.run(["ffuf", "-w", wordlist, "-u", fuzzer],
                                    shell=False, text=True, capture_output=True)
            self.checkFuzz(result.stdout, word_set, subdomain)
        
    def checkFuzz(self, result, word_set, subdomain):
        for line in result.split("/n"):
                words_pattern = re.search(r'Words:\s*(\d+)', line)
                if words_pattern:
                    words = words_pattern.group(1)
                else:
                    continue
                if words not in word_set:
                    word_set.add(words)
                    self.fuzz_output[subdomain[0]].append(line)


if __name__ == '__main__':
    ssl = Fuzz("leetcode.com")
