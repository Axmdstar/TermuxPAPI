# NOTE

## Features
- Send SMS and check SMS indox
- finical analysis using sms messages
- serve and listen for update and events with api

### Finical Analysis
- Getting total income and expenses
- information about specific transaction
- getting transactions in specific time range

### Content Provider Query Doc
- https://github.com/AzeemIdrisi/PhoneSploit-Pro/discussions/74
- https://android.googlesource.com/platform/frameworks/base/+/55f86b1811f0411a5d685d6c97772b846a706e19/cmds/content/src/com/android/commands/content/Content.java
+ "\n"
        + "usage: adb shell content query --uri <URI> [--user <USER_ID>]"
                + " [--projection <PROJECTION>] [--where <WHERE>] [--sort <SORT_ORDER>]\n"
        + "  <PROJECTION> is a list of colon separated column names and is formatted:\n"
        + "  <COLUMN_NAME>[:<COLUMN_NAME>...]\n"
        + "  <SORT_ORDER> is the order in which rows in the result should be sorted.\n"
        + "  Example:\n"
        + "  # Select \"name\" and \"value\" columns from secure settings where \"name\" is "
                + "equal to \"new_setting\" and sort the result by name in ascending order.\n"
        + "  adb shell content query --uri content://settings/secure --projection name:value"
                + " --where \"name=\'new_setting\'\" --sort \"name ASC\"\n"
