HD_metrics = ['Click Through Rate (CTR) (sum)', 'Clicks (sum)', 'Cost Per Click (CPC) (sum)',
              'Cost Per Thousand Views (CPM) (sum)', 'Impressions (sum)', 'MTA In-Store Sales (sum)',
              'MTA Online Sales (sum)', 'MTA Sales (sum)', 'Return on Ad Spend (ROAS) SPA (sum)', 'Return on Ad Spend (ROAS) MTA (sum)',
              'SPA In-Store Sales (sum)', 'SPA Online Sales (sum)', 'SPA Sales (sum)', 'Spend (sum)']

# 单位映射配置
UNITS_MAPPING = {
'Click Through Rate (CTR) (sum)': 'Percentage (%)', 
'Clicks (sum)': "Count", 
'Cost Per Click (CPC) (sum)': 'USD',
'Cost Per Thousand Views (CPM) (sum)': 'USD', 
'Impressions (sum)': 'Count', 
'MTA In-Store Sales (sum)': 'USD',
'MTA Online Sales (sum)': 'USD', 
'MTA Sales (sum)': 'USD', 
'Return on Ad Spend (ROAS) SPA (sum)': '', 
'Return on Ad Spend (ROAS) MTA (sum)': '',
'SPA In-Store Sales (sum)': 'USD', 
'SPA Online Sales (sum)': 'USD', 
'SPA Sales (sum)': 'USD', 
'Spend (sum)': 'USD'
}

headers = {
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "en-US,en;q=0.9",
  "Cache-Control": "no-cache",
  "Connection": "keep-alive",
  "Content-Type": "application/json",
  "Cookie": "sessionid=c66plnv5bv1tbvetks3vtd01iz1487jh; gatewayaffinityCORS=4f76a65c88456540cc49f9db66b243ad; gatewayaffinity=4f76a65c88456540cc49f9db66b243ad; csrftoken=CbYzx62XDN9rSVIxQIf9EVl170jOzxHzcYqdir40QTWUX0DOgzqaRmkaW0ebZPxs; _dd_s=logs=1&id=59b12daf-1fe1-4d41-a6cf-c37b0265aa1e&created=1740510905067&expire=1740514392891",
  "Host": "us.orangeapronmedia.com",
  "Pragma": "no-cache",
  "Referer": "https://us.orangeapronmedia.com/r/33602/campaign/details/45866",
  "Sec-Ch-Ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": "\"Windows\"",
  "Sec-Fetch-Dest": "empty",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Site": "same-origin",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
  "X-Csrftoken": "EeZdv9s3SelCZwXvg65s0VRzZXCZ4PZUCrcnUEM3Sd3bp8ZPWqULUb8mR1NIelL4"
}
