import React from "react";
import { styled } from "@mui/joy/styles";
import Bubble from "../interface/Bubble";
import Banner from "../interface/Banner";
import Sequence from "../interface/Step";
import ScrollToBottom from "react-scroll-to-bottom";

const Division = styled(ScrollToBottom)(({ theme }) => ({
  overflow: "auto",
  paddingBottom: theme.spacing(1),
  flexGrow: 1,
  "& >div": {
    display: "flex",
    flexDirection: "column",
    overflowX: "hidden",
    "& > :first-of-type": {
      marginTop: "auto",
      paddingTop: theme.spacing(2),
    }
  }
}));

function Session(props) {
  const {
    sessionList
  } = props

  return (
    <Division>
      {sessionList.map((item, index) =>
        item.type === "Bubble"
          ? <Bubble
            key={index}
            fromUser={item.fromUser}
            content={item.content.replaceAll(
              /<action>(.+?)<\/action>/g,
              "<code class='dialogue-cpu'>$1</code>"
            )}
            attached={item.attached}
          /> : item.type === "Banner"
          ? <Banner
            key={index}
            color={item.color}
            content={item.content}
          /> : item.type === "Step"
          ? <Sequence
            key={index}
            config={item.config}
          /> : null
      )}
    </Division>
  );
}

export default Session;
