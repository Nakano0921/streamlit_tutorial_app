from selenium import webdriver
import chromedriver_binary
import pandas as pd
import oseti
import numpy as np
import time
import statistics
import const


def main():
    # driver_path = "/app/.chromedriver/bin/chromedriver"
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless") 
    # options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(options=options, executable_path=driver_path)
    # ローカル用のコード(headless)
    # driver = webdriver.Chrome(options=options)
    # ローカル用のコード(not headless)
    driver = webdriver.Chrome()
    return driver


def open_restaurant(driver):
    """
    toppageを開いて
    「検索」を押して、店名を検索
    クチコミを表示
    """
    # 一休レストランのTOPページ
    driver.get(const.top_url)
    time.sleep(1)
    # 「検索」を押す
    button = driver.find_element_by_xpath(const.search_xpath)
    time.sleep(1)
    button.click()
    time.sleep(3)
    # 店名を検索
    button = driver.find_element_by_xpath(const.specific_xpath)
    time.sleep(1)
    button.click()
    time.sleep(3)
    button.send_keys('XEX TOKYO')
    time.sleep(1)
    button = driver.find_element_by_xpath(const.search_botton_xpath)
    time.sleep(1)
    button.click()
    time.sleep(1)
    # レストランを取得してクチコミを表示
    total_assesment = driver.find_element_by_class_name("ratingLabel_hndnZ").text
    if total_assesment == "規定評価数に達していません":
        print("このレストランは規定評価数に達していない為、分析できません。")
    else:
        button = driver.find_element_by_xpath(const.search_result)
        button.click()
    time.sleep(3)
    tab_array = driver.window_handles
    driver.switch_to.window(tab_array[1])
    time.sleep(3)
    button = driver.find_element_by_xpath(const.review_xpath)
    time.sleep(1)
    button.click()
    time.sleep(3)
    button = driver.find_element_by_xpath(const.more_xpath)
    time.sleep(1)
    button.click()
    time.sleep(3)
    button = driver.find_element_by_xpath(const.firstpage_xpath)
    time.sleep(1)
    button.click()
    time.sleep(3)


def open_area(driver):
    """
    toppageを開いて
    「銀座」を開いて
    レストランを開いて
    クチコミを表示
    """
    # 一休レストランのTOPページ
    driver.get(const.top_url)
    driver.implicitly_wait(1)
    # 「銀座」を押す
    ginza_button = driver.find_element_by_xpath(const.ginza_xpath)
    driver.implicitly_wait(1)
    ginza_button.click()
    driver.implicitly_wait(1)
    # レストランを取得
    total_assesment = driver.find_element_by_class_name("ratingCount_6le43").text
    if total_assesment != "規定評価数に達していません":
        top_res_button = driver.find_element_by_xpath(
            '//*[@id="__layout"]/div/div[2]/div[1]/main/section[1]/a/div[1]/span/img'
        )
        driver.implicitly_wait(1)
        top_res_button.click()
        driver.implicitly_wait(5)
        tab_array = driver.window_handles
        driver.switch_to.window(tab_array[1])
        driver.implicitly_wait(1)
        # クチコミを表示
        review_button = driver.find_element_by_xpath(const.review_xpath)
        driver.implicitly_wait(1)
        review_button.click()
        driver.implicitly_wait(5)
        more_see_button = driver.find_element_by_xpath(const.more_xpath)
        driver.implicitly_wait(1)
        more_see_button.click()
        driver.implicitly_wait(1)
        firstpage_button = driver.find_element_by_xpath(const.firstpage_xpath)
        driver.implicitly_wait(1)
        firstpage_button.click()
        driver.implicitly_wait(1)


