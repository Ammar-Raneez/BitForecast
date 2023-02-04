import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Menu, Typography, Avatar } from 'antd';
import {
  BulbOutlined,
  FundOutlined,
  HomeOutlined,
  LoginOutlined,
  LogoutOutlined,
} from '@ant-design/icons';

import { logout } from '../features/userSlice';
import { auth } from '../firebase';
import logo from '../images/logo.png';

const Navbar = () => {
  const user = useSelector((state) => state.user?.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const signOut = () => {
    auth.signOut()
      .then(() => {
        dispatch(logout());
      });
  };

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
          {
            label: user?.payload ? 'Logout' : 'Login',
            icon: user?.payload ? <LogoutOutlined /> : <LoginOutlined />,
            key: user?.payload ? 'logout' : 'login',
            onClick: () => user?.payload ? signOut() : navigate('/login')
          }
        ]}
        className="navbar-menu"
      />
    </div>
  );
};

export default Navbar;