import React from "react";
import { styled } from "@mui/joy/styles";
import Stepper from "@mui/joy/Stepper";
import Step from "@mui/joy/Step";
import StepIndicator from "@mui/joy/StepIndicator";
import Typography from "@mui/joy/Typography";
import Banner from "./Banner";

const PaddingDivision = styled("div")(({ theme }) => ({
  paddingBottom: theme.spacing(0),
}));

const Sequence = (props) => {
  const { config } = props;

  return (
    <PaddingDivision
      sx={{
        maxWidth: "84%",
        alignSelf: "center"
      }}
    >
      <Stepper orientation="vertical">
        {config.map((item, index) => (
          <Step
            key={index}
            indicator={
              <StepIndicator
                variant={item.result ? "soft" : "solid"}
                color={item.result ? "neutral" : "primary"}
              >
                {index + 1}
              </StepIndicator>
            }
          >
            <Typography level="title-sm">
              {item.title}
            </Typography>
            {item.result && <Banner
              color={item.result.color}
              content={item.result.content}
              full
            />}
          </Step>
        ))}
      </Stepper>
    </PaddingDivision>
  )
};

export default Sequence;
