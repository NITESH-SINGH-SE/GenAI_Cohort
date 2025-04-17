class Transformer:
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
    
transformer = Transformer()
encodedData = transformer.encode("Hello, World!")
print(encodedData)
decodedData = transformer.decode(encodedData)
print(decodedData)