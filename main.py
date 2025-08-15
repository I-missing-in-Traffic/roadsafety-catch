import requests
import urllib3

# env
year = 114
countryCode = 0
keyword = "闖紅燈"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

vehicle_types = {
    0: "機車",
    1: "小型車",
    2: "行人",
    3: "大型車",
    4: "自行車",
    5: "其他"
}

url = "https://roadsafety.tw/api/AccAgeI26CauseOrderAjax/GetResult"

table = []
grand_total_cases = 0
grand_total_hurt = 0
grand_total_death = 0

for v_type, v_name in vehicle_types.items():
    params = {
        "Cyear": year,
        "CityKeyid": countryCode,
        "AreaKeyid": 0,
        "OrderType": 1,
        "Age": 0,
        "I26type": v_type
    }
    try:
        resp = requests.get(url, params=params, verify=False, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"⚠ 無法抓取 {v_name} 資料: {e}")
        continue

    filtered = [item for item in data if keyword in item["name"]]
    total_cases = sum(item["caseQty"] for item in filtered)
    total_hurt = sum(item["hurtQty"] for item in filtered)
    total_death = sum(item["deathQty"] for item in filtered)

    table.append((v_name, total_cases, total_hurt, total_death))

    grand_total_cases += total_cases
    grand_total_hurt += total_hurt
    grand_total_death += total_death

name_width = max(len("全車種總計"), max(len(row[0]) for row in table)) + 2
num_width = 8

print(f"年度: {year}，關鍵字: {keyword}, CountryCode: {countryCode}")
header = f"{'車種':<{name_width}}{'案件數':>{num_width}}{'受傷':>{num_width}}{'死亡':>{num_width}}"
print(header)
print("-" * (name_width + num_width * 3))
for row in table:
    print(f"{row[0]:<{name_width}}{row[1]:>{num_width}}{row[2]:>{num_width}}{row[3]:>{num_width}}")
print("-" * (name_width + num_width * 3))
print(f"{'全車種總計':<{name_width}}{grand_total_cases:>{num_width}}{grand_total_hurt:>{num_width}}{grand_total_death:>{num_width}}")

