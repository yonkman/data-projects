data source: https://www.wri.org/resources/data-sets/cait-country-greenhouse-gas-emissions-data

This packaged Tableau workbook contains three dashboards for visualizing worldwide greenhouse gas emissions data. The free [Tableau Reader](https://www.tableau.com/products/reader) or a licensed Tableau product is required to view the file.

### Dashboards:
#### World Overview
Each of the 191 countries with available data are ranked and plotted on a world map according to:
* Total GHGs
* GDP
* Population
* GDP per Capita
* GHGs per Capita
This initial sheet introduces the variables which will be explored further in subsequent sheets. In particular, we are interested in greenhouse gases per capita, which we can view as a national measure of consumption, and GDP per capita, a measure of wealth.

#### Progress??
On this sheet, each country (as well as the world total) are plotted by bubble chart, where the size of the bubble represents total emissions. The y-axis gives emissions per capita, a measure of both inefficiency and consumption. The x-axis represents GHG emissions per GDP, in tons of CO2 equivalent per $1000 USD. This can be seen as a measure of efficiency in creating wealth, where more efficient countries will be nearest the origin, while less efficient (often oil-producing) nations will have greater emissions per GDP. 

While global emissions trend clearly upwards during the plotted period (1990-2014), population has grown at a nearly equal pace. By comparing the first and last year of available data, or traversing the data year-by-year, we can see a gradual movement down and to the left, towards the origin. While far, far more work is required, looking at this 25-year evolution of emissions which is controlled for population shows some progress being made.

#### GHG Breakdown
This sheet can be used to drill down further into the emission breakdown of a specific country over time. For each country, total emissions in CO2 equivalent can be broken down by gas type, sector or subsector. In each case, the primary axis represents total emissions in MtCO2 equivalent, given by area chart, while GDP is given by the bolded line on the secondary axis. 
