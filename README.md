##  B-Cryptic Obfuscation Tool - aka - Practical Obfuscation Pad (POP)

 • Author: Samuel (Shaggy) Bready
 
 • Company: B-Ready Studios LLC
 
 • Version: v0.3.8.5a
 
 • License: MIT
 
 • Status: Production-Ready

    “Encryption hides secrets.
    B-Cryptic hides the fact a message even exists.”

---

What Is B-Cryptic?

B-Cryptic is a next-generation obfuscation tool that makes plaintext invisible to humans, machines, and AI.

It’s built on the Practical Obfuscation Pad (POP) concept — not encryption, but a stealth mechanism. By using 3072 unique tokens, prefix rotation, and statistical noise generation, B-Cryptic transforms your message into gibberish that’s completely reversible only if the full context is known.

It doesn’t hide what you say.
It hides that you ever said anything at all.

---


##  • Key Features

  • 100% reversible encoding/decoding with full token accuracy
  
  • 95 ASCII characters + space supported (printable QWERTY)
  
  • 32 unique tokens per character using a Monolithic Dictionary
  
  • Coming Soon: Word-level obfuscation for 750+ common English terms
  
  • Dynamic prefix rotation: +, *, ^, [- (breaks pattern detection)
  
  • Built-in PDF batch encoding/decoding engine
  
  • Sleek Tkinter GUI with:
  
  • Text and PDF tabs
  
  • Dark mode toggle
  
  • Console-style logs and error handling
  
---


##  • GUI Preview

b_cryptic_ui.py interface includes:

    - Encode/decode tab for plaintext

    - PDF encoding/decoding tab with batch support

    - One-click dark mode toggle

    - Output log window

    - Easy file selection + action buttons

---


##  • Use Cases

- Secure but deniable communication
- Offensive security & red team payloads
- Metadata masking and stealth channels
- ARG/alternate reality games and cryptic puzzles
- Covert personal notes or time capsules
- Anti-AI/NLP communication protection
- Espionage roleplay, LARPing, or Cold War hobbyist projects

---


##  • How It Works

    Every character (a–z, A–Z, 0–9, punctuation, and space) has 32 unique 25-character tokens

    Prefixes (+, *, ^, [-) rotate dynamically to confuse pattern detection

    Tokens are randomly selected with low repetition, generating output that:
      • Looks like nonsense
      • Evades brute-force attacks
      • Can only be reversed with full system definitions

Even if intercepted, the obfuscated message is unreadable without all original tables, prefix logic, and system settings.

---


##  • Project Structure
B-Cryptic/ ├── b_cryptic_core.py # Main encoder/decoder logic ├── b_cryptic_pdf_app.py # PDF handler module ├── b_cryptic_ui.py # Full-featured Tkinter GUI ├── Final_Encoding_Table__*.csv # 8 encoding tables (32×96 per file) ├── requirements.txt ├── version_info.txt ├── README.md


---


##  • Example: Obfuscated Message

> **Plaintext:**  
> `The deal is off. Burn everything.`

> **B-Cryptic Output (Example):**  
> `[+xtl2woT56a7054OBQJ65w840][+K6A3q7O66C48E94A4c03kVcP][+DX9fH5d21M891ik5958zLlo4]...[+xj24qi1lV5FC165o6aVc5118]`
  
> - No decoder can reverse this without full system knowledge  
> - AI/NLP sees this as statistical noise

---


##  • Getting Started

 • Install Dependencies:

 • pip install -r requirements.txt

 • Launch GUI:

 • python b_cryptic_ui.py


##  • Philosophy

B-Cryptic isn’t encryption.
It’s stealth-by-design.

If you're a security researcher, privacy purist, red teamer, or creative mind — B-Cryptic gives you the power to vanish in plain sight.


##  • Credits & Contact

**Author:** Samuel Bready  
**Discord:** [LaterShagGuevara](https://discordapp.com/users/208452282105200640)  

**Email:** [sam@breadystudios.com](mailto:sam@breadystudios.com)  

**Website:** [B-Ready Studios](https://breadystudios.com)

**Linkedin** [Linkedin Profile](https://www.linkedin.com/in/samuel-bready-615bb5115/)


##  • License

B-Cryptic is developed by B-Ready Studios LLC. 
This project is licensed under the MIT License. Use it for good — or at least, for interesting.


##  • Final Words

    “Encryption hides secrets.
    B-Cryptic hides the fact that a secret ever existed.”
