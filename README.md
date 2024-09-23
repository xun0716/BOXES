# BOXES

這個系統是一個基於 Flask 框架的股票爬蟲和數據查詢系統，用戶可以通過簡單的網頁介面進行股票相關的查詢與分析。

## 系統功能：

1. **查詢股價**
   - 使用者可以通過輸入股票代號，查詢該股票的最新日線資料。資料包括日期、開盤價、收盤價、成交量等基本交易數據。

2. **查詢股票新聞**
   - 輸入股票代號後，系統會自動爬取相關的新聞資訊，並展示新聞標題、來源和新聞內容。

3. **查詢 FinMind 資料**
   - 使用者可以通過輸入股票代號及日期範圍，查詢由 FinMind 提供的機構投資人買賣超資料。這些數據顯示了機構投資人對特定股票的操作趨勢，對於投資決策非常有幫助。

## 技術堆疊：

1. **後端框架：Flask**
   - Flask 是一個輕量級的 Python Web 框架，適合快速構建網頁應用。該系統利用 Flask 處理用戶請求和數據展示。

2. **網頁爬蟲：Selenium + BeautifulSoup**
   - Selenium 用於模擬使用者行為，訪問動態加載的新聞頁面並滾動以加載更多內容。
   - BeautifulSoup 用於解析網頁並提取新聞的詳細內容。

3. **數據處理：Pandas**
   - Pandas 用於將 API 返回的數據格式化為 DataFrame，並進行資料處理後返回給前端。

4. **前端：HTML + JavaScript**
   - 使用簡單的 HTML 和 JavaScript 來實現網頁介面，提供交互功能，讓使用者可以提交查詢請求並查看結果。

5. **瀏覽器驅動：ChromeDriver**
   - 使用 ChromeDriver 與 Selenium 搭配，實現自動化的瀏覽器操作。

6. **API 請求管理：Requests**
   - Requests 模組用於與第三方 API 通訊和進行網絡請求，獲取數據並進行處理。

## API：

1. **台灣證券交易所 (TWSE) API**
   - 用於查詢特定股票的日線交易資料。透過請求 [TWSE API](https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY) 獲取指定股票在某日期的交易數據。

2. **FinMind API**
   - 提供多種類型的金融數據。系統使用該 API 獲取機構投資人對特定股票的買賣超資訊。API 請求範例：
     ```plaintext
     https://api.finmindtrade.com/api/v4/data
     ```
     包含 `dataset`, `data_id`, `start_date`, `end_date` 等參數來篩選特定股票的資料。

3. **新聞查詢 (Anue 鉅亨)**
   - 使用爬蟲爬取新聞資料。系統透過 Selenium 自動化操作，訪問像是 Anue 鉅亨新聞等網站的搜索結果頁面，並進行資料擷取。

## 總結：

這個系統為用戶提供了一個方便的工具，用來查詢台灣股票的基本交易資料、新聞動態以及機構投資人的交易行為。後端運用 Flask 與多種技術工具，確保能夠有效地處理大規模的數據請求和網頁爬取。這些功能對於投資者和研究者來說，可以作為有力的輔助決策工具。


取得新聞資訊：

![image](https://github.com/user-attachments/assets/3ee4cfd9-5c55-4296-90e2-0298a7c6e12b)
![image](https://github.com/user-attachments/assets/d26b266b-06f1-412b-bd02-d58f1076d34f)

查詢股價:

![image](https://github.com/user-attachments/assets/aea41864-d5d0-4999-b116-21e2bf069bcc)
![image](https://github.com/user-attachments/assets/3a941a52-2bc6-4082-90a6-55dfbc2ac930)


