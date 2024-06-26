import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging

userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
fate_region = os.environ['fateRegion']
webhook_discord_url = os.environ['webhookDiscord']
blue_apple_cron = os.environ.get("MAKE_BLUE_APPLE")
idempotency_key_signature = os.environ.get('IDEMPOTENCY_KEY_SIGNATURE_SECRET')
device_info = os.environ.get('DEVICE_INFO_SECRET')
user_agent_2 = os.environ.get('USER_AGENT_SECRET_2')


userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')


def check_blue_apple_cron(instance):
    if blue_apple_cron:

        cron = croniter(blue_apple_cron)
        next_date = cron.get_next(datetime)
        current_date = datetime.now()
        
        if current_date >= next_date:
            instance.buyBlueApple(1)
            time.sleep(2)


def get_latest_verCode():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']


def main():
    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.set_latest_assets()

        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                instance.topLogin_l()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
                try:
                   time.sleep(2)
                   logger.info(f"\n ======================================== \n [+] 进行友情点召唤 \n ======================================== " )
                   for _ in range(1): # 可定义每次登录时自动抽几次友情10连（默认1次） 
                      instance.drawFP()
                      time.sleep(4)
                       
                except Exception as ex:
                    logger.error(ex)
                    
            except Exception as ex:
                logger.error(ex)


if __name__ == "__main__":
    main()
