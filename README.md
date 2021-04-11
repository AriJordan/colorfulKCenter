# Colorful k-Center

The idea of this pure Python repository is to compare different algorithms for (Colorful) k-Center.  
It was created for a semester project at the Institute For Operations Research at ETH Zürich.  
It is work in progress. Help is welcome, especially with finding good (possibly heuristic) algorithms.  
High code quality is a goal, but not guaranteed.

# Instructions  
## Getting started  
- Make sure you have python3 with libraries satisfying the requirements in requirements.txt:  
```bash
pip install -r requirements.txt
```
- clone this repository:  
```bash
git clone https://github.com/AriJordan/colorfulKCenter.git
```
- run main.py:  
```
python main.py
```
## Comparing algorithms
- The runtime of algorithms can be compared with the script compareTime.py:
```
python compareTime.py
```
- The approximation ratio of algorithms can be compared with the script compareRadius.py:
```
python compareRadius.py:
```
## Adding own algorithms
You are welcome to add your own algorithms!
To do so perform the following steps:
- Create a new file in the folder **algorithms** with the name of your algorithm
- In the file create a function that accepts the parameters and returns the chosen centers in the same format as the other algorithms.
I recommend to look at the file **algorithms\\G85.py** to see what parameters are passed to and returned by the algorithms.  
The parameters are:  
`nColors`, the number of different colors of points. You may ignore this parameter and assume there is only one type (color) of point.  
`nCenters`, the number of centers, which the algorithm is allowed to create.  
`nPoints`, the total number of points.  
`p` (a numpy array), for each color this is the number of points that need to be covered by the balls around the centers. If you assume one color, assume this array has length one.  
`graph`, (a multidimensional numpy array, ndarray), which represents the distance between the points. It has four dimensions: (1) the color of the first point, (2) the id of the first point, (3) the color of the second point, (4) the id of the second point.  
The return value must be:  
`centerIds`, the chosen centers as a numpy array of pairs of ints, where the first int is the color of the center and the second int is the id of the center.  

- To run your algorithm, possibly against other algorithms, you must edit the file **algorithms\\algoInfo.py**. The simplest way is to just remove an other algorithm there and add your own instead, only changing the `name` (name of your algorithm) and `algo` (your function that you need to import on the top of the file). If you instead want to choose a new letter representig your algorithm you must also add the letter in **configuration.py** to the `algoLetters` entry.
- If you would like to add your algorithm to this repository, feel free to create a pull request.
## Asking questions
If you have any questions, remarks or whatever just make a new issue, or comment on an existing issue if it is related.  


