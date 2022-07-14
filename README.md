# __Detection_Label_Video__

## __Installation__

### 1. Install Anaconda

[__Aanaconda__](!https://www.anaconda.com/products/distribution)

<br/>

### 2. Install pytorch

Detectron provide torch version only 1.8 to 1.10, must be install right torch version.
And also must be install right CUDA

__Link__

[__PyTorch doc__](!https://pytorch.org/get-started/previous-versions/s)

<br/>

### 3. Install Detectron2

Install Detectron2 must be gpu mode.
we provide pycocotools for python in this code, but if it is not available, please install the pycocotools

__pycocotools__

[__From source__](!https://github.com/cocodataset/cocoapi) |
[__Anaconda__](!https://anaconda.org/conda-forge/pycocotools) |
[__Windows with Conda__](!https://mkwilson.tistory.com/210)

__Detectron2__

[__Windows__](!https://medium.com/@yogeshkumarpilli/how-to-install-detectron2-on-windows-10-or-11-2021-aug-with-the-latest-build-v0-5-c7333909676f) | 
[__Linux__](https://detectron2.readthedocs.io/en/latest/tutorials/install.html)

<br/>

### 4. Set Enviroments

__For pip__
```cmd
pip install -r requirements.txt
```

__For Anaconda__
```cmd
conda install -y pyqt jupyter tqdm opencv
```
<br/>

### 5. Downolad weight
[Weights](!https://drive.google.com/file/d/1NbJGUSSih5AbkO9vQYGhsuOVko5A34zB/view?usp=sharing)

## __Run Code__
``` cmd
python main.py
```

## __How to Use It__