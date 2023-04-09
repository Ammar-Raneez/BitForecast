import React, { useCallback, useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Button, Col, DatePicker, Row, Select, Space, Typography } from 'antd';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import dayjs from 'dayjs';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

const { Title: TypTitle } = Typography;
const { Option } = Select;
const { RangePicker } = DatePicker;

const LineChart = ({
  coinHistory,
  currentPrice,
  coinName,
  setTimeperiod,
  timeperiod,
  dates,
  onSetRangepicker,
  forecast,
  forecastedData,
  invalidateDetailsAndRefetch,
  resetForecast,
}) => {
  const [coinPrice, setCoinPrice] = useState([]);
  const [coinTimestamp, setCoinTimestamp] = useState([]);
  const [data, setData] = useState();

  const resetDatasets = useCallback(() => {
    const timestamps = [];
    const prices = [];

    for (let i = coinHistory?.data?.history?.length - 1; i > 0; i--) {
      timestamps.push(
        new Date(coinHistory?.data?.history?.[i].timestamp * 1000).toLocaleDateString()
      );

      prices.push(coinHistory?.data?.history?.[i].price);
    }

    const graphData = {
      labels: timestamps,
      datasets: [
        {
          label: 'Price in USD',
          data: prices,
          fill: false,
          backgroundColor: 'rgba(53, 162, 235, 0.5)',
          borderColor: 'rgb(53, 162, 235)',
        },
      ],
    };

    setCoinPrice(prices);
    setCoinTimestamp(timestamps);
    setData(graphData);
    resetForecast();
  }, []);

  useEffect(() => {
    resetDatasets();
  }, []);

  useEffect(() => {
    if (forecastedData && coinPrice && coinTimestamp) {
      console.log('triggered')
      const timestamps = [];

      forecastedData?.['Predicted For']?.forEach((date) => {
        timestamps.push(new Date(date).toLocaleDateString());
      });

      const forecastedDatasets = [
        {
          label: 'Forecasted price',
          data: [...coinPrice, ...forecastedData?.['Point Forecast']],
          fill: false,
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          borderColor: 'rgb(255, 99, 132)',
        },
        {
          label: 'Upperbounds of forecasted price',
          data: [...coinPrice, ...forecastedData?.['Upperbound Forecast']],
          fill: false,
          backgroundColor: 'rgba(53, 235, 126, 0.5)',
          borderColor: 'rgb(53, 235, 126)',
        },
        {
          label: 'Lowerbounds of forecasted price',
          data: [...coinPrice, ...forecastedData?.['Lowerbound Forecast']],
          fill: false,
          backgroundColor: 'rgba(138, 53, 235, 0.5)',
          borderColor: 'rgb(138, 53, 2356)',
        },
      ];

      const graphData = {
        labels: [...coinTimestamp, ...timestamps],
        datasets: [
          {
            label: 'Price in USD',
            data: coinPrice,
            fill: false,
            backgroundColor: 'rgba(53, 162, 235, 0.5)',
            borderColor: 'rgb(53, 162, 235)',
          },
          ...forecastedDatasets,
        ],
      };

      setCoinTimestamp([...coinTimestamp, ...timestamps]);
      setData(graphData);
    };

  }, [forecastedData]);

  const options = {
    scales: {
      yAxes: {
        scaleLabel: {
          display: true,
          fontColor: 'white',
          fontSize: 25,
          labelString: 'Faction Points',
        },
        ticks: {
          beginAtZero: true,
        },
      },
    },
  };

  const time = ['24h', '7d', '30d', '3m', '1y', '3y', '5y'];

  const disabledDate = (current) => {
    return current && current < dayjs().endOf('day');
  };

  return (
    <>
      <Row className="chart-header">
        <TypTitle level={2} className="chart-title">
          {coinName} Price Chart
        </TypTitle>
        <Col className="price-container">
          <TypTitle level={5} className="price-change">
            Change: {coinHistory?.data?.change}%
          </TypTitle>
          <TypTitle level={5} className="current-price">
            Current {coinName} Price: $ {currentPrice}
          </TypTitle>
        </Col>
      </Row>
      <Row style={{ marginTop: "20px" }} justify="space-between">
        <Col>
          <Typography className="date-range-text">Past timestamp to display</Typography>
          <Select
            className="select-timeperiod"
            placeholder="Select Timeperiod"
            value={timeperiod}
            onChange={(value) => {
              setTimeperiod(value);
              invalidateDetailsAndRefetch();
              resetDatasets();
            }}
          >
            {time.map((date) => <Option key={date}>{date}</Option>)}
          </Select>
        </Col>
        {coinName?.toLowerCase() === 'bitcoin' && (
          <Col>
            <Space direction="vertical">
              <Row>
                <Typography className="date-range-text">Select date range to forecast</Typography>
              </Row>
              <Row>
                <RangePicker
                  value={dates}
                  onChange={onSetRangepicker}
                  disabledDate={disabledDate}
                />
              </Row>
              <Row justify="end">
                <Button type="primary" onClick={forecast}>Forecast</Button>
              </Row>
            </Space>
          </Col>
        )}
      </Row>
      {data && <Line data={data} options={options} />}
    </>
  );
};

export default LineChart;
