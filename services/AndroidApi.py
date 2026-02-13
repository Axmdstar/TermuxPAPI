import re
import subprocess
import time

import uiautomator2 as u2


class AndroidApi:
    def __init__(self, device_ip=None, serial=None):
        self.device_ip = device_ip
        self.serial = serial
        self.d = None
        self.evc_buttons = ["pin", "send"]
        self.wait_time_process = 5
        self.wait_time_action = 1
        self.message_list = []

    def connect(self):
        """Connect to the Android device using uiautomator2."""
        if self.d is None:
            # self.d = u2.connect(self.device_ip or "")
            self.d = u2.connect(self.device_ip or "")

    # NOTE: Unitility Methods
    def __run_adb_command(self, command) -> tuple[int, str, str]:
        """Execute an ADB command and return the result"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)

    def __dial_ussd(self, ussd_code):
        """Dial a USSD code using adb."""
        subprocess.call(
            [
                "adb",
                "shell",
                "am",
                "start",
                "-a",
                "android.intent.action.CALL",
                "-d",
                f"tel:{ussd_code}",
            ]
        )
        time.sleep(self.wait_time_process)  # Wait for the USSD dialog to appear

    def Query_Formatter(self, query_result: str) -> list[dict[str, str]]:
        """Format the query result into a list of dictionaries."""
        messages = []
        entries = query_result.strip().split("Row: ")
        entries = re.split(r"Row: \d+", query_result.strip())

        for entry in entries[1:]:  # Skip the first empty entry
            message = {}
            fields = entry.strip().split(", ", 2)
            for field in fields:
                key_value = field.split("=")
                if len(key_value) == 2:
                    key, value = key_value
                    message[key] = value
            messages.append(message)
        return messages

    def Query_Phone_Messages(self):
        """Query the phone's SMS messages using adb."""

        returncode, stdout, stderr = self.__run_adb_command("""
            adb shell content query --uri content://sms/inbox\
            --sort date\
            --projection address:date:body\
            --where address='192'\
            """)
        if returncode != 0:
            print("Error querying messages:", stderr)
            raise Exception(stderr)
        # print("Query Result :>>", stdout)
        return stdout

    def __dial_ussd_evc(self, ussd_code) -> None:
        """Dial a EVC USSD code using adb."""
        try:
            subprocess.call(
                [
                    "adb",
                    "shell",
                    "am",
                    "start",
                    "-a",
                    "android.intent.action.CALL",
                    "-d",
                    f"tel:{ussd_code}",
                ]
            )
            time.sleep(self.wait_time_process)  # Wait for the USSD dialog to appear
            return None
        except Exception as e:
            print("Errror Dialing Evc USSD", e)
            raise e

    def click_button(self, button_text):
        """Click a button with the specified text."""
        if self.d is None:
            raise Exception("Device not connected. Call connect() first.")

        button = self.d(text=button_text)
        if button.exists:
            button.click()
            return True
        return False

    def __Write_text(self, text):
        """Write text into the focused input field."""
        if self.d is None:
            raise Exception("Device not connected. Call connect() first.")

        returncode, stdout, stderr = self.__run_adb_command(
            f"adb shell input text {text}"
        )

        if "SecurityException" in stderr or "INJECT_EVENTS" in stderr:
            print("Permission error: Cannot inject events without proper privileges")
            raise Exception(stderr)
        time.sleep(self.wait_time_action)

    def __ScreenTextExtractor(self) -> dict[str, str]:
        """Extract Text from a Node, with specific resourceId"""
        print("Extracting Text from the Screen...")
        self.connect()
        if self.d is None:
            raise Exception("Device not connected. Call Connect() first.")

        text = self.d(
            resourceId="com.android.phone:id/message",
        ).get_text()

        # BUG: ScreenTextExtractor is now concrete and only works for USSD dialogs
        # print(f"Extracted Text: {text}")
        # data = self.ParseTextToDict(text)
        data = text
        return data

    def __ParseTextToDict(self, Text: str) -> dict[str, str]:
        """Create Dict formt of the extracted text."""
        # BUG: This Method is only extracting EVC USSD resposnses
        dummy: str = (
            Text
            or "[-EVCPLUS-] $0.01 ayaad uwareejisay 0612553160, Tar: 08/09/25 13:56:47, Haraagaagu waa $1.07.&#10;La soo deg App-ka WAAFI http://onelink.to/waafi@"
        )

        # Check for insufficient balance
        if dummy.find("kuguma filna") != -1:
            raise Exception("Insufficient Balance")

        uwareejisayPartition = dummy.partition("uwareejisay")
        lacagta = re.findall(r"\$\d.\d+", uwareejisayPartition[0])
        tariixa = re.findall(r"\d{2}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}", dummy)
        print(lacagta)
        print(tariixa)
        data = {
            "amount": lacagta[0],
            "to": uwareejisayPartition[2].split(",")[0].strip(),
            "date": tariixa[0],
        }
        return data

    def __GetXmlDump(self):
        """Get the XML dump of the current UI hierarchy."""
        self.connect()
        if self.d is None:
            raise Exception("Device not connected. Call connect() first.")
        return self.d.dump_hierarchy()

    # NOTE:  Workflow Methods
    def automate_ussd_interaction(self, ussd_code, button_texts):
        """Automate the USSD interaction by dialing and clicking buttons."""
        self.connect()
        self.__dial_ussd(ussd_code)

        self.__Write_text("1")
        self.click_button("Send")
        time.sleep(self.wait_time_process)  # Wait for the USSD dialog to appear
        self.__Write_text("1")
        self.click_button("Send")

    def Somnet_Workflow(self, ussd_code):
        """Automate the Somnet USSD interaction."""
        self.connect()
        self.__dial_ussd(ussd_code)

        screen_text = self.__ScreenTextExtractor()
        print(screen_text)
        self.click_button("OK")

    def Read_Sms_Workflow(self):
        """Automate reading SMS messages."""
        messages = self.Query_Phone_Messages()
        formatted_messages = self.Query_Formatter(messages)

        # INFO: Print the formatted messages for debugging
        # for i in range(min(10, len(formatted_messages))):
        #     print(f"Message {i}:")
        #     print(f"  Address: {formatted_messages[i].get('address', 'N/A')}")
        #     print(f"  Date: {formatted_messages[i].get('date', 'N/A')}")
        #     print(f"  Body: {formatted_messages[i].get('body', 'N/A')}")

        self.message_list = formatted_messages

    def autamate_send_evc(self, evc_number, amount="0.9", pin="5511"):
        """Automate sending EVC number."""
        try:
            self.connect()
            self.__dial_ussd_evc(f"*712*{evc_number}*{amount}%23")
            self.__Write_text(pin)

            if self.click_button("Send"):
                # TODO: Send response to api
                print("send button clicked")
                data = self.__ScreenTextExtractor()
                print(data)
                self.click_button("OK")
                return data
            else:
                raise Exception("Send button not found")

        except Exception as e:
            print(e)
            return None


# NOTE: create class instance usind Wifi IP of the device
# api2 = AndroidApi("192.168.6.106:34767")


# TODO: test with multiple devices
# 11 Pro = 9d64ab2553a5
# Samsumg F12 RZ8RA1F2S5A
api = AndroidApi()
# api = AndroidApi("RZ8RA1F2S5A")
# api2 = AndroidApi("9d64ab2553a5")
# api.automate_ussd_interaction("*100%23", ["1", "1", "OK"])
# api2.automate_ussd_interaction("*100%23", ["1", "1", "OK"])
# time.sleep(4)

# TODO: Somnet Workflow
# api.Somnet_Workflow("*100*1%23")

# TODO: Read Sms Workflow
api.Read_Sms_Workflow()
print(api.message_list)
# NOTE: Send EVC
# api.autamate_send_evc("612553160", "10")

# NOTE: Test Evc Send
# api.autamate_send_evc("613072016", "0.9")
# api.wirte_text("1234")

# NOTE: Test Parsing Text to Dict
# text = api.ParseTextToDict("Haraagaagu xissabtaadu kuguma filna, mobile No:")
# print(text)
