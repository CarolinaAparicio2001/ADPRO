# Welcome to project Icaras - Part 2
---
## Rules
1. Be sure that the group submits [the link to the repo on moodle](https://moodle.novasbe.pt/mod/assign/view.php?id=318193).
2. We will pull the existing versions by 0:00, Saturday 16 March 2024. Remember: the pushes have a timestamp!

---
<div class="alert alert-danger">
    <b> NEVER USE USER PROMPTS, IT IS INFINITELY ANNOYING!! </b>
    <br>
    <b> Always use arguments for your methods.</b>
</div>


---
## Scenario (continuation)

Your company was asked to analyse Commercial Airfligh data for a sustainability study. Your group is the best team of Data Scientists in the company's roster and are given the challenge. By undertaking this task, your company expects to contribute to the green transition by having a more savvy taskforce. You decide to create some python tools for the challenge.

You spent the first day doing a lot of the code heavy lifting. It is now time to do some polishing. As you know your project might be picked up for an analysis presentation, you add an introduction about your group on the _README.md_ file. Be sure to add your **names**, **your student numbers** and **your e-mails**. It is time to add more features to the class so you can present the analysis in the showcase notebook.

## Goal
For this project, we will be using data from [International Air Transport Association](https://www.iata.org/). The datasets can be found [here](https://gitlab.com/adpro1/adpro2024/-/raw/main/Files/flight_data.zip?inline=false).

Go over the datasets. You were not given a data dictionary, but the fields can be easily discovered with an online search, as this is heavily used data.

<div class="alert alert-danger">
    <b> THE MOST IMPORTANT TOOLS FOR A DATA SCIENTIST IS PATIENCE AND COMMUNICATION</b>
    <br>
    <b> Discuss the contents of the dataset with your colleagues. Understanding the data is a priority. </b>
</div>

Use whatever python tools you find apropriate.

Day two is beginning.

### Day 2, Phase 1: Add Info with an LLM

- [ ] Define a new method called **aircrafts** that receives no arguments and prints only the list of aircraft models (Names)ircraf.
- [ ] Define a new method called **aircraft_info** that receives a string called _aircraft_name_. If the string is **NOT** in the list of aircrafts in the data, it should return an exception and present a way to guide the user into how they could choose a correct aircraft name.
- [ ] The latter method should use an LLM to print out a table of specifications about the aircraft model in Markdown.
- [ ] Define a new method called **airport_info** that does the same but for airports (don't make checks in this method, you are already demonstrating you understood it in the case for aicrafts).

<div class="alert alert-danger">
    <b> Do not include the API KEY in the project. Declare the API KEY as a system variable.</b>
    <br>
    <b> If the API KEY is not working, let me know ASAP. </b>
</div>

### Day 2, Phase 2: Decarbonisation

For this project, and for the sake of simplicity, flights under 1000km can be considered short-haul flights, although [there are several definitions](https://en.wikipedia.org/wiki/Flight_length).  
Let's do a mini-case study: Choose a country with more than 20 internal routes. This already accounts for "A to B" and "B to A".

- [ ] Refine the fifth method from Day 1: it should now also receive a float, which will be the cutoff distance for short-haul flight definition. The plot should now reflect the difference between long-haul and short-haul flights (use color, be considerate to color blind people), using the cutoff distance selected in the argument.
- [ ] How many flight routes could be considered short-haul for your country of choice? What is the total distance between airports considered short-haul flights? Print this info as a plot annotation. (Please note we want total distances, don't double count routes "A to B" and "B to A".
- [ ] Research question: a plan to cut emissions is to replace short-haul flights with rail services. Find a reference for the ratio between emissions from flights and your alternative (just a ballpark number from a credible source, include a link to your source in the showcase notebook). Taking into account all flights from your country, both internal and external, by how much would you lower flight emissions? Refine the method to also add this as an annotation onto the plot. 

### Day 2, Phase 3: Cleaning up

- [ ] Add a yaml file to git with all the packages you used, a conda environment file. This file will be used to generate an environment where your code will be ran. Remember to make it OS independent.
- [ ] Use sphinx to generate a __docs__ directory that will showcase the documentation of your code. Remember to comment .gitignore appropriately so everything is included. Update README.md to tell the user how to start using the project.

---
## Grading

Between the two parts, there are 20 gradable items in both Part 1 and 2. All items are 1 point out of 20 except for Day 1, Phase 1, which is 1 point total for the 4 items (correctly setting up git remote).

<div class="alert alert-danger">
    <b> REMEMBER: IT IS OK TO PROTOTYPE CODE IN NOTEBOOKS, BUT THE FINAL CLASS MUST BE IN A SINGLE .py FILE! </b>
    <br>
    <b> The final delivery of the project is the "showcase" notebook. Don't place this notebook together with prototyping notebooks.</b>
    <br>
    <b> Prototyping notebooks must have their own separate directory.</b>
    <br>
    <b> We will only consider contents in your "master" repository before the end of the deadline.</b>
</div>

