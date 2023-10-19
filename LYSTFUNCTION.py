from bs4 import BeautifulSoup
import json
import requests
import random
import string
import datetime
import time
from time import sleep
import smtplib
import ssl
import subprocess
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.image import MIMEImage
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys




#####################
def removeMarkup(formatText, formatNumber):
    cleanr = re.compile('<.*?>')
    formattedText = re.sub(cleanr, '', formatText)

    if formatNumber == 'yes':
        formattedText = formattedText[2:]

    return formattedText

###############


def checkPrice(sex, types):
    start_time = time.time()
    # get paramters
    print("<!----Price Check----!>")
    print("")
    searchParameters = getSearchParams('bags', 'Man')
    urlToUse = str(searchParameters[0])
    myPriceLimit_Low = str(searchParameters[1])
    myPriceLimit_High = str(searchParameters[2])
    myGender = sex  # eg "Woman" or "Man"
    myURL = searchParameters
    productSearch = sex + ' ' + types

    if types != "bags" and sex == "Man":
        myURL = urlToUse+"&final_price_from="+myPriceLimit_Low+"&final_price_to="+myPriceLimit_High+"&gender="+myGender+"&view=price_desc&sizes=L&sizes=XL&sizes=XXL"

    print(myURL)
    #fetching HTML source code
    url = getSearchParams2('bags', 'Man') # 'http://' + getContent(getSearchParams2('bags', 'Man'))  #back to normal remove getcontent
    print(url)
    #create path to driver
    s = Service('/usr/biin/chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    
    #function to scroll down
    for i in range(1):
        time.sleep(1)
        print('#########################using beutiful soup###################')
        #checking and printing html
        #response = requests.get(url)
        html = driver.page_source
        #parse the pageload string using BS
        soup = BeautifulSoup(html, 'html.parser') 
        #Defining pContent and assign the calling of findALL()
        pContent = soup.find_all('div', class_='_1wgfN')
        # Extract the text content of the elements in the pContent object
        text = ' '.join([elem.text for elem in pContent])
        # Define the pattern you want to search for
        pattern = r"\d+"
        # Compile the regular expression using the pattern
        regex = re.compile(pattern)
        # Use the findall() method to search for the pattern in the text
        matches = regex.findall(text)
        #print(matches)       #testing
        productNumber = 0
        ignoredForStore = 0
        ignoredForBags = 0
        print("")

        print("<!---- Searching for Products with Gender =  "+str(myGender)+ " | Price Limit: "+str(myPriceLimit_Low)+" | Product Searched: "+str(productSearch)+" ----!>")
        print("")
        for productDetails in pContent:

            print("***** Product Details blerb Starts *****")
            print(productDetails)
            print("***** Product Details blerb Ends *****")
        
        #trying to find a div tag with the class and extract content
            try:
                designer = productDetails.find("div", class_="_2IuM4 _2AZKg").text.strip()
            except:
                designer = 'Not Found'
        #trying to find a div tag with class product-card__short-description-name and extract content
            try:
                desc = productDetails.find("div", class_="_3_ghs").text.strip()
            except:
                desc = 'Not Found'
        #splitting the desc variable into three parts
            first, *middle, last = desc.split()
            color = last
            prodType = types
            prodFrom = "Lyst"
            discount_elem = productDetails.find("span", class_="_2-bIE _2AZKg _1nshI")
            discount = discount_elem #.text
        #producturl = redirected_url #productDetails.find("span", class_="_57YAM")
            storeName_elem = productDetails.find("div", class_="_3PmOF")
            try:
                storeName = storeName_elem.text
            except:
                storeName = 'Not Found'
            getNowPrice_elem = productDetails.find("span", class_="_2-bIE _2AZKg _1nshI")
            getNowPrice = getNowPrice_elem #.text

            if storeName is None:
                store = "Store Unaivalable"

            else:
                store = storeName #.text.strip()
        
        #sorting out correct product link  
            link1 = "https://www.lyst.co.uk" + productDetails.find('a')['href']
            link2 = "https://www.lyst.co.uk/shop/mens-bags/?discount_from=1designer_slug=gucci&designer_slug=balenciaga&designer_slug=valentino&designer_slug=givenchy&designer_slug=dior&designer_slug=valentino&designer_slug=prada&designer_slug=burberry&designer_slug=dolce-gabbana&designer_slug=fendidesigner_slug=hermes&designer_slug=hermes-vintage&designer_slug=saint-laurent%27" + productDetails.find('a')['href']
        
            PD = productDetails.find('a')['href']
            if PD.startswith('#'):
                productLink = link2
            else:
                productLink = link1
        
            redirected_url = productLink
            producturl = redirected_url
            print(producturl)


#########################################
            for i in range(1):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)

