from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import datetime as dt
import certifi
import requests

app = Flask(__name__)



# 根據路由處理請求
@app.route('/')
def index():
    return render_template('index.html')

# 查詢股價
@app.route('/stock', methods=['POST'])
def stock_data():
    stock_id = request.form.get('stock_id', '')
    date = dt.date.today().strftime("%Y%m%d")
    stock_data = requests.get(f'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={date}&stockNo={stock_id}')
    
    try:
        json_data = stock_data.json()
    except ValueError:
        return jsonify({'error': '無效的 JSON 回應，可能 API 請求失敗'})

    if 'data' not in json_data:
        return jsonify({'error': '無法獲取資料'})

    df = pd.DataFrame(data=json_data['data'], columns=json_data['fields'])
    return jsonify(df.to_dict(orient='records'))

# 查詢 FinMind 資料
@app.route('/finmind_data', methods=['POST'])
def get_finmind_data():
    stock_id = request.form.get('stock_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
        "data_id": stock_id,
        "start_date": start_date,
        "end_date": end_date,
        "token": "your_token_here"
    }

    response = requests.get(url, params=parameter)
    
    try:
        data = response.json()
    except ValueError:
        return jsonify({'error': '無效的 JSON 回應，可能 API 請求失敗'})

    if 'data' not in data:
        return jsonify({'error': '無法獲取資料'})

    df = pd.DataFrame(data['data'])
    return jsonify(df.to_dict(orient='records'))

# 查詢股票新聞
@app.route('/news', methods=['POST'])
def get_news():
    stock_id = request.form.get('stock_id')

    # 設定 ChromeOptions
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # 初始化 Selenium driver
    driver = webdriver.Chrome(options=chrome_options)
    data2 = []  # 表格數據
    url = f"https://www.cnyes.com/search/news?keyword={stock_id}"
    driver.get(url)

    # 模擬滑動滑鼠滾輪的行為，用於加載更多內容
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 擷取新聞網址和標題
    elements = driver.find_elements(By.XPATH, '//*[@id="_SearchAll"]/section/div/a')
    for element in elements:
        link = element.get_attribute("href")
        title = element.text
        title = title.split('\n')
        data2.append([stock_id, title[1] if len(title) > 1 else '', title[0], link])

    driver.quit()

    # 擷取每個新聞的具體內容
    for news in data2:
        link_url = news[3]
        try:
            news_content = requests.get(link_url, verify=False).content
            soup = BeautifulSoup(news_content, 'html.parser')
            article = soup.find('article')
            news[3] = article.get_text() if article else '無內容'
        except Exception as e:
            news[3] = f'無法獲取內容，錯誤: {e}'

    # 創建 DataFrame
    columns = ['股票代號', '新聞標題', '來源', '內容']
    df = pd.DataFrame(data2, columns=columns)
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
