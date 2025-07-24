🔧 Telegram Auto-Inviter Tool  V1
Created by: DhautarChor

🧠 Overview:
This powerful tool automates the process of inviting active users from one Telegram group/channel to another. It smartly avoids inactive users, mimics human behavior, and ensures compliance with Telegram's anti-spam rules.

⭐ Features:

✅ User Activity Filtering
- Detects and skips inactive users using Telegram's status types:
  • Recently Online
  • Last Week
  • Last Month
  • Last Seen with datetime comparison
- Ensures only active members are targeted for higher engagement.

🧠 AI-style Personalized Messages
- Sends messages using dynamic, friendly templates:
  "Hey {name}, check this out! {link}"
  "Yo {name}, don’t miss this! {link}"
  ...
- Automatically includes the user's first name and the channel invite link.

⌨️ Typing Simulation
- Mimics human typing using:
  SetTypingRequest + timed delay
- Makes message delivery more natural and less bot-like.

⏱️ Rate Limiting with Random Delays
- Randomized delay between each message (70–120 seconds) to:
  • Evade Telegram anti-spam detection
  • Mimic human outreach behavior

📂 CSV + Text Logging
- Stores user data and invited users to:
  • scraped_users.csv
  • invited_users.txt

🚫 FloodWait Handling
- Automatically handles FloodWaitError by sleeping for the Telegram-specified duration, preventing crashes or bans.

📊 Progress Bar & Color Logging
- Live progress bar using tqdm
- Colored output using colorama for:
  • Invited (Green)
  • Skipped (Yellow)
  • Errors (Red)

📁 File Structure:
- niga.py → Main script
- scraped_users.csv → Extracted usernames from the source group
- invited_users.txt → Successfully invited usernames

🧑‍💻 Developer Credit:
This tool is proudly created by DhautarChor.
For support, contributions, or credits — reach out via GitHub or Telegram.
