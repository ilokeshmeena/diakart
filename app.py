from flask import Flask,jsonify
from flask import Flask
from bs4 import BeautifulSoup
import requests
from flask import request

app=Flask(__name__)

@app.route('/ketofy')
def ketofy():
    link = request.args.get('link', default = 'https://www.ketofy.in/product/buy-dark-keto-chocolate/', type = str)
    req =requests.get(link)
    content=req.content
    soup=BeautifulSoup(content,'lxml' )
    productDetails=[]
    varientDetails=[]
    descriptionList=[]
    productImages=[]

    productName=soup.find('h1',class_="product_title entry-title").text

    allDescription=soup.find("div", {"id": "tab-description"}).findAll('p')
    if len(allDescription)!=0:
        for descriptions in allDescription:
            descriptionList.append(descriptions.text)
    else:
        allDescription=soup.find("div",class_='electro-description clearfix').findAll('li')
        for descriptions in allDescription:
            descriptionList.append(descriptions.text)

    images=soup.find_all('figure',class_='electro-wc-product-gallery__image')
    if len(images)!=0:
        for image in images:
            productImages.append(image.a['href'])
    else:
        images=soup.find_all('div',class_='woocommerce-product-gallery__image')
        for image in images:
            productImages.append(image.a['href'])

    varientInGramList=[]
    varientPricesList=[]
    noOfVarients=0
    varientNames=soup.find_all('div',class_='woovr-variation-name')
    for varientName in varientNames:
        a=varientName.text
        splited=a.split()
        for s in splited:
            if s.__contains__('0g'):  
                noOfVarients +=1
                varientInGramList.append(s.rsplit('g')[0]+'g')

    varientPrices=soup.find_all('div',class_='highlight')
    for i in range(noOfVarients*2):
        if i%2==0: 
            price=varientPrices[i].span.text   
            varientPricesList.append(price.rsplit('₹')[1])

    for i in range(noOfVarients):
        varientDetails.append({
            'varientName':varientInGramList[i],
            'varientPrice':varientPricesList[i]
        })

    productDetails.append({
        'name': productName,
        'description' : descriptionList,
        'images' : productImages,
        'details' : varientDetails
    })
    return jsonify(productDetails)

if __name__=='__main__':
    app.run(debug=True)