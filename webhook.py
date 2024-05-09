import main
import requests
import user
import json


def topLogin(data: list) -> None:
    endpoint = main.webhook_discord_url

    rewards: user.Rewards = data[0]
    login: user.Login = data[1]
    bonus: user.Bonus or str = data[2]
    
    with open('login.json', 'r', encoding='utf-8')as f:
        data22 = json.load(f)

        name1 = data22['cache']['replaced']['userGame'][0]['name']
        fpids1 = data22['cache']['replaced']['userGame'][0]['friendCode']

    messageBonus = ''
    nl = '\n'

    if bonus != "No Bonus":
        messageBonus += f"__{bonus.message}__{nl}```{nl.join(bonus.items)}```"

        if bonus.bonus_name != None:
            messageBonus += f"{nl}__{bonus.bonus_name}__{nl}{bonus.bonus_detail}{nl}```{nl.join(bonus.bonus_camp_items)}```"

        messageBonus += "\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO Daily Bouns - " + main.fate_region,
                "description": f"تم تسجيل الدخول بنجاح، معلومات الحساب ادناه:\n\n{messageBonus}",
                "color": 563455,
                "fields": [
                    {
                        "name": "الاسم",
                        "value": f"{name1}",
                        "inline": True
                    },
                    {
                        "name": "معرف الـ ID",
                        "value": f"{fpids1}",
                        "inline": True
                    },
                    {
                        "name": "المستوى",
                        "value": f"{rewards.level}",
                        "inline": True
                    },
                    {
                        "name": "عدد القسائم (تكت)", 
                        "value": f"{rewards.ticket}",
                        "inline": True
                    },                    
                    {
                        "name": "كوارتز SQ",
                        "value": f"{rewards.stone}",
                        "inline": True
                    },
                    {
                        "name": "Saint Quartz Fragment",
                        "value": f"{rewards.sqf01}",
                        "inline": True
                    },
                    {
                        "name": "تفاح ذهبي",
                        "value": f"{rewards.goldenfruit}",
                        "inline": True
                    },
                    {
                        "name": "تفاح فضي",
                        "value": f"{rewards.silverfruit}",
                        "inline": True
                    },
                    {
                        "name": "تفاح برونزي",
                        "value": f"{rewards.bronzefruit}",
                        "inline": True
                    },
                    {
                        "name": "تفاح ازرق",
                        "value": f"{rewards.bluebronzefruit}",
                        "inline": True
                    },
                    {
                        "name": "شتلة برونزية مطلوبة في انتاج التفاح الازرق",
                        "value": f"{rewards.bluebronzesapling}",
                        "inline": True
                    },
                    {
                        "name": "عدد أيام تسجيل الخول المتتالية",
                        "value": f"{login.login_days}",
                        "inline": True
                    },
                    {
                        "name": "العدد الكلي لأيام تسجيل الدخول",
                        "value": f"{login.total_days}",
                        "inline": True
                    },
                    {
                        "name": "مربع أبيض",
                        "value": f"{rewards.pureprism}",
                        "inline": True
                    },
                    {
                        "name": "نقاط الأصدقاء",
                        "value": f"{login.total_fp}",
                        "inline": True
                    },
                    {
                        "name": "نقاط الأصدقاء المكتسبة اليوم",
                        "value": f"+{login.add_fp}",
                        "inline": True
                    },
                    {
                        "name": "الحد الأقصى الحالي من AP",
                        "value": f"{login.act_max}",
                        "inline": True
                    },
                    {
                        "name": "عدد الكؤوس المقدسة",
                        "value": f"{rewards.holygrail}",
                        "inline": True
                    },
                    
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara01.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


def shop(item: str, quantity: str) -> None:
    endpoint = main.webhook_discord_url
    
    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO نظام التسوق التلقائي - " + main.fate_region,
                "description": f"تمت عملية شراء تفاح ازرق بنجاح",
                "color": 5814783,
                "fields": [
                    {
                        "name": f"المتجر",
                        "value": f"المستهلك {40 * quantity}Ap مقابل الحصول على : {quantity}x {item}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo2/images/commnet_chara10.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


def drawFP(servants, missions) -> None:
    endpoint = main.webhook_discord_url

    message_mission = ""
    message_servant = ""
    
    if (len(servants) > 0):
        servants_atlas = requests.get(
            f"https://api.atlasacademy.io/export/JP/basic_svt.json").json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            svt = svt_dict[servant.objectId]
            message_servant += f"`{svt['name']}` "

    if(len(missions) > 0):
        for mission in missions:
            message_mission += f"__{mission.message}__\n{mission.progressTo}/{mission.condition}\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO بنر الاصدقاء المجاني - " + main.fate_region,
                "description": f"تمت بناجح وهذه هي النتائج.\n\n{message_mission}",
                "color": 5750876,
                "fields": [
                    {
                        "name": "البطاقات المُكتسبة",
                        "value": f"{message_servant}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara02_rv.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)
