****What is this?****
This is a side-project of mine to attempt to predict professional League of Legends games.<br>
****How is it done?****
Currently, I am using a classification AI to determine the winner. I will publish the code for it once I feel it is ready to see the light of day. There is sadly no official, free and reliable API available for LoLEsports. Luckily, Oracle's Elixir makes much of this data available in a very organised form. Thanks for that.<br>
****Why these leagues?****
I am mainly a fan of LCS and decided to preddict results on the four major regions: LEC, LPL, LCK and LEC. Sadly, there is missing data for the LPL Summer Spit of 2021, thus LPL predictions have been left out.<br>
****Notes****
 - These are only predictions, therefore they might not come true. 
 - The project assumes that past performance can predict future performance, thus "upsets" will most likely never be predicted.
 - I try to run the script once a day, thus some predictions might be too late. 
 - This mainly serves as a repository for me to evaluate the long-term correctness of this approach.
 - Currently, I use a weighted average of a team's previous weeks results; the newer, the more weight a performance is given.
 - Feel free to contact me at huk.adam@protonmail.com
<br>

****LEC****
| Team1                 | Team 2                | Blue_side             | Red_side              | T1_blue_win | T1_red_win | Predicted_winner | Date       | Correct |
| --------------------- | --------------------- | --------------------- | --------------------- | ----------- | ---------- | ---------------- | ---------- | ------- |
| FC Schalke 04 Esports | Team Vitality         | FC Schalke 04 Esports | Team Vitality         | 0.0001      | 0.0        | Team Vitality    | 30/07/2021 |
| SK Gaming             | Astralis              | SK Gaming             | Astralis              | 0.8315      | 0.2439     | SK Gaming        | 30/07/2021 |
| Excel Esports         | Rogue                 | Excel Esports         | Rogue                 | 0.0023      | 0.3163     | Rogue            | 30/07/2021 |
| MAD Lions             | G2 Esports            | MAD Lions             | G2 Esports            | 0.0532      | 0.0154     | G2 Esports       | 30/07/2021 |
| Misfits Gaming        | Fnatic                | Misfits Gaming        | Fnatic                | 0.8539      | 0.9795     | Misfits Gaming   | 30/07/2021 |
| Misfits Gaming        | SK Gaming             | Misfits Gaming        | SK Gaming             | 0.6934      | 0.9855     | Misfits Gaming   | 31/07/2021 |
| Astralis              | Excel Esports         | Astralis              | Excel Esports         | 0.6372      | 0.4653     | Astralis         | 31/07/2021 |
| Rogue                 | Team Vitality         | Rogue                 | Team Vitality         | 1.0         | 0.0001     | Rogue            | 31/07/2021 |
| G2 Esports            | FC Schalke 04 Esports | G2 Esports            | FC Schalke 04 Esports | 0.9813      | 1.0        | G2 Esports       | 31/07/2021 |
| Fnatic                | MAD Lions             | Fnatic                | MAD Lions             | 0.8681      | 0.0436     | Fnatic           | 31/07/2021 |
<br>

****LCS****
| Team1                | Team 2           | Blue_side            | Red_side         | T1_blue_win | T1_red_win | Predicted_winner | Date       | Correct |
| -------------------- | ---------------- | -------------------- | ---------------- | ----------- | ---------- | ---------------- | ---------- | ------- |
| 100 Thieves          | TSM              | 100 Thieves          | TSM              | 0.0739      | 0.2163     | TSM              | 30/07/2021 |
| Evil Geniuses        | Cloud9           | Evil Geniuses        | Cloud9           | 0.0319      | 0.366      | Cloud9           | 30/07/2021 |
| FlyQuest             | Golden Guardians | FlyQuest             | Golden Guardians | 0.0         | 0.0606     | Golden Guardians | 31/07/2021 |
| Immortals            | Team Liquid      | Immortals            | Team Liquid      | 0.9658      | 0.0108     | Immortals        | 31/07/2021 |
| Counter Logic Gaming | Dignitas         | Counter Logic Gaming | Dignitas         | 0.0         | 0.0003     | Dignitas         | 31/07/2021 |
| 100 Thieves          | Golden Guardians | 100 Thieves          | Golden Guardians | 0.9481      | 0.0089     | 100 Thieves      | 31/07/2021 |
| Team Liquid          | Evil Geniuses    | Team Liquid          | Evil Geniuses    | 1.0         | 0.0        | Team Liquid      | 31/07/2021 |
| Cloud9               | Dignitas         | Cloud9               | Dignitas         | 0.9933      | 0.2375     | Cloud9           | 31/07/2021 |
|                      |

<br>
****LCK****
| Team1        | Team 2            | Blue_side    | Red_side          | T1_blue_win | T1_red_win | Predicted_winner  | Date       | Correct |
| ------------ | ----------------- | ------------ | ----------------- | ----------- | ---------- | ----------------- | ---------- | ------- |
| Liiv SANDBOX | Nongshim RedForce | Liiv SANDBOX | Nongshim RedForce | 0.2632      | 0.4435     | Nongshim RedForce | 30/07/2021 |
| KT Rolster   | Gen.G             | KT Rolster   | Gen.G             | 0.2009      | 0.1768     | Gen.G             | 30/07/2021 |
| T1           | Fredit BRION      | T1           | Fredit BRION      | 0.288       | 0.7327     | Fredit BRION      | 31/07/2021 |
| DRX          | Afreeca Freecs    | DRX          | Afreeca Freecs    | 0.0         | 0.0        | Afreeca Freecs    | 31/07/2021 |
|              |
