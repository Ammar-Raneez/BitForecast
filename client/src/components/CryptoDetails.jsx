import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Col, Row, Spin, Typography } from 'antd';
import {
  MoneyCollectOutlined,
  DollarCircleOutlined,
  FundOutlined,
  ExclamationCircleOutlined,
  StopOutlined,
  TrophyOutlined,
  CheckOutlined,
  NumberOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons';
import HTMLReactParser from 'html-react-parser';
import millify from 'millify';

import Loader from './Loader';
import LineChart from './LineChart';
import { useGetCryptoDetailsQuery, useGetCryptoHistoryQuery } from '../services/cryptoDetailsApi';
import { getDaysArray } from '../utils/util';
import { useMultivariateForecastMutation, useUnivariateForecastMutation } from '../services/forecastApi';

const { Title, Text } = Typography;

const CryptoDetails = () => {
  const { coinId } = useParams();
  const [timeperiod, setTimeperiod] = useState('7d');
  const [dates, setDates] = useState([]);
  const [forecastFailed, setForecastFailed] = useState(false);
  const [forecastedData, setForecastedData] = useState();
  const { data, isFetching: isFetchingDetails, refetch: refetchDetails } = useGetCryptoDetailsQuery(coinId);
  const { data: coinHistory, isFetching: isFetchingHistory, refetch: refetchHistory } = useGetCryptoHistoryQuery({ coinId, timeperiod });
  const [univariateForecast, { isLoading: isUnivariateForecasting }] = useUnivariateForecastMutation();
  const [multivariateForecast, { isLoading: isMultivariateForecasting }] = useMultivariateForecastMutation();
  const cryptoDetails = data?.data?.coin;

  if (isFetchingDetails || isFetchingHistory) return <Loader />;

  const stats = [
    {
      title: 'Price to USD',
      value: `$ ${cryptoDetails?.price && millify(cryptoDetails?.price)}`,
      icon: <DollarCircleOutlined />,
    },
    {
      title: 'Rank',
      value: cryptoDetails?.rank,
      icon: <NumberOutlined />,
    },
    {
      title: '24h Volume',
      value: `$ ${cryptoDetails?.['24hVolume'] && millify(cryptoDetails?.['24hVolume'])}`,
      icon: <ThunderboltOutlined />,
    },
    {
      title: 'Market Cap',
      value: `$ ${cryptoDetails?.marketCap && millify(cryptoDetails?.marketCap)}`,
      icon: <DollarCircleOutlined />,
    },
    {
      title: 'All-time-high(daily avg.)',
      value: `$ ${cryptoDetails?.allTimeHigh?.price && millify(cryptoDetails?.allTimeHigh?.price)}`,
      icon: <TrophyOutlined />,
    },
  ];

  const genericStats = [
    {
      title: 'Number Of Markets',
      value: cryptoDetails?.numberOfMarkets,
      icon: <FundOutlined />,
    },
    {
      title: 'Number Of Exchanges',
      value: cryptoDetails?.numberOfExchanges,
      icon: <MoneyCollectOutlined />,
    },
    {
      title: 'Approved Supply',
      value: cryptoDetails?.supply?.confirmed ? <CheckOutlined /> : <StopOutlined />,
      icon: <ExclamationCircleOutlined />,
    },
    {
      title: 'Total Supply',
      value: `$ ${cryptoDetails?.supply?.total && millify(cryptoDetails?.supply?.total)}`,
      icon: <ExclamationCircleOutlined />,
    },
    {
      title: 'Circulating Supply',
      value: `$ ${cryptoDetails?.supply?.circulating && millify(cryptoDetails?.supply?.circulating)}`,
      icon: <ExclamationCircleOutlined />,
    },
  ];

  const forecast = async () => {
    const startDate = new Date(dates[0]);
    const endDate = new Date(dates[1]);
    const days = getDaysArray(startDate, endDate);
    let forecastData;

    if (days.length === 1) {
      multivariateForecast().unwrap()
        .then((res) => {
          forecastData = res.output;
          setForecastFailed(false);
          console.log(forecastData)
          setForecastedData(forecastData);
        })
        .catch((err) => {
          console.log(err);
          console.log('Something went wrong');
          setForecastFailed(true);
        });
    } else {
      univariateForecast({ days: days.length }).unwrap()
        .then((res) => {
          forecastData = res.output;
          setForecastFailed(false);
          setForecastedData(forecastData);
        })
        .catch((err) => {
          console.log(err);
          console.log('Something went wrong');
          setForecastFailed(true);
        });
    }
  }

  const resetForecast = () => {
    setForecastedData();
    setDates([]);
  }

  const invalidateDetailsAndRefetch = () => {
    refetchDetails();
    refetchHistory();
  }

  const onSetRangepicker = (e) => {
    setDates(e);
  }

  return (
    <Col className="coin-detail-container">
      <Col className="coin-heading-container">
        <Title level={2} className="coin-name">
          {data?.data?.coin.name} ({data?.data?.coin.symbol}) Price
        </Title>
        <p>
          {cryptoDetails.name} live price in US Dollar (USD). View value statistics, market cap and supply.
        </p>
      </Col>
      <Spin
        spinning={isUnivariateForecasting || isMultivariateForecasting}
        tip="Forecasting... This can take some time"
      >
        <LineChart
          coinHistory={coinHistory}
          currentPrice={millify(cryptoDetails?.price)}
          coinName={cryptoDetails?.name}
          timeperiod={timeperiod}
          setTimeperiod={setTimeperiod}
          dates={dates}
          onSetRangepicker={onSetRangepicker}
          forecast={forecast}
          forecastedData={forecastedData}
          invalidateDetailsAndRefetch={invalidateDetailsAndRefetch}
          resetForecast={resetForecast}
          forecastFailed={forecastFailed}
        />
      </Spin>
      <Col className="stats-container">
        <Col className="coin-value-statistics">
          <Col className="coin-value-statistics-heading">
            <Title level={3} className="coin-details-heading">
              {cryptoDetails.name} Value Statistics
            </Title>
            <p>
              An overview showing the statistics of {cryptoDetails.name}, such as the base and quote currency, the rank, and trading volume.
            </p>
          </Col>
          {stats.map(({ icon, title, value }) => (
            <Col className="coin-stats" key={value + title}>
              <Col className="coin-stats-name">
                <Text>{icon}</Text>
                <Text>{title}</Text>
              </Col>
              <Text className="stats">{value}</Text>
            </Col>
          ))}
        </Col>
        <Col className="other-stats-info">
          <Col className="coin-value-statistics-heading">
            <Title level={3} className="coin-details-heading">Other Stats Info</Title>
            <p>
              An overview showing the statistics of {cryptoDetails.name}, such as the base and quote currency, the rank, and trading volume.
            </p>
          </Col>
          {genericStats.map(({ icon, title, value }) => (
            <Col className="coin-stats" key={value + title}>
              <Col className="coin-stats-name">
                <Text>{icon}</Text>
                <Text>{title}</Text>
              </Col>
              <Text className="stats">{value}</Text>
            </Col>
          ))}
        </Col>
      </Col>
      <Col className="coin-desc-link">
        <Row className="coin-desc">
          <Title level={3} className="coin-details-heading">What is {cryptoDetails.name}?</Title>
          {/* Description is a raw HTML */}
          {HTMLReactParser(cryptoDetails.description)}
        </Row>
        <Col className="coin-links">
          <Title level={3} className="coin-details-heading">{cryptoDetails.name} Links</Title>
          {cryptoDetails.links?.map((link) => (
            <Row className="coin-link" key={link.url}>
              <Title level={5} className="link-name">{link.type}</Title>
              <a href={link.url} target="_blank" rel="noreferrer">{link.name}</a>
            </Row>
          ))}
        </Col>
      </Col>
    </Col>
  );
};

export default CryptoDetails;
