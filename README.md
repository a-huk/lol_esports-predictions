****What is this?****<br>
This is a side-project of mine to attempt to predict professional League of Legends games.<br>
<br>****How is it done?****<br>
Currently, I am using a classification AI to determine the winner. I will publish the code for it once I feel it is ready to see the light of day. There is sadly no official, free and reliable API available for LoLEsports. Luckily, Oracle's Elixir makes much of this data available in a very organised form. Thanks for that.<br>
<br>****Why these leagues?****<br>
I am mainly a fan of LCS and decided to preddict results on the four major regions: LEC, LPL, LCK and LEC. Sadly, there is missing data for the LPL Summer Spit of 2021, thus LPL predictions have been left out.<br>
<br>****Notes****
 - These are only predictions, therefore they might not come true. 
 - The project assumes that past performance can predict future performance, thus "upsets" will most likely never be predicted.
 - I try to run the script once a day, thus some predictions might be too late. 
 - This mainly serves as a repository for me to evaluate the long-term correctness of this approach.
 - Currently, I use a weighted average of a team's previous weeks results; the newer, the more weight a performance is given.
 - Feel free to contact me at huk.adam@protonmail.com
 - :warning: means that the academy roster was played, while the main roster's stats were used.
 - Bo1 matches use the blue team's winrate as the team's side are already known.
 - LCK and other Bo3 or Bo5 series, will use an average of the red and blue side winrate, which is not completely optimal but better than just using blue side's winrate.
<br>



****LEC:**** Correct ratio: 11/15 = 73%
| Team1                 | Team 2                | Blue_side             | Red_side              | T1_blue_win | T1_red_win | Predicted_winner      | Date       | Correct            |
| --------------------- | --------------------- | --------------------- | --------------------- | ----------- | ---------- | --------------------- | ---------- | ------------------ |
| FC Schalke 04 Esports | Team Vitality         | FC Schalke 04 Esports | Team Vitality         | 0.0001      | 0.0        | Team Vitality         | 30/07/2021 | :heavy_check_mark: |
| SK Gaming             | Astralis              | SK Gaming             | Astralis              | 0.8315      | 0.2439     | SK Gaming             | 30/07/2021 | :heavy_check_mark: |
| Excel Esports         | Rogue                 | Excel Esports         | Rogue                 | 0.0023      | 0.3163     | Rogue                 | 30/07/2021 | :heavy_check_mark: |
| MAD Lions             | G2 Esports            | MAD Lions             | G2 Esports            | 0.0532      | 0.0154     | G2 Esports            | 30/07/2021 | :heavy_check_mark: |
| Misfits Gaming        | Fnatic                | Misfits Gaming        | Fnatic                | 0.8539      | 0.9795     | Misfits Gaming        | 30/07/2021 | :heavy_check_mark: |
| Misfits Gaming        | SK Gaming             | Misfits Gaming        | SK Gaming             | 0.6934      | 0.9855     | Misfits Gaming        | 31/07/2021 | :heavy_check_mark: |
| Astralis              | Excel Esports         | Astralis              | Excel Esports         | 0.6372      | 0.4653     | Astralis              | 31/07/2021 | :x:                |
| Rogue                 | Team Vitality         | Rogue                 | Team Vitality         | 1.0         | 0.0001     | Rogue                 | 31/07/2021 | :x:                |
| G2 Esports            | FC Schalke 04 Esports | G2 Esports            | FC Schalke 04 Esports | 0.9813      | 1.0        | G2 Esports            | 31/07/2021 | :heavy_check_mark: |
| Fnatic                | MAD Lions             | Fnatic                | MAD Lions             | 0.8681      | 0.0436     | Fnatic                | 31/07/2021 | :x:                |
| Rogue                 | SK Gaming             | Rogue                 | SK Gaming             | 0.9998      | 0.4951     | Rogue                 | 01/08/2021 | :heavy_check_mark: |
| Team Vitality         | Astralis              | Team Vitality         | Astralis              | 0.5743      | 0.9675     | Team Vitality         | 01/08/2021 | :heavy_check_mark: |
| FC Schalke 04 Esports | Fnatic                | FC Schalke 04 Esports | Fnatic                | 0.8672      | 0.5121     | FC Schalke 04 Esports | 01/08/2021 | :x:                |
| Misfits Gaming        | MAD Lions             | Misfits Gaming        | MAD Lions             | 0.4266      | 0.98       | MAD Lions             | 01/08/2021 | :heavy_check_mark: |
| G2 Esports            | Excel Esports         | G2 Esports            | Excel Esports         | 0.973       | 0.3713     | G2 Esports            | 01/08/2021 | :heavy_check_mark: |
<br>
<br>
<br>


