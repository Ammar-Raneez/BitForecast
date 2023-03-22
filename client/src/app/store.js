import { configureStore } from '@reduxjs/toolkit';

import userReducer from '../features/userSlice';
import { cryptoDetailsApi } from '../services/cryptoDetailsApi';
import { cryptoNewsApi } from '../services/cryptoNewsApi';
import { forecastApi } from '../services/forecastApi';

export default configureStore({
  reducer: {
    user: userReducer,
    [cryptoDetailsApi.reducerPath]: cryptoDetailsApi.reducer,
    [cryptoNewsApi.reducerPath]: cryptoNewsApi.reducer,
    [forecastApi.reducerPath]: forecastApi.reducer,
  },
  middleware: (getDefaultMiddleware) => {
    return getDefaultMiddleware()
      .concat(
        cryptoDetailsApi.middleware,
        cryptoNewsApi.middleware,
        forecastApi.middleware,
      );
  }
});
