import React from "react";
import { Form, Input, Button, Card } from "antd";
import "../App.css";
import axios from "axios";
import { SERVER_URL } from "../env";
import { message } from "antd";

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};

const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

export const Home = ({ setshowChat, setInputMessage, handleSendMessages }) => {
  const [messageApi, contextHolder] = message.useMessage();

  const onFinish = (values) => {
    console.log("Success:", values);
    message.loading({
      key: "loader",
      type: "loading",
      content: "loading..",
      duration: 0,
    });

    axios
      .post(SERVER_URL + "/sentiment", values)
      .then((res) => {
        console.log(res.data);
        message.destroy("loader");
        if (res.data?.sentiment !== "NEGATIVE") {
          message.error("Not a negative emotion");
        } else {
          setshowChat(true);
          setInputMessage(values.text);
          handleSendMessages();
        }
      })
      .catch((err) => {
        message.destroy("loader");
        console.log(err);
      });
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <div style={{ backgroundColor: "#8A2BE2", height: "100vh" }}>
      <div
        className="header"
        style={{ backgroundColor: "white", padding: "15px" }}
      >
        <h1 style={{ fontSize: 23 }}>Sentiment Analysis</h1>
      </div>
      <div className="center">
        <Card style={{ width: 600 }} className="shadow">
          <Form
            {...layout}
            name="basic"
            layout="vertical"
            initialValues={{ remember: true }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
          >
            <Form.Item
              label="Enter any query "
              name="text"
              rules={[{ required: true, message: "Please input something!" }]}
            >
              <Input />
            </Form.Item>

            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Card>
      </div>

      <div
        className="footer"
        style={{ backgroundColor: "white", padding: "15px" }}
      >
        <a href="terms.pdf" target="_blank">
          TERMS AND CONDITIONS
        </a>
      </div>
    </div>
  );
};
