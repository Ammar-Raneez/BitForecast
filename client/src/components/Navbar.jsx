import { Link, useNavigate } from 'react-router-dom';
import { Menu, Typography, Avatar } from 'antd';
import {
  BulbOutlined,
  FundOutlined,
  HomeOutlined,
  LoginOutlined,
} from '@ant-design/icons';

import logo from '../images/logo.png';

const Navbar = () => {
  const navigate = useNavigate();

  return (
    <div className="nav-container">
      <div className="logo-container">
        <Avatar src={logo} size="large" />
        <Typography.Title level={2} className="logo">
          <Link to="/">BitForecast</Link>
        </Typography.Title>
      </div>
      <Menu
        theme="dark"
        items={[
          { label: 'Home', icon: <HomeOutlined />, key: 'home', onClick: () => navigate('/') },
          { label: 'Cryptocurrencies', icon: <FundOutlined />, key: 'cryptocurrencies', onClick: () => navigate('/cryptocurrencies') },
          { label: 'News', icon: <BulbOutlined />, key: 'news', onClick: () => navigate('/news') },
          { label: 'Login', icon: <LoginOutlined />, key: 'login', onClick: () => navigate('/login')}
        ]}
        className="navbar-menu"
      />
    </div>
  );
};

export default Navbar;
