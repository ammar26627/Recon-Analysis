import argparse
from tools import Tools

class ReconAnalysis(Tools):
    def __init__(self, url) -> None:
            super().__init__(url)

    def ssl(self) -> dict:
        return dict(self.getSslOutput())
    
    def fuzz(self, wordlist_path:str) -> dict:
        return dict(self.getFuzzingOutput(wordlist_path))
    
    def subdomains(self) -> dict:
        return dict(self.getSubdomains())

    @classmethod
    def print(cls, dictionary):
        if dictionary:
            for url, value in dictionary.items():
                print(f"Domain name: {url}")
                print("Analysis:")
                for item in value:
                    print(item)
        else:
            print("No vulnerability found")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=
            "Recon Analysis of a given domain. Includes SSL analysis and Fuzzing analysis")

    parser.add_argument('domain', type=str, help="Input domain name") #Domain Name
    parser.add_argument('-s', '--ssl', action='store_true', help="SSL analysis") #SSL Analysis
    parser.add_argument('-f', '--fuzz', type=str, help="Fuzzing analysis: Provide wordlist path") #Fuzzing Analysis
    args = parser.parse_args()

    analysis = ReconAnalysis(args.domain)

    print("Subdomains:\n")
    subdomains = analysis.getSubdomains()
    if subdomains:
        analysis.print(subdomains)
        print("\n")
    else:
        print("No subdomains found")
    if args.ssl:
        print("SSL:\n")
        analysis.print(analysis.ssl())
        print("\n")
    if args.fuzz:
        print("Fuzzing:\n")
        analysis.print(analysis.fuzz(args.fuzz))