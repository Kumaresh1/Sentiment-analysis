import React from "react";
import { Flex, Avatar, AvatarBadge, Text } from "@chakra-ui/react";

const Header = () => {
  return (
    <Flex w="100%">
      <Avatar
        size="lg"
        name="Dan Abrahmov"
        src="https://cdn.dribbble.com/users/1044993/screenshots/6403343/carebot-dribbble.png?compress=1&resize=400x300&vertical=center"
      >
        <AvatarBadge boxSize="1.25em" bg="green.500" />
      </Avatar>
      <Flex flexDirection="column" mx="5" justify="center">
        <Text fontSize="lg" fontWeight="bold">
          MediBot
        </Text>
        <Text color="green.500">Online</Text>
      </Flex>
    </Flex>
  );
};

export default Header;
