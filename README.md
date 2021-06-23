# Typify Tool

Typify is a novel tool that allows for the analysis of publications available on Google Scholar.

## Installation

1. Clone this GitHub repository to your computer.
2. Open "Typify.ipynb" in Jupyter Notebook.
3. Run all cells and click on blue hyperlink appearing on the bottom to start the tool.


## User manual

### **Searching**

###### **Searching for one author**
Enter the full name of an author within the “Enter author name(s)” search box and press on the “Search” button to perform the search. Example: “Jaap Stefels”. Loading times can take up to several minutes, depending on the number of publications of the queried author. <br> <br>

###### **Searching for multiple authors (research group)**
Enter the full names of the authors within the research group, separated by a comma, within the “Enter author name(s)” search box. Press on the “Search” button to perform the search. Example for two authors: “Jaap Stefels, Andy Pimentel”. Loading time can take up to several minutes, depending on the amount of queried authors and the number of publications. The full names of the found authors will be displayed within the “Found author(s)” options menu. <br> <br>

### **General topic extraction options**
###### **Found author(s)** - Select desired authors for visualisation. <br> <br>

###### **Extraction method** - Select the method by which the topics are extracted:
*Semantic* - Search for topics within publication titles semantically. 

*Syntactic* - Search for topics within publication titles syntactically. 

*Enhanced* - Search for overarching topics. This will make the search less accurate and more general. <br> <br>

###### **Year selection** - Select a minimum and maximum publication year. All publications published outside the selected years will not be considered. <br> <br>

###### **Citation minimum** - Select a minimum threshold of citations of the publications. Every publication with fewer citations than the threshold will not be considered. <br> <br>

###### **Citation impact** - Add an impact of citations count to the found topics:
*No impact* - No impact

*Multiply citation* - Multiply the number of topics by the number of citations per article. The result of this feature can be seen within the “Topic table” tab. 

*Multiply log* - Multiply the number of topics by the number of citations per article on a logarithmic scale (base 10) + 1. (1 citation -> multiplication by 1, 10 citations -> multiplication by 2, 100 citations -> multiplication by 3) The result of this feature can be seen within the “Topic table” tab.

*Quintile* - Multiply the number of topics by the number of citations per article on a quintile scale. <br> <br>

#@markdown ## **Graph options** 
#@markdown ###### **Amount of topics plot 1** - Parameter for the amount of options of the upper plot on the “Topic evolution graphs” tab. <br> <br>

###### **Amount of topics plot 2** - Parameter for the amount of options of the lower plot on the “Topic evolution graphs” tab. <br> <br>

###### **Smoothing** - Display smoothed topics in the upper plot on the “Topic evolution graphs” tab:

*No smoothing* - Add no smoothing to the upper plot.

*Historical* -  Add historical smoothing to the upper plot.

*Future* - Add future smoothing to the upper plot.

*Historical & future* - Add future smoothing to the upper plot. <br> <br>

###### **Stacking type** Select a stacking visualisation option:
*Stacked* - Display the topics stacked on top of each other of the upper plot on the “Topic evolution graphs” tab.

*Non-stacked* - Display the topics not stacked on top of each other of the upper plot on the “Topic evolution graphs” tab. <br> <br>

### **Word cloud options**
###### **Max words** - Parameter for the maximum amount of topics within the word cloud. <br> <br>

### **Publication information**
###### **Topic overlay** - Add an overlay of the topic distribution per publication year to the lower plot. <br> <br>

### **Author information**
###### **Author selection** - Select an author in case of mutlple authors.

