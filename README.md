Welcome! Sim Batcher is designed to allow you to use an existing [gcsim](https://gcsim.app/) config to calculate personal and team DPS for a batch of possible weapons or artifact sets in one go. It will optimize substats for each, it will NOT optimize mainstats. Sim Batcher works on Windows and Linux.

Based on a tool originally developed by .athene., adapted by maguerrieri with help from jamberry.

## **Setting Up Sim Batcher:**

**Step 1:** **Download uv**

uv is a Python package and project manager. You will need it for this program to run. 
Open [their website](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) and install according to their instructions depending on the computer you are using. You do not need any specific version and can likely just use the very first method they suggest.

**Step 2:** **Download Sim Batcher**

Open a terminal (such as PowerShell) wherever you would like Sim Batcher to run and run the command: 
uv tool install --upgrade --index https://us-west1-python.pkg.dev/gaymer-haus/python-public/simple/ gcsim-batcher

Congrats! You're all set up and ready to go.

## **Using Sim Batcher:**

**Step 1:** **Create or Find a gcsim Config**

Create a txt file to hold your config. Name it whatever you want- for example, SkirkBurnmelt. Make sure to put it in whatever location/folder you will be running Sim Batcher, or else you'll have to modify the commands from these instructions to help the program find your configs. Then, either write a gcsim config for the team in question, or copy one from [gcsim's public database](https://simpact.app/). 

Remember, if this is for use in a KQM guide, your config should follow [KQMS for gcsim](https://compendium.keqingmains.com/#gcsim). Even if this is not for a guide, good comments make it MUCH easier for others to read your code.

Step 2:** **Narrow Down Weapons/Arti Sets**

In the location you picked, create a new txt file with only the weapons/artifacts to be considered using either their full name with no spaces, no uppercase, and no special characters, or using a nickname [recognized by gcsim](https://docs.gcsim.app/reference/), one per row. Name your file whatever you want.
For example, I want to compare Azurelight to LoFI and Freedom-Sworn since I'm very excited about Skirk's strong melt damage potential with Nahida buffing her, so I might make a file named SuperCoolSkirkWeps that just looks like the below lines:

azurelight
lofi
freedomsworn

**Step 3:** **Create Config Batch**

Open your terminal again, and run the command below changing terms as needed: 
gcsim-generate-batch.exe .\yoursimconfigname.txt {weapon,artifact,multi} character .\yourgearsubsetname.txt outputfoldername

"yoursimconfigname" should be your sim config txt file name. {weapon,artifact,multi} means you should write weapon for a weapon comparison, artifact for an artifact comparison, or multi if you used the multi variable option in Step 2. "character" should be the character. "yourgearsubsetname" should be the name of the txt file you set up in Step 2. "outputfoldername" should be the name of the folder where the batch of configs is going to go.

Example:
gcsim-generate-batch.exe .\SkirkBurnmelt.txt weapon skirk .\SuperCoolSkirkWeps.txt SkirkBurnmeltWepBatch

This should generate a whole batch of sim configs for each gearing option you listed and store them in a folder.

**Step 4:** **Run Config Batch**

Run the command below changing terms as needed again: 
gcsim-run-batch.exe outputfoldername

Example:
gcsim-generate-batch SkirkBurnmeltWepBatch

This should start going through all options one by one, optimizing them and then opening a browser window with the sim results. This will take a few minutes, depending on your CPU. Get up, stretch, get some water, pick up any trash you have sitting on your desk. Take a picture of your cat. Send a picture of your cat to someone. Say "I love you" to your cat. Check if it's done. Check Discord. Check if it's done again. Check your budget to consider if you can afford a better CPU. Check if it's done again. 

**Step 5:** **Cleanup**

When it finishes, you should have a browser tab open for each option in the batch, and a file named test.csv. The csv file will have each option in column A, team DPS in column E, and then individual characters' personal DPS in columns R, AA, AJ, and AS. You will need to go through each browser tab and click the "Share" button in the top right corner and then include that in your results sheet somehow. I would recommend just copying the relevant columns from your csv into a Google Sheet and then creating a column for the sim link for each option and pasting each of them in there. 

Remember, this batcher does NOT optimize mainstats. For characters where artifact set or weapon choice may affect mainstat choice, you may want to do this multiple times through for each viable mainstat, or do one batch with all options that would use a certain mainstat and another batch with all options that would use the other mainstat.