# Wait for the images to be loaded
                #wait = WebDriverWait(driver, 10)
                #img_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img._1wgfN")))
               # try:
                   # div = driver.find_element_by_class_name('_1wgfN')
                   # img_tags = div.find_elements_by_tag_name('img')
                  #  for img_tag in img_tags:
                       # imageItem = img_tag.get_attribute("src")
                      #  imageText = img_tag.get_attribute("alt")
                     #   print(f'Image URL: {imageItem}')
                    #    print(f'Image alt text: {imageText}')
                   # if imageItem is None:
                     #   productImage = ""
                    #    productImageText = ""
                   # else:
                  #      productImage = imageItem
                 #       productImageText = imageText

                #except NoSuchElementException:
                   # print('div or img elements not found')



            for searchImage in productDetails.find_all('img'):
                time.sleep(5)
                imageItem = searchImage.get('src')
                imageText = searchImage.get('alt')
                print(f'Image URL: {imageItem}')
                print(f'Image alt text: {imageText}')
                if imageItem is None:
                    productImage = ""
                    productImageText = ""
                else:
                    productImage = imageItem
                    productImageText = imageText

#############################################
            if discount is not None:
                currentPrice = convertIntoMoney(productDetails.find("span", class_='_2-bIE _2AZKg _1nshI').text.strip())
                oldPrice = convertIntoMoney(productDetails.find("del", class_="_2-bIE _2AZKg").text.strip())
                discount = productDetails.find("span", class_="_1c6ZG").text.strip()[1:3]

            else:
                if getNowPrice is None:
                    currentPrice = 0.00
                    oldPrice = 0.00
                    discount = 0
                else:
                    currentPrice = convertIntoMoney(productDetails.find("span", class_="_2-bIE _2AZKg _1nshI").text.strip())
                    oldPrice = 0.00
                    discount = 0

            productNumber = productNumber + 1

            '''
            print("*************** PRODUCT NUMBER: "+str(productNumber)+" ***************")
            print("--- DESIGNER is: "+str(designer))
            print("--- DESCRIPTION is: "+str(desc))
            print("--- CURRENT_PRICE is: "+str(currentPrice))
            print("--- OLD_PRICE is: "+str(oldPrice))
            print("--- DISCOUNT is: "+str(discount))
            print("--- STORE is: "+str(store))
            print("--- PURCHASE_URL is: "+str(redirected_url))
            print("--- IMAGE URL is: "+str(productImage))
            print("--- COLOUR IS : "+str(color))
            '''

            bagFilters = ["CARD", "AIRPOD", "PHONE", "PHONE", "CAMERA", "MINI", "WALLET", "COIN"]
            storeFilters = ["THE LUXURY CLOSET", "VESTIAIRE COLLECTIVE", "LUXURY GARAGE SALE"]

            if getNowPrice is not None:
                if not any(i in store.upper() for i in storeFilters):
                    if types == "bags":
                        if not any(x in desc.upper() for x in bagFilters):
                            sendEmail(designer,desc,currentPrice,oldPrice,discount,store,productImageText, productImage, redirected_url, productDetails,sex,types,searchParameters,producturl)
                        else:
                            ignoredForBags = ignoredForBags + 1
                else:
                    ignoredForStore = ignoredForStore + 1
                # print("IGNORED: store is one of >> THE LUXURY CLOSET,VESTIAIRE COLLECTIVE,LUXURY GARAGE SALE")

        print("Found " + str(productNumber) + " based on search of " + types + " for " + sex)
        print("Total Products ignored cos of bag filter = " + str(ignoredForBags))
        print("Total Products ignored cos of store filter = " + str(ignoredForStore))
        elapsed_time = time.time() - start_time
        print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

