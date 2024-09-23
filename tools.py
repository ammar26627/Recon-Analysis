from sslTool import Ssl
from fuzzTool import Fuzz

class Tools(Ssl, Fuzz):
    def __init__(self, url) -> None:
        super().__init__(url)

    def getSubdomains(self) -> dict:
        return self.subdomains

    def getSslOutput(self) -> dict:
        self.sslSubdomain()
        return self.ssl_output
    
    def getFuzzingOutput(self, wordlist_path:str) -> dict:
        self.fuzzSubdomain(wordlist_path)
        return self.fuzz_output