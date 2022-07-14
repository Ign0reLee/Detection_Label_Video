# __Detection_Label_Video__

## __Installation__

### 1. Install Anaconda

[__Aanaconda__](https://www.anaconda.com/products/distribution)

<br/>

### 2. Install pytorch

Detectron provide torch version only 1.8 to 1.10, must be install right torch version.
And also must be install right CUDA

__Link__

[__PyTorch doc__](https://pytorch.org/get-started/previous-versions)

<br/>

### 3. Install Detectron2

Install Detectron2 must be gpu mode.
we provide pycocotools for python in this code, but if it is not available, please install the pycocotools

__pycocotools__

[__From source__](https://github.com/cocodataset/cocoapi) | 
[__Anaconda__](https://anaconda.org/conda-forge/pycocotools) | 
[__Windows with Conda__](https://mkwilson.tistory.com/210)

__Detectron2__

[__Windows__](https://medium.com/@yogeshkumarpilli/how-to-install-detectron2-on-windows-10-or-11-2021-aug-with-the-latest-build-v0-5-c7333909676f) | 
[__Linux__](https://detectron2.readthedocs.io/en/latest/tutorials/install.html)

<br/>

### 4. Set Enviroments

__pip__
```cmd
pip install -r requirements.txt
```

__Anaconda__
```cmd
conda install -y pyqt jupyter tqdm opencv
```
<br/>

### 5. Downolad weight


__Download and Unzip__

```
├── [Detection_Label_Video](./)
│    ├── [weights](./weights)
│       ├── [metrics.json](./weights/metrics.json)
│       ├── [coco_instances_results.json](./weights/coco_instances_results.json)
│       ├── [model_final.pth](./weights/model_final.pth)
│       ├── [model_0002999.pth](./weights/model_0002999.pth)
│       ├── [instances_predictions.pth](./weights/instances_predictions.pth)
│       ├── [last_checkpoint](./weights/last_checkpoint)
│       ├── [events.out.tfevents.1654235188.cvmilab-server.476813.0](./weights/events.out.tfevents.1654235188.cvmilab-server.476813.0])
│       └── [README.md](./weights/README.md)
```

[Weights Downloads](https://drive.google.com/file/d/1NbJGUSSih5AbkO9vQYGhsuOVko5A34zB/view?usp=sharing)



## __Run Code__
``` cmd
python main.py
```

## __How to Use It__