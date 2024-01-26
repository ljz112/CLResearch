from pyurbandict import UrbanDict

# pros: very high depth
# cons: low accuracy to what you want 

word = UrbanDict("frapper")
results = word.search()
print(results[1:5])