#########################)


def getContent(searchURL):
    s = Service('/usr/biin/chromedriver')
    browser = webdriver.Chrome(service=s)
    #browser.get(searchURL)
    print('chromedriver found')

    while True:
        try:
            more_buttons = browser.find_element(By.XPATH,'//a[@class="_1Lqo- _4hZt4 _1bL04 _2_DZ4 _30NYb eybWJ _1i_4K _2dtzM _2W4YF _39ZR5"]')
            #more_buttons.click()
            #browser.execute_script("return arguments[0].scrollIntoView(true);",WebDriverWait(browser, 20).until(EC.visibility_of_element_located((BY.XPATH,'//a[@class="_1Lqo- _4hZt4 _1bL04 _2_DZ4 _30NYb eybWJ _1i_4K _2dtzM _2W4YF _39ZR5"]'))))
            #browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="_1Lqo- _4hZt4 _1bL04 _2_DZ4 _30NYb eybWJ _1i_4K _2dtzM _2W4YF _39ZR5"]'))))
            print('show more button clicked')
        except:
            print('no more show button')
            break
    returnedContent = browser.page_source
    browser.quit()
    return returnedContent

#########################
def getProductURL(fullLink):


    myRedirectedURL = None

    while myRedirectedURL is None:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            s = Service('/usr/biin/chromedriver')
            productURL_Driver = webdriver.Chrome(service=s)
            productURL_Driver.get(fullLink)
            sleep(3)
            myRedirectedURL = productURL_Driver.current_url
            productURL_Driver.quit()

        except:
            pass

    return myRedirectedURL
##########################

def getSearchParams(productItem, sex):
    endURL = ""
    bagBrands = ["designer_slug=gucci", "&designer_slug=balenciaga", "&designer_slug=valentino",
                 "&designer_slug=givenchy", "&designer_slug=dior", "&designer_slug=valentino", "&designer_slug=prada",
                 "&designer_slug=burberry", "&designer_slug=dolce-gabbana", "&designer_slug=fendi",
                 "designer_slug=hermes", "&designer_slug=hermes-vintage", "&designer_slug=saint-laurent"]
    pantsBrands = ["designer_slug=gucci", "&designer_slug=balenciaga", "&designer_slug=valentino",
                   "&designer_slug=givenchy", "&designer_slug=dior", "&designer_slug=valentino", "&designer_slug=prada",
                   "&designer_slug=burberry", "&designer_slug=dolce-gabbana", "&designer_slug=fendi",
                   "&designer_slug=vetements", "&designer_slug=palm-angels", "&designer_slug=off-white-co-virgil-abloh",
                   "&designer_slug=saint-laurent"]
    topsBrands = ["designer_slug=gucci", "&designer_slug=balenciaga", "&designer_slug=valentino",
                  "&designer_slug=givenchy", "&designer_slug=dior", "&designer_slug=valentino", "&designer_slug=prada",
                  "&designer_slug=burberry", "&designer_slug=dolce-gabbana", "&designer_slug=fendi",
                  "&designer_slug=palm-angels", "&designer_slug=off-white-co-virgil-abloh",
                  "&designer_slug=saint-laurent"]
    jacketBrands = ["designer_slug=gucci", "&designer_slug=balenciaga", "&designer_slug=valentino",
                    "&designer_slug=givenchy", "&designer_slug=dior", "&designer_slug=valentino",
                    "&designer_slug=prada", "&designer_slug=burberry", "&designer_slug=dolce-gabbana",
                    "&designer_slug=fendi", "&designer_slug=celine", "&designer_slug=saint-laurent"]

    if sex == "Man":
        topsURL = "https://www.lyst.co.uk/shop/mens-t-shirts/?discount_from=1"
        pantsURL = "https://www.lyst.co.uk/shop/mens-pants/?discount_from=1"
        jacketURL = "https://www.lyst.co.uk/shop/mens-jackets/?discount_from=1"
        bagsURL = "https://www.lyst.co.uk/shop/mens-bags/?discount_from=1"

    else:
        topsURL = "https://www.lyst.co.uk/shop/tops/?discount_from=1"
        pantsURL = "https://www.lyst.co.uk/shop/pants/?discount_from=1"
        jacketURL = "https://www.lyst.co.uk/shop/jackets/?discount_from=1"
        bagsURL = "https://www.lyst.co.uk/shop/bags/?discount_from=1"

    if productItem == "bags":
        for brand in bagBrands:
            bagsURL += brand
        endURL = bagsURL
        myPriceLimit_Low = "300"
        myPriceLimit_High = "600"

    if productItem == "tops":
        for brand in topsBrands:
            topsURL += brand

        endURL = topsURL
        myPriceLimit_Low = "50"
        myPriceLimit_High = "180"

    if productItem == "jackets":
        for brand in jacketBrands:
            jacketURL += brand
        endURL = jacketURL
        myPriceLimit_Low = "80"
        myPriceLimit_High = "200"

    if productItem == "pants":
        for brand in pantsBrands:
            pantsURL += brand
        endURL = pantsURL
        myPriceLimit_Low = "50"
        myPriceLimit_High = "200"

    return endURL, myPriceLimit_Low, myPriceLimit_High

