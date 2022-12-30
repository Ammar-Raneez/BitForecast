import { configureStore } from '@reduxjs/toolkit';

import { cryptoDetailsApi } from '../services/cryptoDetailsApi';
import { cryptoNewsApi } from '../services/cryptoNewsApi';

export default configureStore({
  reducer: {
    [cryptoDetailsApi.reducerPath]: cryptoDetailsApi.reducer,
    [cryptoNewsApi.reducerPath]: cryptoNewsApi.reducer,
  },
  middleware: (getDefaultMiddleware) => {
    return getDefaultMiddleware()
      .concat(cryptoDetailsApi.middleware, cryptoNewsApi.middleware);
  }
});
