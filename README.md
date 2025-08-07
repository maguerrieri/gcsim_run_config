Welcome! Sim Batcher is designed to allow you to use an existing [gcsim](https://gcsim.app/) config to calculate personal and team DPS for a batch of possible weapons or artifact sets in one go. It will optimize substats for each, it will NOT optimize mainstats. Sim Batcher works on Windows and Linux.

Based on a tool originally developed by .athene., adapted by maguerrieri with help from jamberry.

## **Setting Up Sim Batcher:**

**Step 1:** **Download uv**

uv is a Python package and project manager. You will need it for this program to run. 
Open [their website](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) and install according to their instructions depending on the computer you are using. You do not need any specific version and can likely just use the very first method they suggest.

**Step 2:** **Download Sim Batcher**

Open a terminal (such as PowerShell) wherever you would like Sim Batcher to run and run the command: 
uv tool install --upgrade --index https://us-west1-python.pkg.dev/gaymer-haus/python-public/simple/ gcsim_run_config

Congrats! You're all set up and ready to go.

## **Using Sim Batcher:**

**Step 1:** **Create or Find a gcsim Config**

Create a txt file to hold your config. Name it whatever you want- for example, SkirkBurnmeltGuideSims. Make sure to put it in whatever location you will be running Sim Batcher. Then, either write a gcsim config for the team in question, or copy one from [gcsim's public database](https://simpact.app/). 

Remember, if this is for use in a KQM guide, your config should follow [KQMS for gcsim](https://compendium.keqingmains.com/#gcsim). Even if this is not for a guide, good comments make it MUCH easier for others to read your code.

**OPTIONAL!!! Step 2:** **Narrow Down Weapons/Arti Sets**

In the Sim Batcher folder you just downloaded, open either the folder named weapons or the folder named artifacts. If you would like to narrow down which sets to consider, create a new txt file with only the weapons/artifacts to be considered using either their full name with no spaces, no uppercase, and no special characters, or using a nickname [recognized by gcsim](https://docs.gcsim.app/reference/). You can copy the full list from the other txt files in the folder and just delete useless ones. For example, in my Skirk Burnmelt team, I know Blizzard Strayer will be useless, so I'll delete that, but since she'll deal so little damage I'll leave Instructor in case it's worth it to buff my Emilie. Name this whatever you want as well- for example, SkirkSets.

**Step 3:** **Create Config Batch**

Open your terminal again, and run the command below changing terms as needed: 
gcsim-batch-weapons.exe '.\yourconfigname.txt' batchname character
mv '.\character batchname output\' ./output

"yourconfigname" should be your config txt file name. "batchname" should be what set of options you're trying to calc: artifacts, bows, catalysts, claymores, polearms, swords, or the name of the txt file you set up in Step 2 if you're a mega efficient gamer. "character" should be the character.

Example:
gcsim-batch-weapons.exe '.\SkirkBurnmeltGuideSims.txt' SkirkSets Skirk
mv '.\skirk SkirkSets output\' ./output

**Step 4:** **Run Config Batch**

Run the command below changing terms as needed again: 
gcsim-generate-batch batchname output test

Example:
gcsim-generate-batch SkirkSets output test

This should start going through all options one by one, optimizing them and then opening a browser window with the sim results. This will take a few minutes, depending on your CPU. Get up, stretch, get some water, pick up any trash you have sitting on your desk. Take a picture of your cat. Send a picture of your cat to someone. Say "I love you" to your cat. Check if it's done. Check Discord. Check if it's done again. Check your budget to consider if you can afford a better CPU. Check if it's done again. 

**Step 5:** **Cleanup**

When it finishes, you should have a browser tab open for each option in the batch, and a file named test.csv. The csv file will have each option in column A, team DPS in column E, and then individual characters' personal DPS in columns R, AA, AJ, and AS. You will need to go through each browser tab and click the "Share" button in the top right corner and then include that in your results sheet somehow. I would recommend just copying the relevant columns from your csv into a Google Sheet and then creating a column for the sim link for each option and pasting each of them in there. 

Remember, this batcher does NOT optimize mainstats. For characters where artifact set or weapon choice may affect mainstat choice, you may want to do this multiple times through for each viable mainstat, or do one batch with all options that would use a certain mainstat and another batch with all options that would use the other mainstat.
