from selenium import webdriver
from selenium.webdriver.common.by import By

# Initalizes testdata and executes tests
def performtest():
    driver = webdriver.Chrome()
    testdata = []
    testdata['url'] = "https://psychologbarlinek.pl/"
    testdata['title'] = "Gabinet Psychologiczny Diagnoza & Terapia - Agnieszka Komorowska"
    testdata['header'] = "Gabinet Psychologiczny Diagnoza & Terapia Agnieszka Komorowska"
    testdata['content_header'] = "Bo w życiu chodzi o ludzi"
    testdata['offerpagename'] = "Oferta"
    test_pageload(driver, testdata)
    test_pages(driver, testdata)
    
# Checks if the page is loaded correctly and if header is displayed
def test_pageload(driver, testdata):
    driver.get(testdata['url'])
    title = driver.title
    assert title == testdata['title']
    driver.implicitly_wait(5)
    header = driver.getElement(by = By.CSS_SELECTOR, value="header h1")
    assert header.text == testdata['header']

# Checks if all the navigation links in top of the page redirect to correct subpages
# todo: look into if there is any clever method to checking which subpage is currently active from page contents, if not have to bruteforce it and hardcode all content headers
def test_pages(driver, testdata):
    header = driver.getElement(by = By.CSS_SELECTOR, value="header h1")
    header.click()

    content_header = driver.getElement(by = By.CSS_SELECTOR, value="section.textContent h2")
    assert content_header.text == testdata['content_header']  

    navigation = driver.getElements(by = By.CSS_SELECTOR, value="nav")

    for subpage in navigation:
        target = subpage.text
        subpage.click()

        if target == testdata['offerpagename']:
            subpage_header = driver.getElement(by = By.CSS_SELECTOR, value="section h2")
            assert target == subpage_header.text
            test_offerpage(driver, testdata)

# Checks if cards in the offer subpage expand after being clicked
def test_offerpage(driver, testdata):
    cards = driver.getElements(by = By.CSS_SELECTOR, value="section div.card")
    for card in cards:
        initial_height = card.rect.height
        card.click()
        transformed_height = card.rect.height
        assert initial_height < transformed_height