###########################

def convertIntoMoney(money):
    converted_Price = float(money[1:6].replace(",", ""))
    return converted_Price



###########################
def getSearchParams2(productItem, sex):
    endURL = ""
    bagBrands = ["designer_slug=gucci", "&designer_slug=balenciaga", "&designer_slug=valentino",
                 "&designer_slug=givenchy", "&designer_slug=dior", "&designer_slug=valentino", "&designer_slug=prada",
                 "&designer_slug=burberry", "&designer_slug=dolce-gabbana", "&designer_slug=fendi",
                 "designer_slug=hermes", "&designer_slug=hermes-vintage", "&designer_slug=saint-laurent"]
    pantsBrands = ["designer_slug=gucci", "&designer_slug=balenciaga", "&designer_slug=valentino",
                   "&designer_slug=givenchy", "&designer_slug=dior", "&designer_slug=valentino", "&designer_slug=prada",
                   "&designer_slug=burberry", "&designer_slug=dolce-gabbana", "&designer_slug=fendi",
                   "&designer_slug=vetements", "&designer_slug=palm-angels", "&designer_slug=off-white-co-virgil-abloh",
                   "&designer_slug=saint-laurent"]
    topsBrands = ["designer_slug=gucci", "&designer_slug=balenciaga", "&designer_slug=valentino",
                  "&designer_slug=givenchy", "&designer_slug=dior", "&designer_slug=valentino", "&designer_slug=prada",
                  "&designer_slug=burberry", "&designer_slug=dolce-gabbana", "&designer_slug=fendi",
                  "&designer_slug=palm-angels", "&designer_slug=off-white-co-virgil-abloh",
                  "&designer_slug=saint-laurent"]
    jacketBrands = ["designer_slug=gucci", "&designer_slug=balenciaga", "&designer_slug=valentino",
                    "&designer_slug=givenchy", "&designer_slug=dior", "&designer_slug=valentino",
                    "&designer_slug=prada", "&designer_slug=burberry", "&designer_slug=dolce-gabbana",
                    "&designer_slug=fendi", "&designer_slug=celine", "&designer_slug=saint-laurent"]

    if sex == "Man":
        topsURL = "https://www.lyst.co.uk/shop/mens-t-shirts/?discount_from=1"
        pantsURL = "https://www.lyst.co.uk/shop/mens-pants/?discount_from=1"
        jacketURL = "https://www.lyst.co.uk/shop/mens-jackets/?discount_from=1"
        bagsURL = "https://www.lyst.co.uk/shop/mens-bags/?discount_from=1"

    else:
        topsURL = "https://www.lyst.co.uk/shop/tops/?discount_from=1"
        pantsURL = "https://www.lyst.co.uk/shop/pants/?discount_from=1"
        jacketURL = "https://www.lyst.co.uk/shop/jackets/?discount_from=1"
        bagsURL = "https://www.lyst.co.uk/shop/bags/?discount_from=1"

    if productItem == "bags":
        for brand in bagBrands:
            bagsURL += brand
        endURL = bagsURL
        myPriceLimit_Low = "300"
        myPriceLimit_High = "600"

    if productItem == "tops":
        for brand in topsBrands:
            topsURL += brand

        endURL = topsURL
        myPriceLimit_Low = "50"
        myPriceLimit_High = "180"

    if productItem == "jackets":
        for brand in jacketBrands:
            jacketURL += brand
        endURL = jacketURL
        myPriceLimit_Low = "80"
        myPriceLimit_High = "200"

    if productItem == "pants":
        for brand in pantsBrands:
            pantsURL += brand
        endURL = pantsURL
        myPriceLimit_Low = "50"
        myPriceLimit_High = "200"

    return endURL

