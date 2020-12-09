# Plus-Energie-Quartier-Excel ("PE-Excel")
## Konzeptpapier 
### Starting Point: Positive Energy District Simulation with Excel
Starting from the infamous "Plusenergieexcel". It has some great merits alongside some very painful flaws:
**The Good:**
* Dynamic: It had hourly resolution: Energy balance, load profiles, PV generation, everything was known for each 8760 h of the year and could be used in a "smart algorithm" trying to optimize for own consumption, CO2 emission, etc
* Defaults: It had all defaults already set up: Plugloads of different usages (residential, office, etc), efficiencies of conversion systems
* Easy to use: It was a car ready to drive: all components already interlocked, just give us some floor areas and we have results immediately
* Comprehensible: It was … relatively .. clear how the simulation was carried out: each timestep one row, each calculation one column
* It was a One-Stop-Shop: you had all your neccessary input data, simulation logic, results and visualisations in one neat file
	
**The Bad:**
* No Version Control: each Simulation input and output was one single file. New variant means -> new file. Once you have separated files, you have no way of knowing which inputs are the same and which differ (except by filename prose and memory, which are both not very well communicatable). At this point you have to trust that you (and your collaborators) dont do any mistakes from this point onwards anymore or risk binning alot of work
* No Input-check: There is basically no way to check for errors or validate the inputs except checking every single cell, "glancing" and "plausibility"
	
**The Ugly:**
* Unwieldy: The file is upwards of 35 MB. That is not emailable. This gets old real fast.
* Unstable: The calculation takes a long time and is unstable. Many Laptops cant handle the requirements to keep all that data in memory and crash… often not letting the user save properly either. Then have fun restoring your work and checking for all the changes you made previously. Which ones made it and which didnt. Do you remember all of them? 
* Not updateable: Changing the calculation means changing the whole file. Since inputs are not readily transferrable between files, this means that you cannot check against other projects. I repeat: You cannot use older project input data with newer files.
	
So the main pain points here are:
1. Unwieldy filesize, crashes.
2. No flexible way to change calculation / simulation / algorithm
3. No easy way to calculate and store variations


# pyped  
## Concept for transitioning from Excel to Python

pyped stands for **python positive energy district** and is designed for the
following tasks:
1. Wrapping (quasi-)dynamic peb simulation methods
    * PE-Excel
        * Map xls variables to python datastructs
    * Casaclima excel?
    * Classes?
* Perform time series calculation
* flexible /optional sub-energy models. Sub-model agnostic?
* comprehensive model representation
    (eco, lca, comfort)
3. (Visual representation)
    * Plots
4. User interfaces
    * simtower
        * Modelling / Learning tool

Möglicherweise eigene Projekte, vielleicht hier als feature dabei:
* Meta-Wrapper? bzw API
    * city gml > all data (energy ADE)
    * cityJSON > same but less and less maintained. more lightweight and native
    * BIM / IFC > gibts sicher schon einiges, um die Therm. Hülle und HLKS zu bekommen
    * Open IFC vomBednar? Integral? wieh hat das geheißen?

* Git-style version control system for Variant Exploration and documentation

Ziele Was ist das Ziel von pyped
Zu 1. Mai
