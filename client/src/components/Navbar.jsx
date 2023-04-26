import { useCallback, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Menu, Typography, Avatar, Drawer, Button, Space } from 'antd';
import {
  BulbOutlined,
  CloseCircleOutlined,
  FundOutlined,
  HomeOutlined,
  LoginOutlined,
  LogoutOutlined,
  MenuOutlined,
  RadarChartOutlined,
} from '@ant-design/icons';

import { logout } from '../features/userSlice';
import { auth } from '../firebase';
import logo from '../images/logo.png';

const Navbar = () => {
  const user = useSelector((state) => state.user?.user);

  const [windowSize, setWindowSize] = useState([
    window.innerWidth,
    window.innerHeight,
  ]);

  const [menuItems, setMenuItems] = useState();
  const [showDrawer, setShowDrawer] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const signOut = useCallback(() => {
    auth.signOut()
      .then(() => {
        dispatch(logout());
      });
  }, [dispatch]);

  useEffect(() => {
    const handleWindowResize = () => {
      setWindowSize([window.innerWidth, window.innerHeight]);
    };

    window.addEventListener('resize', handleWindowResize);

    return () => {
      window.removeEventListener('resize', handleWindowResize);
    };
  }, []);

  useEffect(() => {
    const items = [
      { label: 'Home', icon: <HomeOutlined />, key: 'home', onClick: () => navigate('/') },
      { label: 'Cryptocurrencies', icon: <FundOutlined />, key: 'cryptocurrencies', onClick: () => navigate('/cryptocurrencies') },
      { label: 'News', icon: <BulbOutlined />, key: 'news', onClick: () => navigate('/news') },
      {
        label: user?.payload ? 'Logout' : 'Login',
        icon: user?.payload ? <LogoutOutlined /> : <LoginOutlined />,
        key: user?.payload ? 'logout' : 'login',
        onClick: () => user?.payload ? signOut() : navigate('/login')
      }
    ]

    if (user?.payload) {
      items.splice(3, 0, { label: 'Metrics', icon: <RadarChartOutlined />, key: 'metrics', onClick: () => navigate('/metrics') });
    }

    setMenuItems(items);
  }, [navigate, signOut, user?.payload]);

  return (
    <div className="nav-container">
      <div className="logo-container">
        <Avatar src={logo} size="large" />
        <Typography.Title level={2} className="logo">
          <Link to="/">BitForecast</Link>
        </Typography.Title>
      </div>
      {windowSize[0] > 1000 ? (
        <Menu
          theme="dark"
          items={menuItems}
          className="navbar-menu"
          mode="vertical"
        />
      ) : (
        <>
          <div>
            <Button
              type="primary"
              onClick={() => setShowDrawer(true)}
              style={{ height: '100%' }}
            >
              <MenuOutlined />
            </Button>
          </div>
          <Drawer
            placement="left"
            onClose={() => setShowDrawer(false)}
            open={showDrawer}
            headerStyle={{ backgroundColor: '#062848', border: 'none', display: 'flex', justifyContent: 'flex-end' }}
            bodyStyle={{ backgroundColor: '#062848' }}
            closeIcon={
              <CloseCircleOutlined style={{ color: 'white', fontSize: '1.5rem' }} />
            }
          >
            <Menu
              theme="dark"
              items={menuItems}
              className="navbar-menu"
              mode="vertical"
            />
          </Drawer>
        </>
      )}
    </div>
  );
};

export default Navbar;