****LCS:**** Correct ratio: 8/15 = 53%
| Team1                | Team 2           | Blue_side            | Red_side         | T1_blue_win | T1_red_win | Predicted_winner     | Date       | Correct            |
| -------------------- | ---------------- | -------------------- | ---------------- | ----------- | ---------- | ----------------     | ---------- | ------------------ |
| 100 Thieves          | TSM              | 100 Thieves          | TSM              | 0.0739      | 0.2163     | TSM                  | 30/07/2021 | :heavy_check_mark: |
| Evil Geniuses        | Cloud9           | Evil Geniuses        | Cloud9           | 0.0319      | 0.366      | Cloud9               | 30/07/2021 | :x:                |
| FlyQuest             | Golden Guardians | FlyQuest             | Golden Guardians | 0.0         | 0.0606     | Golden Guardians     | 31/07/2021 | :heavy_check_mark: |
| Immortals            | Team Liquid      | Immortals            | Team Liquid      | 0.9658      | 0.0108     | Immortals            | 31/07/2021 | :x:                |
| Counter Logic Gaming | Dignitas         | Counter Logic Gaming | Dignitas         | 0.0         | 0.0003     | Dignitas             | 31/07/2021 | :heavy_check_mark: |
| 100 Thieves          | Golden Guardians | 100 Thieves          | Golden Guardians | 0.9481      | 0.0089     | 100 Thieves          | 31/07/2021 | :heavy_check_mark: |
| Team Liquid          | Evil Geniuses    | Team Liquid          | Evil Geniuses    | 1.0         | 0.0        | Team Liquid          | 31/07/2021 | :heavy_check_mark: |
| Cloud9               | Dignitas         | Cloud9               | Dignitas         | 0.9933      | 0.2375     | Cloud9               | 31/07/2021 | :heavy_check_mark: |
| FlyQuest             | Immortals        | FlyQuest             | Immortals        | 0.0001      | 0.7125     | Immortals            | 01/08/2021 | :x:                |
| Counter Logic Gaming | TSM              | Counter Logic Gaming | TSM              | 0.0         | 0.0        | TSM                  | 01/08/2021 | :heavy_check_mark: |
| Dignitas             | TSM              | Dignitas             | TSM              | 0.1621      | 0.0264     | TSM                  | 01/08/2021 | :x:                |
| Immortals            | Golden Guardians | Immortals            | Golden Guardians | 0.7571      | 0.9967     | Immortals            | 01/08/2021 | :x:                |
| Team Liquid          | Cloud9           | Team Liquid          | Cloud9           | 0.6775      | 0.0001     | Team Liquid          | 01/08/2021 | :x:                |
| 100 Thieves          | Evil Geniuses    | 100 Thieves          | Evil Geniuses    | 0.9217      | 0.006      | 100 Thieves          | 01/08/2021 | :x: :warning:      |
| Counter Logic Gaming | FlyQuest         | Counter Logic Gaming | FlyQuest         | 0.99        | 0.8959     | Counter Logic Gaming | 02/08/2021 | :heavy_check_mark: |
| Evil Geniuses        | Dignitas         | Evil Geniuses        | Dignitas         | 0.0484      | 0.9376     | Dignitas             | 07/08/2021 |
|                      |

<br>
<br>
<br>

****LCK:**** Correct ratio: 5/11 = 55%
| Team1             | Team 2              | Blue_side         | Red_side            | T1_blue_win | T1_red_win | Predicted_winner  | Date       | Correct            |
| ----------------- | ------------------- | ----------------- | ------------------- | ----------- | ---------- | ----------------- | ---------- | ------------------ |
| Liiv SANDBOX      | Nongshim RedForce   | Liiv SANDBOX      | Nongshim RedForce   | 0.2632      | 0.4435     | Nongshim RedForce | 30/07/2021 | :x:                |
| KT Rolster        | Gen.G               | KT Rolster        | Gen.G               | 0.2009      | 0.1768     | Gen.G             | 30/07/2021 | :heavy_check_mark: |
| T1                | Fredit BRION        | T1                | Fredit BRION        | 0.288       | 0.7327     | T1                | 31/07/2021 | :heavy_check_mark: |
| DRX               | Afreeca Freecs      | DRX               | Afreeca Freecs      | 0.0         | 0.0        | Afreeca Freecs    | 31/07/2021 | :x:                |
| Nongshim RedForce | Hanwha Life Esports | Nongshim RedForce | Hanwha Life Esports | 0.9838      | 0.3925     | Nongshim RedForce | 01/08/2021 | :heavy_check_mark: |
| KT Rolster        | DWG KIA             | KT Rolster        | DWG KIA             | 0.0337      | 0.0072     | DWG KIA           | 01/08/2021 | :heavy_check_mark: |
| Fredit BRION      | DWG KIA             | Fredit BRION      | DWG KIA             | 0.6977      | 0.0072     | DWG KIA           | 05/08/2021 | :heavy_check_mark: |
| Liiv SANDBOX      | Hanwha Life Esports | Liiv SANDBOX      | Hanwha Life Esports | 0.9457      | 0.7901     | Liiv SANDBOX      | 05/08/2021 | :heavy_check_mark: |
| KT Rolster        | DRX                 | KT Rolster        | DRX                 | 0.0058      | 0.1011     | DRX               | 06/08/2021 | :x:                |
| T1                | Gen.G               | T1                | Gen.G               | 0.9868      | 0.0026     | Gen.G             | 06/08/2021 | :x:                |
| Nongshim RedForce | Afreeca Freecs      | Nongshim RedForce | Afreeca Freecs      | 0.7996      | 0.9377     | Nongshim RedForce | 07/08/2021 | :x:                |
| Liiv SANDBOX      | Fredit BRION        | Liiv SANDBOX      | Fredit BRION        | 1.0         | 0.9143     | Liiv SANDBOX      | 07/08/2021 |
|                   |
<br>
<br>
