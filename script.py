from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import requests
import random

# global variables here
driver=webdriver.Firefox()

# New functions code Here 

# note for weight value should be 10-120
# checkValueValidation(10, 120, this)

# note for tall value should be 10-120
# checkValueValidation(100, 200, this)

def get_important_information_to_fill_weight_tall(cookies):
   
    # suggestions to make the code better :
    # 1. scrape all students data at once then posting them all together
    # 2. login to microsoft and get the cookies with requests library instead of selenium library

    FitnessWeightHeightMesaures_page = scrape_FitnessWeightHeightMesaures_page(cookies)
    schools = [ i['value'] for i in get_schools_data(FitnessWeightHeightMesaures_page)][0]
    grades = get_grades_data(FitnessWeightHeightMesaures_page)
    controlled_ranodmness = {'سابع' : [(140,150) ,(48,55)] ,
                        'ثامن' : [(148,156) ,(55,62)] ,
                        'تاسع' : [(152,160) ,(60,69)] ,
                        'عاشر' : [(157,164) ,(64,71)] ,
                        'حادي عشر' : [(163,170) ,(64,75)] ,
                        'ثاني عشر' : [(163,175) ,(65,78)]}

    for grade in grades:
        html_text = scrape_students_ids_html(cookies , schools , grade['value'])
        students_data = [i for i in get_students_ids(html_text)]
        for item in controlled_ranodmness:
            if item in grade['text']:
                h_range , w_range = controlled_ranodmness[item]
                request_payload = random_request_payload(students_data ,h_range=h_range,w_range=w_range)
        
        response = requests.post(
            'https://jolearn.jo/index.php?r=EFitness/FitnessWeightHeightMesaures/create',
            cookies=cookies,
            data=request_payload
        )
        print(" تم تعبئة الصف بنجاح " + grade['text'])
        print(response.status_code )

def scrape_FitnessWeightHeightMesaures_page(cookies):
    response = requests.get(
        'https://jolearn.jo/index.php?r=EFitness/FitnessWeightHeightMesaures/create',
        cookies=cookies,
    )
    return response.text

def get_grades_data(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    # Find the select dropdown by ID
    select_dropdown = soup.find('select', {'id': 'FitnessSchoolSort_ViewCodeNameWHMeasures_GradeID'})

    # Check if the select dropdown is found
    if select_dropdown:
        # Extract options
        grades = []
        for option in select_dropdown.find_all('option'):
            value = option.get('value')
            text = option.get_text(strip=True)
            if "ختر" not in text :
                grades.append({'value': value, 'text': text})
        # print(grades)
        return grades

def get_schools_data(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    # Find the select dropdown by ID
    select_dropdown = soup.find('select', {'id': 'SchoolID'})

    # Check if the select dropdown is found
    if select_dropdown:
        # Extract options
        schools = []
        for option in select_dropdown.find_all('option'):
            value = option.get('value')
            text = option.get_text(strip=True)
            if len(value):
                schools.append({'value': value, 'text': text})
        # print(schools)
        return schools

def scrape_students_ids_html(cookies , schoolId , gradeId):
    data = {
    'viewCodeName': 'ViewCodeNameWHMeasures',
    'SchoolID': schoolId,
    'GradeID': gradeId,
    # 'SchoolID': '4B9EEE39-FC46-4AA7-A33D-1F3FE5E99AC1',
    # 'GradeID': '6363D458-760B-4E5C-8C1D-E15DDA9C13A1',
    }

    response = requests.post(
        'https://jolearn.jo/index.php?r=EFitness/FitnessWeightHeightMesaures/GetListOfAllStudentsPeriods',
        cookies=cookies,
        data=data,
    )
    return response.text

def get_students_ids(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    # Find all rows with class 'weightHeightMesauresRow'
    rows = soup.find_all('tr', class_='weightHeightMesauresRow')

    # Extract names and corresponding MesaureStudentID values and store in a list of dictionaries
    data = []
    for row in rows:
        name = row.find('td').get_text(strip=True)
        mesaure_student_id = row.find('input', {'name': 'MesaureStudentID'})['value']
        test_period_id = row.find('input', {'name': 'testPeriodID'})['value']
        data.append({'name': name, 'mesaure_student_id': mesaure_student_id, 'test_period_id': test_period_id})

    return data

def random_request_payload(students_data,w_range=(85, 100) , h_range=(100, 120) ):
    # Define the weight and height ranges
    weight_range = w_range
    height_range = h_range

    # Generate the dictionary
    fitness_data = []
    for item in students_data:
        entry = {
            "StudentID": item['mesaure_student_id'],
            "Weight": str(random.randint(*weight_range)),
            "Height": str(random.randint(*height_range)),
            "TestPeriod": item['test_period_id']
        }
        fitness_data.append(entry)

    # Convert the list of dictionaries to a JSON-like string
    fitness_data_str = {'FitnessWeightHeightMesaures':str(fitness_data).replace("'", '"')}
    return fitness_data_str

def get_cookies(driver):
    WebDriverWait(driver, 10).until(EC.url_contains("jolearn"))
    cookies = driver.get_cookies()
    cookies = {i['name']: i['value'] for i in cookies}
    return cookies

def go_to_create_page():
    driver.get("https://jolearn.jo/index.php?r=EFitness/FitnessWeightHeightMesaures/create")

def get_school_grades():
    driver.get("https://jolearn.jo/index.php?r=EFitness/FitnessWeightHeightMesaures/create") 
    DROPDOWN = (By.ID, "FitnessSchoolSort_ViewCodeNameWHMeasures_GradeID")
    grades = wait_for_element(driver, DROPDOWN)
    grades = grades

def login_to_jolearn(username, password, driver):
    driver.get("https://jolearn.jo/") 
    login = wait_for_element(driver, (By.CSS_SELECTOR, ".btn.btn-lg"))
    login_url = login.get_attribute('href') 
    login_to_microsoft(username , password , login_url , driver)

def login_to_microsoft (username, password, url ,driver):
    EMAILFIELD = (By.ID, "i0116")
    PASSWORDFIELD = (By.ID, "i0118")
    NEXTBUTTON = (By.ID, "idSIButton9")

    driver.get(url)

    # wait for email field and enter email
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(username)

    # Click Next
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

    # wait for password field and enter password
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(password)

    # Click Login - same id?
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

def wait_for_element(driver, locator , overlay_locator=False):
    try:
        if overlay_locator:
            # Wait for the overlay element to disappear
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except StaleElementReferenceException:
        return wait_for_element(driver, locator)
    return element

def click_element( element):
    element.click()
    # return element

if __name__ == "__main__":
    login_to_jolearn('9841033839@jolearn.jo' , 'Ahmad33839' , driver)
    cookies = get_cookies(driver)
    
    get_important_information_to_fill_weight_tall(cookies)
    
    print('finished')
