import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_KEY,
  authDomain: 'bit-forecast.firebaseapp.com',
  projectId: 'bit-forecast',
  storageBucket: 'bit-forecast.appspot.com',
  messagingSenderId: '683638483894',
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: 'G-TP4YKLK0VX'
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };
