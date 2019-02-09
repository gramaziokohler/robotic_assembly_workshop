**Quick links:** [compas: main library docs](https://compas-dev.github.io/main/) | [compas_assembly docs](https://blockresearchgroup.github.io/compas_assembly/) | [compas_fab docs](https://gramaziokohler.github.io/compas_fab/latest/) | [slides](https://docs.google.com/presentation/d/1PsRl-eQNKiS1NvbXI4aQfWoPb0sP291kvo6l8Ps3w20/edit?usp=sharing)

# Workshop: Robotic Assembly with COMPAS framework

Materials for the Robotic Assembly workshop using COMPAS framework

> During this workshop, we will design an assembly of bricks, represented by a custom data structure, evaluate its stability and stability of the incomplete assembly at various stages of the assembly process, and plan the assembly process using a robotic arm.

## Requirements

* Operating System: **Windows 10** Pro or better <sup>(1)</sup>.
* [Rhinoceros 3D 6.0](https://www.rhino3d.com/): Focus on Rhino 6.0 only. [See here if you use Rhino 5.0](#rhino-50)
* [Anaconda Python Distribution](https://www.anaconda.com/download/): 2.7 or 3.x
* [Docker Community Edition](https://www.docker.com/get-started): Download it for [Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows) or [Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac).
* X11 Server: On Windows use [XMing](https://sourceforge.net/projects/xming/), on Mac use [XQuartz](https://www.xquartz.org/) (see details [here](https://medium.com/@mreichelt/how-to-show-x11-windows-within-docker-on-mac-50759f4b65cb)).
* Git: [official command-line client](https://git-scm.com/) or visual GUI (e.g. [Github Desktop](https://desktop.github.com/) or [SourceTree](https://www.sourcetreeapp.com/))
* [ABB RobotStudio](https://new.abb.com/products/robotics/robotstudio/downloads): 6.08 (only available for Windows). After install, **make sure you add RobotWare 6.03.02** (`Add-Ins` -> `RobotApps` -> `RobotWare` and add `6.03.02`). After completing the setup, you can open the [ABB Linear Axis station](robot_station) in RobotStudio.

> Note: if you get an error, scroll down to the [Troubleshooting](#troubleshooting) section.

<sup>(1): Windows 10 Home does not support running Docker.</sup>

## Getting started

We will install all the required **COMPAS** packages using Anaconda. Anaconda uses **environments** to create isolated spaces for projects' depedencies, it is recommendable that you do all the exercises in a newly created environment.

First, clone this repository. You have two options:

<details><summary>1. Using a visual client <i>(e.g. SourceTree)</i></summary>
Open your GIT visual client (e.g. SourceTree), and clone the repository (on SourceTree, `File -> Clone / New`) and enter the following URL and the destination folder:

      https://github.com/gramaziokohler/robotic_assembly_workshop.git

</details>

<details><summary>2. Using git command line client</summary>
Start your Anaconda Prompt, go to the destination folder where you wish to place all the workshop material and run:

      git clone https://github.com/gramaziokohler/robotic_assembly_workshop.git

</details>

<br/>

Now, we can create the environment and install all packages. Start your Anaconda Prompt (**run as administrator**), go to the repository folder you just cloned, and run:

      conda env create -f workshop.yml -n workshop
      conda activate workshop

<details><summary>Not working?</summary>

Make sure you really changed into the repository folder. For example, if you cloned the repository into a folder called `Code` in your home directory, you should type:

**On Mac**

      cd ~/Code/robotic_assembly_workshop

**On Windows**

      cd %USERPROFILE%\Code\robotic_assembly_workshop

If the command fails because you already have an environment with the same name, choose a different one, or remove the old one before creating the new one:

      conda remove -n workshop --all

</details>

<br/>

Great! Now type `python` in your Anaconda Prompt, and test if the installation went well:

      >>> import compas
      >>> import compas_fab
      >>> import compas_assembly

If that doesn't fail, you're good to go! Exit the python interpreter (either typing `exit()` or pressing `CTRL+Z` followed by `Enter`).

Now let's make all the installed packages packages available inside Rhino. Still from the Anaconda Prompt, type the following:

      python -m compas_rhino.install -v 6.0 -p compas compas_ghpython compas_rhino compas_assembly compas_fab roslibpy

Congrats! 🎉 You are all set! Open Rhino and try to import `compas` to verify everything is working fine.

> **NOTE:**
> If the previous command throws an error, make sure you run the Anaconda Prompt as an **Administrator**.

## Setting up your development environment

You can use any development environment that you're comfortable with, but for this workshop, we suggest using [VS Code](https://code.visualstudio.com/), since it provides very deep integration with Anaconda, Docker, Python debugging and many other niceties.

* Install [VS Code](https://code.visualstudio.com/) and open it
* Go to `Extensions` and install:
  * `Python` (official extension)
  * `EditorConfig for VS Code` (optional)
  * `Docker` (official extension, optional)
* On the bottom left status bar, select the python interpreter to use. The list will contain Anaconda environments, select the one created above: `workshop`.

As a starting point, check the contents of the [`examples`](examples) folder and open it with VS Code (right-click the folder from Explorer -> `Open with Code`). Open `ex00_hello_compas.py` and press `F5` to run it.

---

## Exercises

By now, you should be up and running and ready to start playing with **compas**, **compas_assembly** and **compas_fab**!

* Assembly: stack:
  * [x] Generate a stack ([example](examples/ex02_stack_generate.py))
  * [x] Identify interfaces of a stack ([example](examples/ex03_stack_interfaces.py))
  * [x] Compute contact forces required for static equilibrium of an assembly ([example](examples/ex04_stack_equilibrium.py))
  * [x] Draw stack in Rhino ([example](examples/ex05_stack_rhino.py))
* Assembly: brick wall:
  * [x] Generate an assembly for a brick wall ([example](examples/ex06_wall_generate.py))
  * [x] Add assembly support plate ([example](examples/ex07_wall_support.py))
  * [x] Identify interfaces of the brick wall assembly ([example](examples/ex08_wall_interfaces.py))
  * [x] Identify the courses of the assembly ([example](examples/ex09_wall_courses.py))
* Robotic fundamentals:
  * [x] Frame orientation specs ([example](examples/ex10_frame_orientation_specs.py))
  * [x] Expressing frames in different coordinate systems ([example](examples/ex11_transformation_frame.py))
  * [x] Create a robot model programmatically ([example](examples/ex20_robot_model))
  * [x] Load robot model from URDF ([example](examples/ex21_robot_model_from_disk.py))
  * [x] Load complete robot ([example](examples/ex22_load_compas_fab_robot.py), [exercise](examples/ex22_load_compas_fab_robot_template.py))
  * [x] Represent robot configurations / joint state ([example](examples/ex23_configuration.py))
* ROS:
  * > Before running the following examples, compose the `ROS Basic` system.
  * [x] Hello ROS ([example](examples/ex30_hello_ros.py))
* Robotic fabrication exercises:
  * [x] Create `RobotModel`
  * [x] Create `RobotArtist`
  * [x] Create `RobotClient`
  * [x] Create `Robot`
  * [x] Create a UR5 `Robot` from a `RobotModel` (URDF file), `RobotArtist` from compas_rhino, `RobotSemantics` (SRDF file), and a `RobotClient`.
  * [x] Create `Configuration`
  * [x] ..

---

## Rhino 5.0

The focus of the workshop will be on Rhino 6.0 only. While most things will work on Rhino 5.0, it is not recommended as there are several manual steps required to get the software to run.

However, if you do use Rhino 5.0, make sure to install the following:

* [Grasshopper](https://www.grasshopper3d.com/)
* [GHPython](https://www.food4rhino.com/app/ghpython)
* [IronPython 2.7.5](https://github.com/IronLanguages/main/releases/tag/ipy-2.7.5) ([see here for details about this manual update](https://compas-dev.github.io/main/environments/rhino.html#ironpython-1)).

## Troubleshooting

Sometimes things don't go as expected. Here are some of answers to the most common issues you might bump into:

> Q: Docker does not start. It complains virtualization not enabled in BIOS.

This is vendor specific, depending on the manufacturer of your computer, there are different ways to fix this, but usually, pressing a key (usually `F2` for Lenovo) before Windows even start will take you to the BIOS of your machine. In there, you will find a `Virtualization` tab where this feature can be enabled.

> Q: Cannot start containers, nor do anything with Docker. Error message indicates docker daemon not accessible or no response.

Make sure docker is running. Especially after a fresh install, docker does not start immediately. Go to the start menu, and start `Docker for Windows`.

> Q: `conda` commands don't work.

Try running them from the *Conda Prompt*. Depending on how you installed Anaconda, it might not be available by default on the normal Windows command prompt.

> Q: When trying to install the framework in Rhino, it fails indicating the lib folder of IronPython does not exist.

Make sure you have opened Rhino 6 and Grasshopper at least once, so that it finishes setting up all its internal folder structure.

> Q: It fails when trying to install on Rhino.

Try running the command prompt as administrator. Depending on the version of Python, it might be required or not.

> Q: error: Microsoft Visual C++ 14.0 is required

Follow the link to install Microsoft Visual C++ 14.0
https://www.scivision.co/python-windows-visual-c++-14-required/

> Q: When running `conda install compas_fab`, I get the error: `cannot find Frame`

You have already installed an older, pre-release version of COMPAS. Please remove it.

> Q: When installing `shapely`, I get the error: `HTTP 000 Connection Failed`

Your environment has an outdated version of OpenSSL. Go to your root environment (i.e. run `conda deactivate`) and then run the same command to install `shapely` on the workshop's environment.
