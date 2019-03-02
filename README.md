# README

This is robot which constantly checks Github release page and notifies user about changes by email

***Notice***: This project was created before Github added this option to repositories. 


# Install
1. python3 -m pip install -r requirements.txt

2. Copy or rename urls.example.txt to urls.txt, modify it's content:

```
email: dpanic@gmail.com
username: dpanic@gmail.com
password: here_goes_your_password


# php
https://github.com/phpmyadmin/phpmyadmin/releases.atom
```


# Todo
2. Code refactor






# Docker
Running docker:

1. **Build**: 
```
docker build -t gitscanner .
```

2. **Run**: 

```
docker run --name gitscanner_instance --restart=always -d -t gitscanner
```

or 

```
docker run --name gitscanner_instance -d -t gitscanner
```


3. **Bash (if you need)**: 
```
docker exec -i -t gitscanner_instance /bin/bash
```

4. **Stop and remove**:
```
docker stop gitscanner_instance
docker rm gitscanner_instance 
docker rmi gitscanner
```

5. **Logs**
```
docker logs -f gitscanner_instance
```