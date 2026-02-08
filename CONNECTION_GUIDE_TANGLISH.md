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
3. Athula **IPv4 Address** nu irukkura number-ah note pannungah (e.g., `10.18.234.93`). 

---

## 3. Step 2: Backend-ah Start Pannungah
Backend run pannathaan mobile request-ah accept panna mudiyum.

**Run Command:**
```bash
python app.py
```

> [!NOTE]
> Unga code-la `app.run(host="0.0.0.0")` nu irukkum. Ithu yen na, normal-ah Flask laptop-kulla mattum thaan listen pannum. `0.0.0.0` kudutha thaan, vera unga mobile mathiri external devices kooda connect aaga mudiyum.

---

## 4. Step 3: Mobile APK Demo
Mobile APK already unga PC IP-ah thaan target panni build panni irukkura thala, direct-ah work aagum.
1. Mobile-la app-ah open pannungah.
2. Message-ah type pannungah.
3. **Scan** button-ah click pannungah.
4. Next 2-3 seconds-la unga Laptop-la request varutha nu paarungah, app-la result display aagum.

---

## 5. Viva / Interview Special (Oral Explanation)
**Question: "Yen 0.0.0.0 use panni run panteenga?"**
**Answer:** "Sir/Ma'am, default-ah Flask localhost-la mattum thaan run aagum. But nampa demo-la physical phone use panrathu naala, laptop network interface-ah open panna thaan phone kooda communicate panna mudiyum. Athunaala `host=0.0.0.0` use panni external requests-ah allow panren."

**Question: "Server side result vanthurucha?"**
**Answer:** "Yes, backend (Flask) processing panni JSON format-la result-ah anuppum, atha Android Retrofit client handle panni UI-la kaattum."

---

## 6. Troubleshoot (Work aagala na ithippa paarunga)
- **Firewall:** Windows Firewall kelavi message blocking panna vaaipu irukku. Demo appa windows firewall-ah temporarily **OFF** panni vaiyungah.
- **Port 5000:** Port 5000 busy-ah iruuntha vera application use pannutha nu check pannungah.

**Local demo successful na project complete!** All the best for your demo! 🚀
