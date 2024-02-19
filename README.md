
[![](https://img.shields.io/badge/python-3.11-blue.svg?style=flat)]("https://www.python.org/")

RESTful API based on [YFinance](https://github.com/ranaroussi/yfinance)

Using the [FastApi](https://fastapi.tiangolo.com/) web framework for building the API

Using [Uvicorn](https://www.uvicorn.org/) as ASGI web server

### Run the server : 
``` {.bash}
uvicorn app.main:app
```

### Endpoints:

#### Holders :
``` {.python}
GET /holders/{symbol}
```
* Get holders for a symbol

#### Price
``` {.python}
GET /price/current-price/{symbol}
```
* Current price of a symbol

``` {.python}
POST /price/current-price-symbols
```
* Current price of a list of symbols

``` {.python}
GET /price/historical-prices
```
* Historical prices of a symbol


##### Profile
``` {.python}
GET /profile/{symbol}
```
* Profile of a symbol. Includes data such as location, industry and business summary.

#### Statistics
``` {.python}
GET /statistics/{symbol}
```
* Statistics of a symbol. Includes data such as market cap, price to book, price to earnings and earnings per share