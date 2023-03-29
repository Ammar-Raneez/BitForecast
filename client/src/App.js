import { useEffect } from 'react';
import { Link, Navigate, Route, Routes } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Layout, Space, Typography } from 'antd';
import { onAuthStateChanged } from 'firebase/auth';

import {
  Cryptocurrencies,
  CryptoDetails,
  Home,
  Login,
  Navbar,
  News,
  Metrics,
} from './components';
import { login, logout } from './features/userSlice';
import { auth } from './firebase';
import './App.css';

function App() {
  const user = useSelector((state) => state.user?.user);
  const dispatch = useDispatch();

  useEffect(() => {
    onAuthStateChanged(auth, (user) => {
      if (user) {
        dispatch(login(user.accessToken));
      } else {
        dispatch(logout());
      }
    });
  }, [dispatch]);

  return (
    <div className="app" >
      <div className="navbar">
        <Navbar />
      </div>
      <div className="main">
        <Layout style={{ justifyContent: 'center' }}>
          <div className="routes">
            <Routes>
              <Route exact path="/" element={<Home />} />
              <Route exact path="/cryptocurrencies" element={<Cryptocurrencies />} />
              <Route exact path="/crypto/:coinId" element={<CryptoDetails />} />
              <Route exact path="/news" element={<News />} />
              {user?.payload ? (
                <Route exact path="/metrics" element={<Metrics />} />
              ) : (
                <Route exact path="/metrics" element={<Navigate to="/" />} />
              )}
              {!user?.payload ? (
                <Route exact path="/login" element={<Login />} />
              ) : (
                <Route exact path="/login" element={<Navigate to="/" />} />
              )}
            </Routes>
          </div>
        </Layout>
        <div className="footer">
          <Typography.Title level={5} style={{ color: 'white', textAlign: 'center' }}>
            Copyright © {new Date().getFullYear()}
            <Link to="/">
              {' '}BitForecast Inc.
            </Link> <br />
            All Rights Reserved.
          </Typography.Title>
          <Space>
            <Link to="/">Home</Link>
            <Link to="/cryptocurrencies">Cryptocurrencies</Link>
            <Link to="/news">News</Link>
          </Space>
        </div>
      </div>
    </div>
  );
}

export default App;
