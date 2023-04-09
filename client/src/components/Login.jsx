import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import {
  Button,
  Col,
  Divider,
  Form,
  Input,
  Layout,
  Row,
  Typography,
} from 'antd';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { signInWithEmailAndPassword } from 'firebase/auth';

import { login } from '../features/userSlice';
import { auth } from '../firebase';
import logo from '../images/logo-secondary.png';

function Login() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [errLogin, setErrLogin] = useState(false);

  const onFinish = (values) => {
    setErrLogin(false);
    const { email, password } = values;

    signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        const user = userCredential.user;
        dispatch(login(user.accessToken));
        navigate('/');
      })
      .catch(() => {
        setErrLogin(true);
      });
  };

  return (
    <Layout>
      <Row gutter={[32, 32]} style={{ justifyContent: 'center' }}>
        <Col span={6} className="admin-login-branding">
          <Row style={{ justifyContent: 'center', padding: '0rem 1rem 2rem 1rem' }}>
            <img src={logo} alt="logo" className="admin-login-logo" />
          </Row>
          <Row>
            <Typography.Text level={2} className="admin-login-desc">
              Login into the BitForecast system to view the evaluation metrics of the machine learning model being used
              to forecast the Bitcoin prices.
            </Typography.Text>
          </Row>
        </Col>
        <Col span={6} className="admin-login-form">
          <Form
            name="admin-login"
            labelCol={{ span: 6 }}
            initialValues={{ remember: true }}
            onFinish={onFinish}
            autoComplete="off"
            className="login-form"
          >
            <Divider plain={false}>
              <Typography.Title level={2} className="admin-login-title">
                Admin Login
              </Typography.Title>
            </Divider>
            <Form.Item
              name="email"
              rules={[{ required: true, message: 'Please enter the email' }]}
            >
              <Input
                type="email"
                prefix={<UserOutlined />}
                placeholder="Email"
              />
            </Form.Item>
            <Form.Item
              name="password"
              rules={[{ required: true, message: 'Please enter the password' }]}
            >
              <Input
                prefix={<LockOutlined />}
                type="password"
                placeholder="Password"
              />
            </Form.Item>
            {errLogin && (
              <Typography.Text style={{ color: 'red', textAlign: 'center' }}>
                Invalid email or password
              </Typography.Text>
            )}
            <Form.Item style={{ marginBottom: 0 }}>
              <Button type="primary" htmlType="submit" className="login-form-button">
                Authorize
              </Button>
            </Form.Item>
          </Form>
        </Col>
      </Row>
    </Layout>
  );
}

export default Login;
