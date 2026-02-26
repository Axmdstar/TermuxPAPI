from datetime import datetime
import re

msg = [
    {
        "address": "192",
        "date": "1757325809622",
        "body": "[-EVCPLUS-] $0.01 ayaad uwareejisay XXX XXX XXX(0612553160), Tar: 08/09/25 13:05:20, Haraagaagu waa $1.08.\nLa soo deg App-ka WAAFI http://onelink.to/waafi",
    },
    {
        "address": "192",
        "date": "1757329008655",
        "body": "[-EVCPLUS-] $0.01 ayaad uwareejisay XXX XXX XXX(0612553160), Tar: 08/09/25 13:56:47, Haraagaagu waa $1.07.\nLa soo deg App-ka WAAFI http://onelink.to/waafi",
    },
    {
        "address": "192",
        "date": "1757414938716",
        "body": "[-EVCPLUS-] $0.5 ayaad uwareejisay XXX XXX XXX(0613072016), Tar: 09/09/25 13:52:13, Haraagaagu waa $0.57.\nLa soo deg App-ka WAAFI http://onelink.to/waafi",
    },
    {
        "address": "192",
        "date": "1760254381073",
        "body": "[-EVCPLUS-] $0.25 ayaad uwareejisay XXX XXX XXX(0614918632), Tar: 12/10/25 10:32:47, Haraagaagu waa $6.87.\nLa soo deg App-ka WAAFI http://onelink.to/waafi",
    },
    {
        "address": "192",
        "date": "1760254448030",
        "body": "[-EVCPLUS-] $1 ayaad uwareejisay XXX XXX XXX(0613072016), Tar: 12/10/25 10:37:29, Haraagaagu waa $0.\nLa soo deg App-ka WAAFI http://onelink.to/waafi",
    },
    {
        "address": "192",
        "date": "1460254448030",
        "body": "[-EVCPlus-] waxaad $20.73 ka heshay 0612553160, Tar: 22/01/24 11:03:17 haraagagu waa $1,014.37.\nLa soo deg App-ka WAAFI http://onelink.to/waafi",
    },
    {
        # Beco
        "address": "192",
        "date": "1460254448030",
        "body": "EVCPlus -> TransferId: 19660409360\nGuri No: 220523.\nWaxaad $ 72.16 ka bixisay AXMED FAARAX MAX/ED XAAJI,\nHaraagaagu waa: $51.73.",
    },
    {
        # Salaam Bank
        "address": "192",
        "date": "1460254448030",
        "body": "[-EVCPlus-] waxaad kala baxday $10 Xisaabtaada bangiga No: 328XXX58, haraagaagu waa  $10.18.",
    },
]


# NOTE:
# For Analysis we need:
# 1. Total number of messages
# 2. Total amount transferred
# 3. Average amount transferred per message
# 4. Total amount transferred to each unique recipient
# 5. Sort messages by date
# 6. Identify the most frequent recipient
# 7. filter uwareejisay and heshey messages
# 8. Track balance(haraagagu) changes over time
# NOTE:
# Data we need to extract from each message:
# 1. Amount transferred (lacagta)
# 2. Recipient (to)
# 3. Date of transfer (date)
# 4. Balance after transfer (haraagagu)
# 5. Type of transaction (uwareejisay or heshey)
# We can use regular expressions to extract the relevant information from the message body. For example:
#
class Message:
    def __init__(
        self, amount, recipient, recipient_num, date, rest_balance, transaction_type
    ) -> None:
        self.amount: float = amount
        self.recipient: str = recipient
        self.recipient_num: str = recipient_num
        self.date: str = date
        self.rest_balance: float = rest_balance
        self.transaction_type: str = transaction_type


