from selenium import webdriver
from time import sleep
import chromedriver_binary
import pandas as pd
import oseti
import numpy as np
import const


def main():
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
    sleep(1)
    # 「検索」を押す
    button = driver.find_element_by_xpath(const.search_xpath)
    sleep(1)
    button.click()
    sleep(1)
    # 店名を検索
    button = driver.find_element_by_xpath(const.specific_xpath)
    sleep(1)
    button.click()
    sleep(1)
    restaurant_name = input("レストランの名前を入力してください。")
    button.send_keys(restaurant_name)
    sleep(1)
    button = driver.find_element_by_xpath(const.search_botton_xpath)
    sleep(1)
    button.click()
    # レストランを取得してクチコミを表示
    total_assesment = driver.find_element_by_class_name("ratingLabel_hndnZ").text
    if total_assesment == "規定評価数に達していません":
        print("このレストランは規定評価数に達していない為、分析できません。")
    else:
        button = driver.find_element_by_xpath(const.search_result)
        button.click()
    sleep(5)
    tab_array = driver.window_handles
    driver.switch_to.window(tab_array[1])
    sleep(1)
    button = driver.find_element_by_xpath(const.review_xpath)
    sleep(1)
    button.click()
    sleep(1)
    button = driver.find_element_by_xpath(const.more_xpath)
    sleep(1)
    button.click()
    sleep(1)
    button = driver.find_element_by_xpath(const.toppage_xpath)
    sleep(1)
    button.click()
    sleep(1)


def open_area(driver):
    """
    toppageを開いて
    「銀座」を開いて
    レストランを開いて
    クチコミを表示
    """
    # 一休レストランのTOPページ
    driver.get(const.top_url)
    sleep(1)
    # 「銀座」を押す
    button = driver.find_element_by_xpath(const.ginza_xpath)
    sleep(1)
    button.click()
    sleep(1)
    # レストランを取得
    total_assesment = driver.find_element_by_class_name("ratingCount_6le43").text
    if total_assesment != "規定評価数に達していません":
        button = driver.find_element_by_xpath(
            '//*[@id="__layout"]/div/div[2]/div[1]/main/section[1]/a/div[1]/span/img'
        )
        sleep(1)
        button.click()
        sleep(5)
        tab_array = driver.window_handles
        driver.switch_to.window(tab_array[1])
        sleep(1)
        # クチコミを表示
        button = driver.find_element_by_xpath(const.review_xpath)
        sleep(1)
        button.click()
        sleep(1)
        button = driver.find_element_by_xpath(const.more_xpath)
        sleep(1)
        button.click()
        sleep(1)
        button = driver.find_element_by_xpath(const.toppage_xpath)
        sleep(1)
        button.click()
        sleep(1)


def get_item(driver):
    """
    コメント、味、サービスのスクレイピング
    """
    assesment_url = driver.current_url
    driver.implicitly_wait(3)
    driver.get(assesment_url)
    assesments = driver.find_elements_by_class_name("des_gdIDUsrImprBox")
    # scraping_cnt = ユーザーが選んだ件数をtextで取得
    # lis = int(scraping_cnt) / 10
    i = 4
    # if lis == 1:
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
    print(result_df)


if __name__ == "__main__":
    driver = main()
    # open_restaurant(driver)
    open_area(driver)
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
