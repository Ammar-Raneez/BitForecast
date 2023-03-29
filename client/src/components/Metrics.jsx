import React, { useEffect, useState } from 'react';
import {
  Layout,
  Table,
  Typography,
} from 'antd';

import Loader from './Loader';
import { useGetModelEvaluationResultsQuery } from '../services/forecastApi';

function Metrics() {
  const { data, isFetching: isFetchingMetrics } = useGetModelEvaluationResultsQuery();
  const [univariateMetrics, setUnivariateMetrics] = useState();
  const [multivariateMetrics, setMultivariateMetrics] = useState();

  useEffect(() => {
    const uMetrics = data?.output?.univariate_metrics;
    const mMetrics = data?.output?.multivariate_metrics;

    const univariate = [
      {
        key: '1',
        model: 'Ensemble architecture',
        mae: uMetrics?.Ensemble?.mae,
        mse: uMetrics?.Ensemble?.mse,
        mape: uMetrics?.Ensemble?.mape,
        mase: uMetrics?.Ensemble?.mase,
        rmse: uMetrics?.Ensemble?.rmse,
      },
      {
        key: '2',
        model: 'Naive model',
        mae: uMetrics?.Naive?.mae,
        mse: uMetrics?.Naive?.mse,
        mape: uMetrics?.Naive?.mape,
        mase: uMetrics?.Naive?.mase,
        rmse: uMetrics?.Naive?.rmse,
      }
    ]

    const multivariate = [
      {
        key: '1',
        model: 'Ensemble architecture',
        mae: mMetrics?.Ensemble?.mae,
        mse: mMetrics?.Ensemble?.mse,
        mape: mMetrics?.Ensemble?.mape,
        mase: mMetrics?.Ensemble?.mase,
        rmse: mMetrics?.Ensemble?.rmse,
      },
      {
        key: '2',
        model: 'Naive model',
        mae: mMetrics?.Naive?.mae,
        mse: mMetrics?.Naive?.mse,
        mape: mMetrics?.Naive?.mape,
        mase: mMetrics?.Naive?.mase,
        rmse: mMetrics?.Naive?.rmse,
      }
    ]

    setUnivariateMetrics(univariate);
    setMultivariateMetrics(multivariate);
  }, [data?.output?.multivariate_metrics, data?.output?.univariate_metrics]);

  const columns = [
    {
      title: 'Model',
      dataIndex: 'model',
      key: 'model',
    },
    {
      title: 'MAE',
      dataIndex: 'mae',
      key: 'mae',
    },
    {
      title: 'MSE',
      dataIndex: 'mse',
      key: 'mse',
    },
    {
      title: 'MAPE',
      dataIndex: 'mape',
      key: 'mape',
    },
    {
      title: 'MASE',
      dataIndex: 'mase',
      key: 'mase',
    },
    {
      title: 'RMSE',
      dataIndex: 'rmse',
      key: 'rmse',
    },
  ];

  if (isFetchingMetrics || !univariateMetrics || !multivariateMetrics) return <Loader />;

  return (
    <Layout>
      <Typography.Title level={3} className="heading">Univariate Model Metrics</Typography.Title>
      <Table
        dataSource={univariateMetrics}
        columns={columns}
        pagination={false}
      />
      <br />
      <Typography.Title level={3} className="heading">Multivariate Model Metrics</Typography.Title>
      <Table
        dataSource={multivariateMetrics}
        columns={columns}
        pagination={false}
      />
    </Layout>
  );
}

export default Metrics;
