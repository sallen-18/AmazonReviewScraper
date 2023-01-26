# Tutorial followed by John Watson Rooney https://www.youtube.com/watch?v=UD4VzOfhBCQ

from requests_html import HTMLSession
import json
import asyncio
from itertools import chain

class Reviews:
    def __init__(self,asin) -> None:
        self.asin = asin
        self.session = HTMLSession()
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        self.url = f"https://www.amazon.co.uk/product-reviews/{self.asin}/ref=cm_cr_othr_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="

    def pagination(self, pageNumber):
        r = self.session.get(self.url + str(pageNumber))
        r.html.render(sleep=1)
        if not r.html.find("div[data-hook=review]"):
            return False
        else:
            print(f"Found reviews page {pageNumber}")
            return r.html.find("div[data-hook=review]")


    def parse(self, reviews):
        total=[]
        for review in reviews:
            if review.find("a[data-hook=review-title]"):
                title = review.find("a[data-hook=review-title]", first=True).text

                rating = review.find("i[data-hook=review-star-rating] span", first=True).text

                if review.find("span[data-hook=review-body] span"):
                    body = review.find("span[data-hook=review-body] span", first=True).text.replace('\n','').strip()

                data = {
                    'title': title,
                    'rating': rating,
                    'body': body
                }

                total.append(data)

            else:
                print("Error occured")
        
        return total

    def save(self, results):
        with open(self.asin +'-reviews.json', 'w') as f:
            json.dump(results, f)




if __name__ == "__main__":
    amz = Reviews("B00NBR70DO")
    results = []
    for i in range(1, 10):
        review = amz.pagination(i)
        if review:
            results.append(amz.parse(review))

    amz.save(list(chain.from_iterable(results)))