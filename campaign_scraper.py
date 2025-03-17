import requests
import pandas as pd
import json
import time

df = pd.read_excel("campaignsummary250226.xlsx", skiprows = 4)
df = df[df['Status'] == 'running']

with open('campaign_ids.json', 'r') as f:
    campaign_ids = json.load(f)

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

def extract_product(product_dict: dict):
    if product_dict:
        ad_id = product_dict.get('id')
        metrics = product_dict.get('metrics')

        if metrics:
            spend = metrics.get('adSpend')
            ctr = metrics.get('ctr')
            impressions = metrics.get('impressions')
            roas = metrics.get('roas')
            brandHaloRoas = metrics.get('brandHaloRoas')
    
        sku = product_dict.get('sku')
        product_name = product_dict.get('creative').get('name')
        price = product_dict.get('creative').get('price')

    data_dict = {
        'ad_id': ad_id if ad_id else None,
        'spend': spend if spend else None,
        'ctr': ctr if ctr else None,
        'impressions': impressions if impressions else None,
        'roas': roas if roas else None,
        'brandHaloRoas': brandHaloRoas if brandHaloRoas else None,
        'sku': sku if sku else None,
        'product_name': product_name if product_name else None,
        'price': price if price else None
    }

    return data_dict

# 你的原始 headers 和 url
base_url = "https://us.orangeapronmedia.com/api/v2/store/33602/campaigns/{}/targeting/?page=1&page_size=10"
base_referer = "https://us.orangeapronmedia.com/r/33602/campaign/details/{}"

# 读取唯一 Campaign ID

# 存储所有请求结果
responses = {}
product_results = []
for campaign_id in campaign_ids:
    # 动态修改 URL 和 Referer
    url = base_url.format(campaign_id)
    headers["Referer"] = base_referer.format(campaign_id)

    # 发送 GET 请求
    response = requests.get(url, headers=headers)

    # 存储响应内容
    responses[campaign_id] = response.json().get('results') # 或 response.text

    for i in range(len(response.json().get('results'))):

        product_dict = extract_product(response.json().get('results')[i])

        product_dict['campaign_id'] = campaign_id

        product_results.append(product_dict)
    
    print(f"Fetched data for Campaign ID: {campaign_id}, Status Code: {response.status_code}")

    time.sleep(5)

# responses 字典存储了所有 Campaign ID 的 API 响应

df_results = pd.DataFrame(product_results)