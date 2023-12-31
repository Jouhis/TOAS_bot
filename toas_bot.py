from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

from datetime import datetime

from time import sleep


class ToasBot:
    """
    A bot that can access, reserve and manage sauna, laundry and club room times from TOAS's website.
    """

    def __init__(self):
        self.driver = self.login_and_go_to_booking_page(
            credentials_path="credentials.txt"
        )
        self.current_booking_type = None
        self.current_staircase = None
        self._update_date()

    def _read_credentials(self, file_path):
        """
        Reads the credentials from a txt-file and returns them in a list [username, password]
        """
        with open(file_path, "r") as file:
            username = file.readline().strip()
            password = file.readline().strip()
            return [username, password]

    def login_and_go_to_booking_page(self, credentials_path):
        """
        Starts the browser, logs in and goes to the sauna reservation page. Returns the driver.
        """
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()))
        # Move the window to the second monitor
        driver.set_window_position(4000, 0)
        driver.maximize_window()
        driver.get(
            "https://identity.etampuuri.fi/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dtoas-asukassivut%26redirect_uri%3Dhttps%253A%252F%252Fomatoas.toas.fi%252Fsignin-callback%26response_type%3Dcode%26scope%3Dopenid%2520eTampuuri.Front%26state%3Dd09a3e75ac7345c58ed8b43f7e424a72%26code_challenge%3D70I8UHS5jhBsxbLykbtRNBEACBCl9iAMgZs4c4U3REw%26code_challenge_method%3DS256%26response_mode%3Dquery"
        )
        credentials = self._read_credentials(credentials_path)
        # Login
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Email"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Password"))
        )
        username_field.send_keys(credentials[0])
        password_field.send_keys(credentials[1])
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "loginButton"))
        ).click()
        # Open reservation page
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "etusivu-asumisenpalvelut-tiili-10-asumisenpalvelut-tiili-1-link-0",
                )
            )
        ).click()
        # Change handle to the new window
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        self.current_booking_type = (
            "pesuvuorot"  # Default booking type opnens when logging in
        )
        self.current_staircase = "A-B"  # Default staircase opens when logging in
        return driver

    def open_sauna_reservation_page(self):
        """
        Opens the sauna reservation page.
        """
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "saunavuorot"))
            ).click()
            self.current_booking_type = "saunavuorot"
            self.current_staircase = (
                WebDriverWait(self.driver, 20)
                .until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//div[@class='box service-nav']/span[@class='selected']",
                        )
                    )
                )
                .text.split(" ")[-1]  # TODO: FIX THIS
            )
            self._update_date()
        except (
            selenium.common.exceptions.TimeoutException,
            selenium.common.exceptions.ElementNotInteractableException,
            selenium.common.exceptions.ElementClickInterceptedException,
        ):
            print("Failed to open laundry reservation page")

    def open_laundry_reservation_page(self):
        """
        Opens the laundry reservation page.
        """
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "pesuvuorot"))
            ).click()
            self.current_booking_type = "pesuvuorot"
            self.current_staircase = (
                WebDriverWait(self.driver, 20)
                .until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//div[@class='box service-nav']/span[@class='selected']",
                        )
                    )
                )
                .text.split(" ")[-1]  # TODO: FIX THIS
            )
            self._update_date()
        except (
            selenium.common.exceptions.TimeoutException,
            selenium.common.exceptions.ElementNotInteractableException,
            selenium.common.exceptions.ElementClickInterceptedException,
        ):
            print("Failed to open laundry reservation page")

    def open_club_room_reservation_page(self):
        """
        Opens the club room reservation page.
        """
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "kerhohuoneet"))
        ).click()
        self.current_booking_type = "kerhohuoneet"
        self.current_staircase = None
        self._update_date()

    def next_day(self):
        """
        Navigates to the next day in the reservation calendar.
        """
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "next"))
        ).click()
        self._update_date()
        sleep(0.5)

    def previous_day(self):
        """
        Navigates to the previous day in the reservation calendar.
        """
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "prev"))
        ).click()
        self._update_date()
        sleep(0.5)

    def navigate_to_first_day(self):
        """
        Navigates to the first day in the reservation calendar.
        """
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "prev"))
                ).click()
                self._update_date()
                sleep(0.5)
            except (
                selenium.common.exceptions.TimeoutException,
                selenium.common.exceptions.ElementNotInteractableException,
                selenium.common.exceptions.ElementClickInterceptedException,
            ):
                print("Navigated to first day")
                return

    def navigate_to_last_day(self):
        """
        Navigates to the last day in the reservation calendar.
        """
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "next"))
                ).click()
                self._update_date()
                sleep(0.5)
            except (
                selenium.common.exceptions.TimeoutException,
                selenium.common.exceptions.ElementNotInteractableException,
                selenium.common.exceptions.ElementClickInterceptedException,
            ):
                print("Navigated to last day")
                return

    def refresh_page(self):
        """
        Refreshes the page.
        """
        self.driver.refresh()

    def get_bookable_staircases(self):
        """
        Returns a list of the bookable staircases. The selected staircase is marked with span and does
        not contain a hyperlink. Other staircases are hyperlinks. The last one is "Vapaat ajat" and should
        be skipped.
        """
        # Wait for the elements to be clickable
        staircases = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='box service-nav']/*")
            )
        )

        # Extract text from elements, excluding the last item ("Vapaat ajat")
        staircase_texts = [staircase.text.strip()
                           for staircase in staircases[:-1]]

        return staircase_texts

    def select_staricase(self, staircase: str):
        """
        Selects the staircase in the sauna reservation page.
        """
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//div[@class='box service-nav']/a[contains(text(), '{staircase}')]",
                    )
                )
            ).click()
            self.current_staircase = staircase
            print(f"Selected staircase {staircase}")
        except (
            selenium.common.exceptions.TimeoutException,
            selenium.common.exceptions.ElementNotInteractableException,
            selenium.common.exceptions.ElementClickInterceptedException,
            selenium.common.exceptions.InvalidSelectorException,
        ):
            print(f"Error selecting staircase {staircase}")

    def get_bookable_items(self):
        # HMTL FORMAT:
        """<tbody>
            <tr>
                <td></td>
                <td class="head"> <h3>Pesukone 1</h3> </td>
                <td class="head"> <h3>Pesukone 2</h3> </td>
                <td class="head"> <h3>Kuivausrumpu 1</h3> </td>
                <td class="head"> <h3>Kuivausrumpu 2</h3> </td>
            </tr>
        </tbody>"""
        # Get the text of the items in first row (the item names)
        items = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//table[@class='calendar']/tbody/tr[1]/td")
            )
        )
        items = [item.text for item in items[1:]]
        print(items)

    def _update_date(self):
        """
        Returns the current date in format YYYY-MM-DD
        """
        self.current_date = datetime.strptime(
            WebDriverWait(self.driver, 20)
            .until(EC.presence_of_element_located((By.XPATH, "//a[@class='js-datepicker']")))
            .text,
            "%d.%m.%Y",
        ).date()


'''    def get_available_sauna_times(self):
        """
        Returns dataframe of available sauna times in format [date, time, reservation_status]
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "saunavuorot"))).click()
        # Click through the sauna reservation pages and get the available times
        df = pd.DataFrame(columns=["date", "time", "reservation_status"])
        while True:
            try:
                sleep(0.6) # Wait for the calendar to load
                # Get the available date
                date = datetime.strptime(WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "js-datepicker")))[0].text, "%d.%m.%Y").date()
                # Get the available times
                calendar = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "calendar")))[0]
                rows = calendar.text.split("\n")[2:]
                # If time can be converted to datetime add to the dataframe
                new_rows = []
                for row in rows:
                    time = datetime.strptime(row.split()[0], "%H:%M").time()
                    reservation_status = 1 if row.split()[1] == "VARATTU" else 0
                    new_row = (date, time, reservation_status)
                    # Check if this combination of date and time already exists in df
                    if not ((df['date'] == date) & (df['time'] == time)).any():
                        new_rows.append(new_row)
                new_rows_df = pd.DataFrame(new_rows, columns=["date", "time", "reservation_status"])
                df = pd.concat([df, new_rows_df], ignore_index=True)
                # Click the next day button
                WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "next"))).click()
            except (selenium.common.exceptions.TimeoutException,
            selenium.common.exceptions.ElementNotInteractableException,
            selenium.common.exceptions.ElementClickInterceptedException):
                return df
            except Exception as e:
                print(e)
                return df


    def check_sauna_time_availability(self, df, preferred_sauna_time: str):
        """
        Checks if the preferred sauna time is available. Returns True if available, False if not available.
        """
        try:
            # Convert preferred sauna time to datetime and round time to closest 30 min interval datetime.strptime("20:30 2023-12-15", "%H:%M %Y-%m-%d")
            pref = datetime.strptime(preferred_sauna_time, "%H:%M %Y-%m-%d")
            pref = pref.replace(minute=pref.minute // 30 * 30)
            filtered_df = df.loc[(df["date"] == pref.date()) & (df["time"] == pref.time())]
            if not filtered_df.empty:
                return filtered_df["reservation_status"].values[0] == 0
            else:
                return False
        except Exception as e:
            print(e)
            return False


    def reserve_sauna(self, preferred_sauna_time: str):
        """
        Reserves the sauna for the preferred time. preferred_sauna_time format: "HH:MM YYYY-MM-DD"
        """
        pref = datetime.strptime(preferred_sauna_time, "%H:%M %Y-%m-%d")
        # Click through the sauna reservation pages until the correct date is found
        wrong_date = True
        while wrong_date:
            date = datetime.strptime(WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "js-datepicker")))[0].text, "%d.%m.%Y").date()
            if date == pref.date():
                break
            WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "next"))).click()
            time.sleep(1)
            print(f"Wrong date: {date}")
        # Click correct time
        row_xpath = f"//table[@class='calendar']/tbody/tr[td[contains(text(), '{pref.time().strftime('%H:%M')}')]]"
        row = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, row_xpath)))
        reserve_button_xpath = f"//table[@class='calendar']/tbody/tr[td[contains(text(), '{pref.time().strftime('%H:%M')}')]]/td[2]"
        row.find_element(By.XPATH, reserve_button_xpath).click() # Find the button within the row
        reserve_div_xpath = f"//div[@class='tooltipbutton']"
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, reserve_div_xpath))).click()
        print(f"Reserved sauna for {pref.date()} at {pref.time()}")'''
