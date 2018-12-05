from bloomfilter.bloomfilter import BloomFilter


print("1")
bfilter = BloomFilter()
bfilter.add("213123213")


print(bfilter.get("213123213"))