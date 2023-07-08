import { Flex } from "@chakra-ui/react";
import React, { useState } from "react";
import Divider from "../components/Divider";
import Footer from "../components/Footer";
import Header from "../components/Header";
import Messages from "../components/Messages";
import { Home } from "./Home";
import axios from "axios";
import { API_KEY, SERVER_URL } from "../env";
const Chat = () => {
  const [showChat, setshowChat] = useState(false);
  const [messages, setMessages] = useState([
    { from: "computer", text: "Hi, My Name is MediChat" },
    { from: "me", text: "Hey there" },
    {
      from: "computer",
      text: "Nice to meet you. You can ask me any query.",
    },
  ]);
  const [inputMessage, setInputMessage] = useState("");

  // const getOpenAIModel = async () => {
  //   const apiResponse = await axios.post(
  //     "https://api.openai.com/v1/chat/completions",
  //     {
  //       model: "text-davinci-003",
  //       messages: [
  //         { role: "system", content: "You are a helpful assistant." },
  //         { role: "user", content: "Is it working" },
  //       ],
  //     },
  //     {
  //       headers: {
  //         "Content-Type": "application/json",
  //         Authorization: `Bearer ${API_KEY}`,
  //       },
  //     }
  //   );

  //   const reply = apiResponse.data.choices[0].message.content;
  //   console.log(reply);
  // };
  const handleSendMessage = async () => {
    // getOpenAIModel();
    if (!inputMessage.trim().length) {
      return;
    }
    const data = inputMessage;

    setMessages((old) => [...old, { from: "me", text: data }]);

    await axios
      .post(SERVER_URL, {
        text: data,
      })
      .then(async (res) => {
        console.log(res.data.data);

        setMessages((old) => [
          ...old,
          { from: "computer", text: res.data.data },
        ]);
      })
      .catch((err) => {
        console.log(err);
      });
    setInputMessage("");
  };

  return (
    <>
      {showChat ? (
        <Flex w="100%" h="100vh" justify="center" align="center">
          <Flex w={["100%", "100%", "40%"]} h="90%" flexDir="column">
            <Header />
            <Divider />
            <Messages messages={messages} />
            <Divider />
            <Footer
              inputMessage={inputMessage}
              setInputMessage={setInputMessage}
              handleSendMessage={handleSendMessage}
            />
          </Flex>
        </Flex>
      ) : (
        <Home
          setshowChat={setshowChat}
          setInputMessage={setInputMessage}
          handleSendMessage={handleSendMessage}
        />
      )}
    </>
  );
};

export default Chat;
