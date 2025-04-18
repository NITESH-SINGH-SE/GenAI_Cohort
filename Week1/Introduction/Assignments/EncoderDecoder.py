class Tonkenizer:
    def encode(self, input):
        vector = []
        for ch in input:
            vector.append(ord(ch))
        return vector


    def decode(self, vector):
        res = ""
        for num in vector:
            res += chr(num)
        return res
    
tokenizer = Tonkenizer()
encodedData = tokenizer.encode("Hello, World!")
print(encodedData)
decodedData = tokenizer.decode(encodedData)
print(decodedData)