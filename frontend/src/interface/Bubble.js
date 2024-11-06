import React from "react";
import clsx from "clsx";
import { styled } from "@mui/joy/styles";
import Card from "@mui/joy/Card";
import Chip from "@mui/joy/Chip"
import UploadFileOutlinedIcon from "@mui/icons-material/UploadFileOutlined";
import PackedMarkdown from "../components/Markdown";

const PaddingDivision = styled('div')(({ theme }) => ({
  paddingBottom: theme.spacing(2),
  "& code, pre": {
    fontFamily: theme.fontFamily.code,
    fontSize: theme.fontSize.md
  },
  "& code.dialogue-user, pre.dialogue-user": {
    backgroundColor: theme.palette.neutral.softHoverBg
  },
  "& code.dialogue-cpu, pre.dialogue-cpu": {
    backgroundColor: theme.palette.primary.softHoverBg
  },
}));

const Bubble = (props) => {
  const {
    fromUser,
    content,
    attached
  } = props;

  return (
    <PaddingDivision
      sx={(theme) => ({
        maxWidth: "min(800px, 90%)",
        alignSelf: fromUser ? "flex-end" : "flex-start",
        [theme.breakpoints.only("sm")]: {
          [fromUser ? "paddingLeft" : "paddingRight"]: "min(40px, 10%)"
        },
        [theme.breakpoints.up("sm")]: {
          [fromUser ? "paddingLeft" : "paddingRight"]: "9%",
        },
        [fromUser ? "paddingRight" : "paddingLeft"]: theme.spacing(fromUser ? 1 : 2)
      })}
    >
      <Card
        className={clsx("markdown-body", fromUser ? "dialogue-user" : "dialogue-cpu")}
        color={fromUser ? "neutral" : "primary"}
        orientation="vertical"
        size="md"
        variant="soft"
      >
        {attached && <Chip
          color="primary"
          sx={{
            "--Chip-radius": "0px",
            padding: 0.5,
            "& .MuiChip-label": {
              display: "flex",
              alignItems: "center"
            }
          }}
        >
          <UploadFileOutlinedIcon sx={{ marginRight: 0.5 }} />
          {attached}
        </Chip>}
        <PackedMarkdown children={content} />
      </Card>

    </PaddingDivision>
  )
};

export default Bubble;
