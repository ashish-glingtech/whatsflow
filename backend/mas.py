import json
import sys
import traceback

import requests


class ExtractQrImage():

  @staticmethod
  def start():
    # Perform login and retrieving the cookies
    driver = setup_webdriver()

    print("[*] Logging In", end="\r")
    perform_login(driver)
    # wait_till_loader_finish(driver)
    print("[√] Logging In")

    driver.get("https://app.messageautosender.com/customer/channelList")

    status_button_xpath = """ //section[@id="mainPageContent"] //button[@data-channelid and contains(@id, "status")] """
    status_button = driver.find_element(By.XPATH, status_button_xpath)
    status_button.click()

    connected_message_xpath = """ //section[@id="mainPageContent"] //*[contains(text(), "Connection successful. You can start using system.")] """
    qr_image_xpath = """ //section[@id="mainPageContent"] //*[contains(text(), "Connection successful. You can start using system.")] """

    payload = {
        "receiverMobileNo": ",".join(RECIPIENT_NUMBERS),
        "message": [f""],
    }
    headers = {
        "x-api-key": WHATSAPP_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post("https://app.messageautosender.com/api/v1/message/create", headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print("\t[√] WhatsApp message Sent")
    except:
        print("\t[x] WhatsApp message Sent")

    driver.quit()

  @staticmethod
  def test():
      LOGIN_API = "https://app.messageautosender.com/login"
      STATUS_API = "https://app.messageautosender.com/customer/channel/login/{}"
      DETAILS_API = "https://app.messageautosender.com/api/v1/account/detail"

      resp1 = { "status": "SUCCESS", "imageSource": None }
      resp2 = { "status": "IMAGE_VISIBLE", "imageSource": "data:image/png;base64" }

      payload = {'username': 'hyz6szhi', 'password': 'pMLteC6J@ni5quE'}

      basic = requests.auth.HTTPBasicAuth(payload['username'], payload['password'])
      resp = requests.get(DETAILS_API, auth=basic)
      resp_data = resp.json()
      channel_id = resp_data['result']['channels'][0]['id']

      session = requests.Session()
      headers = {'Content-Type': 'application/x-www-form-urlencoded'}
      resp = session.post(LOGIN_API, data=payload, headers=headers)
      print(resp.status_code)

      resp = session.get(STATUS_API.format(channel_id), auth=basic)
      resp_data = resp.json()
      print(resp_data)


if __name__ == '__main__':
    ExtractQrImage.test()