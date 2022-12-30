import React from 'react';
import { Line } from 'react-chartjs-2';
import { Col, Row, Typography } from 'antd';
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

const LineChart = ({ coinHistory, currentPrice, coinName }) => {
  const coinPrice = [];
  const coinTimestamp = [];

  for (let i = coinHistory?.data?.history?.length - 1; i > 0; i--) {
    coinTimestamp.push(
      new Date(coinHistory?.data?.history?.[i].timestamp * 1000).toLocaleDateString()
    );

    coinPrice.push(coinHistory?.data?.history?.[i].price);
  }

  const data = {
    labels: coinTimestamp,
    datasets: [
      {
        label: 'Price in USD',
        data: coinPrice,
        fill: false,
        backgroundColor: '#0071bd',
        borderColor: '#0071bd',
      },
    ],
  };

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
      <Line data={data} options={options} />
    </>
  );
};

export default LineChart;
