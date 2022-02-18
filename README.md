
****What is this?****<br>
This is a side-project of mine to attempt to predict professional League of Legends games. [Here](https://github.com/a-huk/lol_esports-predictions/blob/main/results.csv) are the predictions.
<br><br>****What is the accuracy?****<br>
Current accuracy: -tflearn: 60.61% (20/33) -akkio: 60.61% (20/33)
<br><br>****Thanks****<br>
I could not do this project on my own. So here are people/organisations that I would like to thank and suggest that you check out their work.
First, thanks to [Oracle's Elixir](https://oracleselixir.com/) for the up-to-date and free data available on their website, nobody else has such data available like they do.
Second, thanks to [MRittinghouse](https://github.com/MRittinghouse) for his [oracles_elixir.py](https://github.com/MRittinghouse/ProjektZero-LoL-Model/blob/main/src/oracles_elixir.py) script and advice on OE's discord.
Third, thanks to [zlypher](https://github.com/zlypher) for his [LoL schedules](https://github.com/zlypher/lol-events)
Lastly, to anyone else that I have forgotten.
<br><br>****How is it done?****<br>
Without going into too much detail, I use two models to predict game results. The first is built using [tflearn](https://github.com/tflearn/tflearn) which is based on TensorFlow 1. It is a classification deep-neural-network.
The second model is based on [Akkio](https://www.akkio.com/), which I would describe as a all-in-one black-box AI (using their free tier), apparently it is using a Sparse Neural Network.
There is sadly no official, free and reliable API available for LoLEsports. Luckily, [Oracle's Elixir](https://oracleselixir.com/) makes much of this data available in a very organised form. Thanks for that. 
<br><br>****Why these leagues?****<br>
I am mainly a fan of the LCS and decided to predict results on the four major regions: LEC, LPL, LCK and LEC. Sadly, there is missing data for the LPL on OE, thus LPL predictions have been left out. 
<br><br>****How to get it running****<br>
This only works on Linux, there is no plan to port it to another OS. There are many different components involved, so most is managed by conda. First, clone the repository and install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html), then [import](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) [my environment](https://github.com/a-huk/lol_esports-predictions/blob/main/config/tf15.yml). 
You also need to install Firefox. Then run the predict.sh file (change it to match you username). 
Add you pandascore and akkio token.
Then voila you should be predict.
<br><br>****NOTES****<br>
 - These are only predictions, therefore they might not come true. 
 - The project assumes that past performance can predict future performance, thus "upsets" will most likely never be predicted.
 - We are determining the "stronger" team and saying that it will win.
 - I will try to run the script automatically once a day, thus all predictions should be updated daily.
 - This mainly serves as a repository for me to evaluate the long-term correctness of this approach.
 - Akkio seems to make much balder/cut&dry predictions.
 - Feel free to contact me at huk.adam@protonmail.com

<br><br>****Your code is awful!****<br>
As said above, this is not serious, just some hacked together code. 
<br><br>****How have you come to this DNN structure?****<br>
There is no easy way to find the best parameters for tflearn, I have done some limited testing trying different activation fucntions, epochs and layers. To be fair, most did not make much of a difference, take a look at the [tuning](https://github.com/a-huk/lol_esports-predictions/tree/main/tuning) folder for some non-scientific measurements.
<br><br>****Any improvements to make?****<br>
I could cache much more. Also I could save the model once it is trained and not retrain it. The training is relatively fast even on a CPU and this way it incorporates the latest data.
<br><br>****Any plans for the future?****<br>
Like MRittinghouse, I would like to create a few more models, especially based on players and combine them into an ensemble, as they are proven to give better accuracy with competent models.

