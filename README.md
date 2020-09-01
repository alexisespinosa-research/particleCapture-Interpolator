# pyCaptureDev

This repository is for the development of python tools for estimating **particle capture in aquatic systems**. These tools use results from the research performed by: Alexis Espinosa-Gayosso, Marco Ghisalberti, Greg Ivey, Nicole Jones and Jeff Shimeta.

This repository has been published as complementary information of the manuscript:

```
Espinosa-Gayosso A., Ghisalberti M., Shimeta J. & Ivey G.N.
"On predicting particle capture rates in aquatic systems"
Submited to PLOSOne on September2020.
```
### The "pyCapture" package
This package is under the folder `pyCapture`. It contains the database generated from CFD simulations. It also contains the function for estimating the capture efficiency by direct interception:

```
pyCaptureDB.captureEfficiencyDI
```
The function can give estimates of capture efficiency for `0<Rey<=1000` and `0<=rp<=1.5`. It utilises the mentioned CFD database. Its usage is described in the example scripts and it is also utilised in the calculatorGUI.

### The "pyCaptureExampleScripts"
The script examples in this directory show how to use the `pyCaptureDB.captureEfficiencyDI` function.
The script `basicUse.py` provides a basic explanation of use.
The script `totalBiomassOptimisation_Fig-10.py` provides a more elaborated use and reproduces the Fig-10 of the manuscript.

### The "pyCaptureCalculatorGUI"
This is a simple Graphic User Interface built with Tkinter. By executing the `calculatorGUI.py`, users can input different variables or parameters for obtaining estimates of Capture Efficiency and Particle Capture Rate. The tool uses the `pyCaptureDB.captureEfficiencyDI` function.


## Python dependencies to be installed
#### Utilised by pyCapture
- numpy
- scipy

#### Additional dependencies utilised by the example scripts
- matplotlib


## For Windows:

1. Install Python-3 on your computer (look for instructions elsewhere). Any version (like 3.x.x) should work fine. 
2. Install a GIT client on your computer (look for instructions elsewhere). We recommend to use the tool: "GitHub Desktop".
3. Clone this repository into your computer. If using the command line, use:
```
git clone https://github.com/alexisespinosa-research/pyCaptureDev
```

4. Install all the Python dependencies indicated above. We have used `pip` for the installation of the dependencies. For example (from a command prompt in windows):
```
py -m pip install numpy scipy matplotlib
```

5. Execute the `calculatorGUI.py` to obtain estimates. Or inspect and execute any of the example scripts.


## For Mac or Linux:
1. Install Python-3 on your computer (look for instructions elsewhere). Any version (like 3.x.x) should work fine.
2. Install a GIT client on your computer (look for instructions elsewhere).
3. Clone this repository into your computer. If using the command line, use:
```
git clone https://github.com/alexisespinosa-research/pyCaptureDev
```

4. Install all the Python dependencies indicated above. We have used `pip` for the installation of the dependencies. For example (from a command prompt in windows):
```
python3 -m pip install numpy scipy matplotlib
```

5. Execute the `calculatorGUI.py` to obtain estimates. Or inspect and execute any of the example scripts.