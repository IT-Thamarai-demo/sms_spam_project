# SMS Spam Detection: Local Demo Connection Guide (Tanglish)

Intha guide physical Android phone-ah unga laptop backend kooda connect panni demo kaamikka help pannum.

---

## 1. Demo Checklist (Kandippa check panniye aaganum)
- [ ] Unga **Laptop** and **Android Phone** rendume **ore Wi-Fi** network-la irukanum.
- [ ] Mobile-la APK install aagi irukanum.
- [ ] Laptop-la `app.py` start aagi irukanum.

---

## 2. Step 1: PC IP Address-ah Check Pannungah
Unga laptop identity (IP) unga mobile-ku theriya num.
1. Laptop-la **Command Prompt (CMD)** open pannungah.
2. `ipconfig` nu type panni Enter adikkungah.
3. Athula **IPv4 Address** nu irukkura number-ah note pannungah. (Example IP: `10.18.234.93`)

---

## 3. Step 2: Backend-ah Start Pannungah
Backend run pannathaan mobile request-ah accept panna mudiyum.

**Command:**
```bash
# Backend folder kulla poyittu run pannunga
python app.py
```

> [!NOTE]
> Unga code-la `app.run(host="0.0.0.0")` nu irukkum. Ithu yen na, normal-ah Flask laptop-kulla mattum thaan listen pannum. `0.0.0.0` kudutha thaan, vera unga mobile mathiri external devices kooda connect aaga mudiyum (Universal listening).

---

## 4. Step 3: Mobile APK Demo
Mobile APK already unga PC IP-ah thaan target panni build panni irukkura thala, direct-ah work aagum.
1. Mobile-la app-ah open pannungah.
2. Message box-la ethavathu type pannungah (e.g., "Win a free prize").
3. **Scan** button-ah click pannungah.
4. Laptop CMD-la request log varutha nu check pannungah.
5. Mobile screen-la result (Spam/Not Spam) display aagum.

---

## 5. Viva / Interview Special (Oral Explanation)
**Question: "Yen physical device-la 10.0.2.2 work aagala?"**
**Answer:** "Sir, `10.0.2.2` address emulator-ku mattum thaan PC localhost-ah point pannum. Physical phone use pannum pothu nampa PC-oda actual Local IP address kudutha thaan communicate panna mudiyum."

**Question: "Same Wi-Fi network-la yen irukkanum?"**
**Answer:** "Two devices connect aaganum na physical-ah wire illama local network (LAN) vazhiya thaan data transfer aagum. So, Wi-Fi router vazhiya nampa mobile laptop-ah find panni data send pannum."

---

## 6. Troubleshoot (Work aagala na ?)
- **Firewall:** Windows Firewall blocking panna vaaipu irukku. Demo appa windows firewall-ah temporarily **OFF** panni vaiyungah.
- **Wi-Fi Hotspot:** Wi-Fi router illa na, laptop hotspot-la phone-ah connect pannalam.

**Local demo successful na project complete!** All the best for your demo! 🚀
