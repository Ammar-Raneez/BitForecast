import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const forecastApi = createApi({
  reducerPath: 'forecastApi',
  baseQuery: fetchBaseQuery({ baseUrl: process.env.REACT_APP_BITFORECAST_API }),
  endpoints: (builder) => ({
    univariateForecast: builder.mutation({
      query: ({ days }) => ({
        url: '/api/v1/models/univariate',
        method: 'POST',
        body: { days }
      }),
    }),
    multivariateForecast: builder.mutation({
      query: () => ({
        url: '/api/v1/models/multivariate',
        method: 'POST',
      }),
    }),
  }),
});

export const {
  useUnivariateForecastMutation,
  useMultivariateForecastMutation
} = forecastApi;