#####################
def sendEmail(designer, desc, currentPrice, oldPrice, discount, store, productImageText, productImage, redirected_url, productDetails, sex, types, searchParameters,producturl):
    print('###################################')
    print(productImage)
    receiver_email = "sampythontesting@gmail.com"
    SMTP_SERVER = "smtp-mail.outlook.com"
    SMTP_PORT = 587  # For starttls
    sender_email = "sampythontesting@outlook.com"
    if sex == "Man":
        receiver_email = "sampythontesting@gmail.com"
    password = "test1259"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Man Bags Alert: {designer} {desc} selling for {currentPrice}"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    text = f"""\
    Hey there,
    {designer} {desc} is available for {currentPrice}
    go here to purchase:
    {redirected_url}"""
    
    html = f"""\
    <html>
    <body>
    <center>
       <table style="margin: 0 auto; max-width: 500px;">
           <tbody>
               <tr>
                   <td style="font-family: Brown,Helvetica Neue,Helvetica,Arial,sans-serif;font-size:40px; font-weight: 1000"><center><strong>{store}</strong></td>
               </tr>
               <tr>
                   <td style="max-width: 100%;display: block; height: auto; margin: 0 auto; font-size:30px;"colspan="2"><center><a href="{redirected_url}"><img src="{productImage}" height="250" width="200" alt="{productImageText}" ></a></td>
               </tr>
               <tr>
                   <td style="font-family: Brown,Helvetica Neue,Helvetica,Arial,sans-serif;font-size:30px; font-weight: 1000"><center>{designer}</td>
               </tr>
               <tr>
                   <td style="font-family: Brown,Helvetica Neue,Helvetica,Arial,sans-serif;font-size:30px; font-weight: 700"><center><{desc}</a></td>
               </tr>
               <tr>
                   <td style="font-family: Brown,Helvetica Neue,Helvetica,Arial,sans-serif;font-size:30px; font-weight: 700;color: #ed6c50;font-weight: 700;"><center>{currentPrice}</td>
               </tr>
               <tr>
                   <td style="font-family: Brown,Helvetica Neue,Helvetica,Arial,sans-serif;font-size:30px; font-weight: 700;color: #021135;"><s><center>{oldPrice}</s></td>
               </tr>
               <tr>
                   <td style="font-family: Brown,Helvetica Neue,Helvetica,Arial,sans-serif;font-size:30px; font-weight: 700; color: #6d7288;"><center>{discount}% Off</td>
               </tr>
           </tbody>
       </table>
       <br>
       <br>
       <br>
       <p>Url which will take you to Lyst product page = {redirected_url}</p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    try:
        part1 = MIMEText(text, "plain")
    except Exception as e:
        print(f"An exception occurred while creating part1: {e}")
    try:
        part2 = MIMEText(html, "html")
    except Exception as e:
        print(f"An exception occurred while creating part2: {e}")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    
     # Create secure connection with server and send email
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 # disable newer versions of TLS
    context.options |= ssl.OP_NO_COMPRESSION  # disable compression
    context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email Sent")

#############################
checkPrice('Man','bags')
#print(getSearchParams('bags', 'Man'))
print("Code Complete")
