from bloomfilter.bloomfilter import BloomFilter


print("1")
bfilter = BloomFilter()
bfilter.add("213123213")


print("213123213: ", bfilter.get("213123213"))
print("53123213: ", bfilter.get("553123213"))
