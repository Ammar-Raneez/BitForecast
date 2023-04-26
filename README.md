# BitForecast

![Vercel](https://vercelbadge.vercel.app/api/Ammar-Raneez/BitForecast)
[![Heroku CI/CD](https://github.com/Ammar-Raneez/BitForecast/actions/workflows/main.yaml/badge.svg)](https://github.com/Ammar-Raneez/BitForecast/actions/workflows/main.yaml)

[![CodeQL](https://github.com/Ammar-Raneez/BitForecast/actions/workflows/codeql.yml/badge.svg)](https://github.com/Ammar-Raneez/BitForecast/actions/workflows/codeql.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/ammar-raneez/bitforecast/badge)](https://www.codefactor.io/repository/github/ammar-raneez/bitforecast)


BitForecast is a Bitcoin forecasting application that uses the Liquid Time-stochasticity network described here: https://github.com/Ammar-Raneez/Liquid-Time-stochasticity-networks for its forecasting model. Additionally, it considers multiple exogenous factors, including Twitter volume, Google Trends, Twitter sentiment, and the block reward size, alongside the basic historical prices, to produce a more robust and effective forecast.

### Prerequisities
* Node 16+
* Python 3.8+

### Monorepos
* client - frontend application built using React & Redux
* server - Flask API server for local trials & testing
* ml - Machine learning experiments, trails & testing
* deployment - Flask API server hosted in Heroku

