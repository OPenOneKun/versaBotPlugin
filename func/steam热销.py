import requests
from datetime import datetime

def get_steam_top_sellers():
    # Steam Store API 热销商品接口
    api_url = "https://store.steampowered.com/api/featuredcategories"
    params = {
        "l": "schinese",  # 中文结果
        "cc": "CN"        # 中国区
    }

    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            top_sellers = data.get("top_sellers", {}).get("items", [])
            
            # 获取前10个游戏的详细信息
            games_info = []
            for game in top_sellers[:10]:
                app_id = game["id"]
                detail_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=CN&l=schinese"
                detail_response = requests.get(detail_url)
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    if detail_data[str(app_id)]["success"]:
                        game_data = detail_data[str(app_id)]["data"]
                        
                        # 处理价格信息
                        price_info = game_data.get("price_overview", {})
                        if price_info:
                            original_price = price_info.get("initial_formatted", "")
                            final_price = price_info.get("final_formatted", "")
                            discount = price_info.get("discount_percent", 0)
                        else:
                            original_price = "免费游戏"
                            final_price = "免费"
                            discount = 0

                        # 整理游戏信息
                        game_info = {
                            "name": game_data.get("name", "未知"),
                            "original_price": original_price,
                            "final_price": final_price,
                            "discount": discount,
                            "header_image": game_data.get("header_image", ""),
                            "release_date": game_data.get("release_date", {}).get("date", "发布日期未知"),
                            "developers": ", ".join(game_data.get("developers", ["开发商未知"])),
                            "description": game_data.get("short_description", "暂无描述")
                        }
                        games_info.append(game_info)
            
            return games_info
        else:
            print(f"获取热销榜信息失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def format_top_sellers(games_info):
    if not games_info:
        return "无法获取热销榜信息"

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    markdown = f"# Steam 热销榜 Top 10\n\n更新时间: {current_time}\n\n"

    for index, game in enumerate(games_info, 1):
        discount_info = f"~~{game['original_price']}~~ **{game['final_price']}** (-{game['discount']}%)" if game['discount'] > 0 else game['final_price']
        
        markdown += f"""
## {index}. {game['name']}

![{game['name']}]({game['header_image']})

- 价格: {discount_info}
- 发布日期: {game['release_date']}
- 开发商: {game['developers']}

{game['description']}

---"""

    return markdown

def main():
    print("正在获取Steam热销榜信息...")
    games_info = get_steam_top_sellers()
    print(format_top_sellers(games_info))

if __name__ == "__main__":
    main()