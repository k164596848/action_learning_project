# Action Learning

## What we are doing

- Using openpose to detect human body's keypoints
- Calculate action frequency by measure of angle
- Object's level is reference to 體育署 data

## Evironments

- Python 3.7 or 3.8
  - see our [requirements.txt](requirements.txt)
- OpenPose

## Install

See [Install Guide](INSTALL.md)

## Run

`python app.py`

## Usage

Check swagger (http://your.ip:port/api/v1/doc) after ran

## More details

Please check [Final report](https://drive.google.com/file/d/1cVKnpKiqlVK1KscEza4of8vurxL9W5US/view?usp=sharing)

## Module structure

```plain
.
+-- core  # core features
    +-- action.py  # action class
    +-- activity.py  # activity class
    +-- base.py  # some base classes
    +-- distribution.py  # for level evaluation
    +-- part.py  # defines body parts
    +-- segmentation.py  # segments action to different parts
+-- data  # data module
    +-- __init__.py  # Data
+-- draw  # draw module
    +-- __init__.py
    +-- body.py  # Body drawing lib
    +-- util.py  # Drawing utility
    +-- video.py  # Video drawing lib
+-- tests  # some test cases
+-- util  # utilities for core features
    +-- base.py  # base utilities
    +-- openpose.py  # command utilities for executing openpose
+-- views  # web views
    +-- __init__.py
    +-- action.py  # action view
    +-- fitness.py  # fitness view
+-- web  # utilities for web
    +-- middleware.py  # web middleware
+-- app.py  # entrance
```