def get_item(driver):
    """
    コメント、味、サービスのスクレイピング
    """
    assesment_url = driver.current_url
    time.sleep(3)
    driver.get(assesment_url)
    assesments = driver.find_elements_by_class_name("des_gdIDUsrImprBox")
    i = 4
    l = 0
    n = 3
    while l < 9:
        for assesment in assesments:
            if i == 24:
                break
            comment = assesment.find_element_by_xpath(
                f'//*[@id="des_inner"]/div[{i}]/div[3]/table/tbody/tr[3]/td'
            ).text
            comments.append(comment)
            taste = assesment.find_element_by_xpath(
                f'//*[@id="des_inner"]/div[{i}]/div[1]/table/tbody/tr[2]/td[2]/span'
            ).text
            tastes.append(taste)
            service = assesment.find_element_by_xpath(
                f'//*[@id="des_inner"]/div[{i}]/div[1]/table/tbody/tr[3]/td[2]/span'
            ).text
            services.append(service)
            mood = assesment.find_element_by_xpath(
                f'//*[@id="des_inner"]/div[{i}]/div[1]/table/tbody/tr[4]/td[2]/span'
            ).text
            moods.append(mood)
            cospa = assesment.find_element_by_xpath(
                f'//*[@id="des_inner"]/div[{i}]/div[1]/table/tbody/tr[5]/td[2]/span'
            ).text
            cospas.append(cospa)
            i += 2
        if l == 0:
            next_page_bottun = driver.find_element_by_xpath('//*[@id="des_inner"]/div[24]/a[1]')
            time.sleep(1)
            next_page_bottun.click()
            time.sleep(3)
            assesments = driver.find_elements_by_class_name("des_gdIDUsrImprBox")
            l += 1
            i = 4
        elif l >= 1 and l <= 5:
            next_page_bottun = driver.find_element_by_xpath(f'//*[@id="des_inner"]/div[24]/a[{n}]')
            time.sleep(1)
            next_page_bottun.click()
            time.sleep(3)
            assesments = driver.find_elements_by_class_name("des_gdIDUsrImprBox")
            l += 1
            n += 1
            i = 4
        elif l >= 6:
            n = 7
            next_page_bottun = driver.find_element_by_xpath(f'//*[@id="des_inner"]/div[24]/a[{n}]')
            time.sleep(1)
            next_page_bottun.click()
            time.sleep(3)
            l += 1
        

def write_csv():
    """
    csvに保存
    """
    df = pd.DataFrame(
        {
            "comment": [comments[0]],
            "taste": [tastes[0]],
            "service": [services[0]],
            "mood": [moods[0]],
            "cospa": [cospas[0]],
        }
    )
    for (com, tas, ser, moo, cos) in zip(
        comments[1:], tastes[1:], services[1:], moods[1:], cospas[1:]
    ):
        df = df.append(
            {"comment": com, "taste": tas, "service": ser, "mood": moo, "cospa": cos},
            ignore_index=True,
        )
    df.to_csv("assesment.csv")
    # 確認用のコードprint(df)
    result_df = df
    return result_df


def pick_csv(result_df):
    """
    コメントをリスト化※negaposi()でforで回す為
    """
    # 確認用のコードprint(result_df.columns)
    result_comments = []
    result_comment = result_df["comment"]
    for result_com in result_comment[0:]:
        result_comments.append(result_com)
    # 確認用のコードprint(result_comments)
    return result_comments


def negaposi(result_comments):
    """
    ネガポジ判定して、リスト化
    """
    analyzer = oseti.Analyzer()
    result_negaposies = []
    for result_comment in result_comments:
        result_negaposi = analyzer.analyze(result_comment)
        result_average = np.average(result_negaposi)
        result_negaposies.append(result_average)
    # 確認用のコードprint(result_negaposies)
    return result_negaposies


def add_csv(result_negaposies, result_df):
    """
    ネガポジの結果をデータフレームに追加
    """
    result_df["negaposi"] = result_negaposies
    result_df.to_csv("assesment.csv")
    # 確認用のコードprint(result_df)


if __name__ == "__main__":
    driver = main()
    # open_area(driver)
    open_restaurant(driver)
    comments = []
    tastes = []
    services = []
    moods = []
    cospas = []
    get_item(driver)
    result_df = write_csv()
    result_comments = pick_csv(result_df)
    result_negaposies = negaposi(result_comments)
    add_csv(result_negaposies, result_df)