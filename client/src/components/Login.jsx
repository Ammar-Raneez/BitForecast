import React from 'react';
import {
  Avatar,
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

import logo from '../images/logo-secondary.png';

function Login() {
  const onFinish = (values) => {
    console.log('Success:', values);
  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
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
              Login into the BitForecast system to update the machine learning model being used
              to forecast the Bitcoin prices.
            </Typography.Text>
          </Row>
          <br />
          <Row>
            <Typography.Text level={2} className="admin-login-desc">
              By authorizing yourself you will be able to update the model hyperparameters and retrain
              the model.
            </Typography.Text>
          </Row>
        </Col>
        <Col span={6} className="admin-login-form">
          <Form
            name="admin-login"
            labelCol={{ span: 6 }}
            initialValues={{ remember: true }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
            className="login-form"
          >
            <Divider plain={false}>
              <Typography.Title level={2} className="admin-login-title">
                Admin Login
              </Typography.Title>
            </Divider>
            <Form.Item
              name="username"
              rules={[{ required: true, message: 'Please enter the username' }]}
            >
              <Input prefix={<UserOutlined />} placeholder="Username" />
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
