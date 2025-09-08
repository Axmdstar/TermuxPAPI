import re
import subprocess
import time

import uiautomator2 as u2


def run_adb_command(command):
    """Execute an ADB command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


class AndroidApi:
    def __init__(self, device_ip):
        self.device_ip = device_ip
        self.d = None
        self.evc_buttons = ["pin", "send"]

    def connect(self):
        """Connect to the Android device using uiautomator2."""
        self.d = u2.connect(self.device_ip)

    def dial_ussd(self, ussd_code):
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
        time.sleep(7)  # Wait for the USSD dialog to appear

    def dial_ussd_evc(self, ussd_code):
        """Dial a EVC USSD code using adb."""
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
        time.sleep(5)  # Wait for the USSD dialog to appear

    def click_button(self, button_text):
        """Click a button with the specified text."""
        if self.d is None:
            raise Exception("Device not connected. Call connect() first.")

        button = self.d(text=button_text)
        if button.exists:
            button.click()
            return True
        return False

    def wirte_text(self, text):
        """Write text into the focused input field."""
        # if self.d is None:
        #     raise Exception("Device not connected. Call connect() first.")
        #
        # self.d.send_keys(text)
        returncode, stdout, stderr = run_adb_command(f"adb shell input text {text}")
        if "SecurityException" in stderr or "INJECT_EVENTS" in stderr:
            print("Permission error: Cannot inject events without proper privileges")
            print("This script will likely not work without root access")
        time.sleep(2)

    def autamate_send_evc(self, evc_number, amount="0.9"):
        """Automate sending EVC number."""
        self.connect()
        self.dial_ussd_evc(f"*712*{evc_number}*{amount}%23")
        self.wirte_text("1234")
        self.click_button("send")

    def ScreenaTextExtractor(self):
        """Extract Text from a Node, with specific resourceId"""
        self.connect()
        if self.d is None:
            raise Exception("Device not connected. Call Connect() first.")
        text = self.d(
            resourceId="com.android.phone:id/message",
        ).get_text()
        return text

    def ParseTextToDict(self, Text: str):
        """Create Dict formt of the extracted text."""
        dummy: str = "[-EVCPLUS-] $0.01 ayaad uwareejisay 0612553160, Tar: 08/09/25 13:56:47, Haraagaagu waa $1.07.&#10;La soo deg App-ka WAAFI http://onelink.to/waafi@"
        uwareejisayPartition = dummy.partition("uwareejisay")
        lacagta = re.findall(r"\$\d.\d+", uwareejisayPartition[0])
        tariixa = re.findall(r"\d{2}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}", dummy)
        # dummylints = dummy.splitlines()
        # dummySpace = dummy.partition()

    def GetXmlDump(self):
        """Get the XML dump of the current UI hierarchy."""
        self.connect()
        if self.d is None:
            raise Exception("Device not connected. Call connect() first.")
        return self.d.dump_hierarchy()

    def automate_ussd_interaction(self, ussd_code, button_texts):
        """Automate the USSD interaction by dialing and clicking buttons."""
        self.connect()
        self.dial_ussd(ussd_code)

        self.wirte_text("1")
        self.click_button("Send")
        self.wirte_text("1")
        self.click_button("Send")

        # for text in button_texts:
        #     if not self.click_button(text):
        #         print(f"Button with text '{text}' not found.")
        #         break
        #     time.sleep(2)  # Wait between clicks


# NOTE: create class instance
api = AndroidApi("192.168.6.100:38809")
# api.automate_ussd_interaction("*100%23", ["1", "1", "OK"])
time.sleep(4)

# NOTE: Test getting Text from the xml node
# api.ScreenaTextExtractor()

# NOTE: get UI Xml Dump to parse Text on the current screen
file = api.GetXmlDump()
with open("dump.xml", "w", encoding="utf-8") as f:
    f.write(file)

# NOTE: Test Evc Send
# api.autamate_send_evc("613072016", "0.9")
# api.wirte_text("1234")

# def ussd_automation():
#     # Connect to device (requires USB debugging)
#     # TODO: Change the IP address to your device's address, use env or variable
#     d = u2.connect("192.168.6.100:38809")
#
#     # Dial USSD code
#     subprocess.call(
#         [
#             "adb",
#             "shell",
#             "am",
#             "start",
#             "-a",
#             "android.intent.action.CALL",
#             "-d",
#             "tel:*100%23",
#         ]
#     )
#
#     time.sleep(5)
#
#     # Try to find and click elements (may work better than input commands)
#     # This requires knowing the UI elements' resource IDs or text
#     ok_button = d(text="OK")
#     if ok_button.exists:
#         ok_button.click()
#
#     # Additional automation steps...
#
#
# ussd_automation()
