import React from "react";
import { styled } from "@mui/joy/styles";
import Card from "@mui/joy/Card";

const PaddingDivision = styled('div')(({ theme }) => ({
  paddingBottom: theme.spacing(2),
}));

const Banner = (props) => {
  const {
    color,
    content,
    full
  } = props;

  return (
    <PaddingDivision
      sx={{
        maxWidth: full ? "100%" : "80%",
        alignSelf: "center"
      }}
    >
      <Card
        sx={{ "--Card-radius": "0px" }}
        color={color}
        orientation="vertical"
        size="sm"
        variant="soft"
        children={content}
      />
    </PaddingDivision>
  )
};

export default Banner;
