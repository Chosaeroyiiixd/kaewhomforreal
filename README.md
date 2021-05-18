# How to run this kaewhomforreal project
1.Download all "kaewhomforreal" file.
2.Extract file.
3.Open cmd and create virtual environment by $ conda create -n YOUR_ENVIRONMENT_NAME python=3.6
4.Then activate that virtual environment by $ conda activate YOUR_ENVIRONMENT
5.Install django and pillow by $ conda install django=2.2 and $ conda install pillow
6.Then change directory to "kaewhomforreal" as working directory by $ cd YOUR/PATH/TO/"kaewhomforreal"
7.When you working directory is now at "kaewhomforreal" $ cd myproject
8.Apply migrate by $ python manage.py migrate.
9.Now you can run this project by $ python manage.py runserver.
10.Copy URL that generated in cmd and paste it in your browser.