class MessageParser:
    def __init__(self, messages: list) -> None:
        self.messages = messages

    def __parse_message(self, message) -> Message:
        """Parse a single message and extract relevant information."""

        # INFO: Check for Beco message
        beco = ("Guri No:" in message["body"]) and ("ka bixisay" in message["body"])
        if beco:
            print("Beco message detected, skipping parsing.")
            return Message(0, "Beco", "", "", 0, "beco")

        # INFO: Check for Salaam Bank message
        salaam = "bangiga No:" in message["body"]
        if salaam:
            return Message(0, "salaam", "", "", 0, "salaam")

        # Extract amount
        amount_match = re.search(r"\$[\d.]+", message["body"])
        amount = amount_match.group(0) if amount_match else None
        # print(f"Extracted amount: {amount}")

        # Determine transaction type
        transaction_type = (
            "uwareejisay" if "uwareejisay" in message["body"] else "heshey"
        )

        # Extract recipient
        recipient_match = ""
        recipient_match_num = ""
        if transaction_type == "uwareejisay":
            recipient_match = re.search(r"uwareejisay\s(.+)\b\(", message["body"])
            recipient_match_num = re.search(r"\b\((\d+)\)", message["body"])
        else:
            recipient_match = re.search(r"heshay\s+(\d+)", message["body"])

        recipient = recipient_match.group(1) if recipient_match else None
        recipient_num = recipient_match_num.group(1) if recipient_match_num else None
        # print(f"Extracted recipient: {recipient}")
        # print(f"Extracted recipient Number: {recipient_num}")

        # Extract date
        date_match = re.search(
            r"Tar:\s+(\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})", message["body"]
        )
        date = date_match.group(1) if date_match else None
        # print(f"Extracted date: {date}")

        # Extract balance after transfer
        balance_match = re.search(
            r"(Haraagaagu|haraagagu)\s+waa\s+\$[\d,.]+", message["body"]
        )
        rest_balance = balance_match.group(0).split()[-1] if balance_match else None
        rest_balance = rest_balance.replace(",", "") if rest_balance else None
        # print(f"Extracted rest balance: {rest_balance}")
        # print(f"rest balance Raw: {balance_match.group(0) if balance_match else 'N/A'}")
        # print(f"Extracted rest balance: {rest_balance[1:-1]}")

        # print(f"Determined transaction type: {transaction_type}")
        # print("_______________________________________________________")

        return Message(
            float(amount[1:] if amount else 0),
            recipient,
            recipient_num,
            date,
            float(rest_balance[1:-1] if rest_balance else 0),
            transaction_type,
        )

    def parse_all_messages(self) -> list[Message]:
        """Parse all messages and return a list of parsed data."""
        parsed_messages = []
        for message in self.messages:
            parsed_data = self.__parse_message(message)
            if (
                parsed_data.transaction_type == "beco"
                or parsed_data.transaction_type == "salaam"
            ):
                continue
            parsed_messages.append(parsed_data)
        return parsed_messages


class SmsAnalysis:
    def __init__(self, messages):
        self.messages = MessageParser(messages).parse_all_messages()

    def Number_Of_Messages(self):
        """Return the total number of messages."""
        print(f"Total number of messages: {len(self.messages)}")
        return len(self.messages)

    def Total_Amount_Recieved(self):
        """Calculate the total amount Revieved."""
        heshay_messages = []
        for message in self.messages:
            if message.transaction_type == "heshey":
                heshay_messages.append(message)

        total_amount = sum(message.amount for message in heshay_messages)

        print(f"Total amount Recieved: ${total_amount:.2f}")
        return total_amount

    def Total_Amount_Transferred(self, messages=None):
        """Calculate the total amount transferred."""
        uwareejisay_messages = []

        if messages is None:
            messages = self.messages

        for message in messages:
            if message.transaction_type == "uwareejisay":
                uwareejisay_messages.append(message)

        total_amount = sum(message.amount for message in uwareejisay_messages)

        print(f"Total amount transferred: ${total_amount:.2f}")
        return total_amount

    def FilterByRecipient(self, recipient):
        """Filter messages by recipient."""
        filtered_messages = []
        for message in self.messages:
            if message.recipient == recipient or message.recipient_num == recipient:
                filtered_messages.append(message)
        print(
            f"Messages filtered by recipient '{recipient}': {len(filtered_messages)} "
        )
        self.Total_Amount_Transferred(filtered_messages)
        return filtered_messages


# NOTE:
# 1. Total number of messages
SmsAnalysis(msg).Number_Of_Messages()
# 2. Total amount transferred
# SmsAnalysis(msg).Total_Amount_Transferred()
# 3. Total amount Recieved
# SmsAnalysis(msg).Total_Amount_Recieved()
