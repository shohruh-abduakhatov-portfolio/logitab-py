
# Logi Back - Py

## Run

```
# help
./run.setup.sh --help
# or
./run.app.sh -h
# output: 
OPTIONS:
        -p/--prod       trun with production config
        -d/--dev        run with production config
# NOTE: you should have .env.prod file for production mode 


# to run docker,redis,mongo on seperate instance
./run.setup.sh 

# to run app itsel
./run.app.sh 
```

> IMPORTANT: do not run as root


To add submodule please refer to [```logi-core-py ```](https://gitlab.com/logitab/back-end-team/logi-core-py) instructions


# Milestone

- [ ] auto-reload handler

## SSL/HTTPS
- https://www.youtube.com/watch?v=knO_4DYdoVM
 
- https://www.youtube.com/results?search_query=https+on+aws+ec2

## Domain register

- [freenom domain](my.freenom.com)

> Domain certificate is in Virginia us-east-1
- [logitab.cloudns.cl](https://www.cloudns.net/records/domain/3011063/)


[pytz](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)

### PDF Generator
- https://pypi.org/project/pdfkit/
- https://github.com/ozawa-hi/agatereports