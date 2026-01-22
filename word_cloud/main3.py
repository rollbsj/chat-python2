from textblob import TextBlob

text = """
문제는 이 상품이 같은 해 상반기에 출시한 ‘블랙 야자수 후드 티셔츠’(정가 50만원 대) 상품을 재가공한 뒤 소비자에게 별도의 고지를 하지 않은 채 판매했다는 점이다.
"""

blob = TextBlob(text)
sentiment = blob.sentiment

print(f"극성(polarity): {sentiment.polarity}") #-1(부정)~1(긍정)
print(f"주관성(Subjectivity):{sentiment.subjectivity}")