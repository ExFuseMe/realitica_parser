from datetime import *
from bs4 import BeautifulSoup
import requests, json, re, threading, os
from PIL import Image
page = 0
image_elements = []


region = {}
def parse(url, state, region):

    if url != '' and requests.get(f"https://www.realitica.com/{url}").status_code == 200:
        
        children_soup = BeautifulSoup(requests.get(url).text, 'lxml')
        div = children_soup.find(id='listing_body').get_text()
        text = re.sub(r"\[.*?\]+", '', div)
        text = text.replace('\n', '').replace('\t', '')

        name=str(url.split('/')[-1])

        region[state].update({name:text})


        page_images = children_soup.find_all('img', attrs={'style':"margin-bottom:15px;"})

        for el in page_images:
            image_elements.append(el)


# call all states from website
states = ['Macedonia','Hrvatska', 'Crna+Gora', 'Bosna+i+Hercegovina', 'Deutschland', 'Srbija']


def main_function(i):
    global region



    # run all states from array
    for state in states:
        # append this state to json object
        region.update({state:{}})
        for page in range(i-50, i):


            # check because another url for Germany
            if state != 'Deutschland':
                url = f"https://www.realitica.com/?cur_page={page}&for=Prodaja&pState={state}&lng=eng"
            else:
                url = f"https://www.realitica.com/?cur_page={page}&for=Prodaja&pCountry=Deutschland&lng=deg"

            if requests.get(url).status_code == 200:

                soup = BeautifulSoup(requests.get(url).text, 'lxml')

                if 'Listing Not Found' not in soup.text:

                    # find a special element(<div></div>) which is in all posts
                    a = soup.div
                    parent_a = a.parent
                    data = parent_a.find_all_next('div', attrs={'style':'width:100%;'})

                    # create an array and fill it with links to posts pages
                    urls = ['']*20


                    for i in range(len(data)):
                        urls[i] = data[i].find_parent('div').a['href']
                    
                    # start parse all appartments in the page
                    threading.Thread(target=parse, args=(urls[0],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[1],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[2],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[3],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[4],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[5],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[6],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[7],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[8],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[9],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[10],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[11],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[12],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[13],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[14],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[15],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[16],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[17],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[18],state, region,)).start()
                    threading.Thread(target=parse, args=(urls[19],state, region,)).start()
                            
                else:
                    break

a = threading.Thread(target=main_function, args=(50,))
b = threading.Thread(target=main_function, args=(101,))
a.start()
b.start()
a.join()
b.join()
abs_path = os.path.dirname(__file__)
realitica_path = "realitica"
with open(f"{abs_path}\\{realitica_path}\\realitica.json", 'w', encoding='utf8') as f:
    json.dump(region, f, indent=4, ensure_ascii=False)

for el in image_elements:
    # for development
    folder = el.get('alt').split('.')[0]
    xpath = f"{abs_path}\\{realitica_path}\\{folder}\\{el.get('alt').split('.')[0]}"
    # with open(el.get('alt'), 'wb') as f:
    #     f.write(requests.get(el.get('src')).content)
    # image = Image.open(el.get('alt')).convert('RGB')
    # image.save(f"{os.getcwd()}/realitica/images/{el.get('alt').split('.')[0]}.webp")
    # os.remove(el.get('alt'))


    # for checking downloading(locally)
    print(el.get('alt').split('.')[0], requests.get(f"https://www.realitica.com/{el.get('src')}"))

