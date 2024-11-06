import React from "react";
import { styled } from "@mui/joy/styles";
import { useDropzone } from "react-dropzone";
import Textarea from "@mui/joy/Textarea";
import Box from "@mui/joy/Box";
import Chip from "@mui/joy/Chip"
import ChipDelete from "@mui/joy/ChipDelete";
import Button from "@mui/joy/Button";
import IconButton from "@mui/joy/IconButton";
import SendIcon from "@mui/icons-material/Send";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import UploadFileOutlinedIcon from "@mui/icons-material/UploadFileOutlined";
import { sendPrompts } from "../interface/api";

const Division = styled('div')(({ theme }) => ({
  padding: theme.spacing(1, 2, 2, 2),
  display: "flex",
  flexDirection: "column"
}));

const WrapTextarea = styled(Textarea)(({ theme }) => ({
  "& .MuiTextarea-startDecorator": {
    padding: theme.spacing(0.25, 0.5, 0)
  }
}));

const Span = styled('div')(({ theme }) => ({
  flexGrow: 1
}));

function InputPanel(props) {
  const {
    sessionList,
    setSessionList
  } = props

  const [prompts, setPrompts] = React.useState("");
  const [savedPrompts, setSavedPrompts] = React.useState({ prompts: "", file: null });
  const [dropFile, setDropFile] = React.useState(null);
  const [promptsDisabled, setPromptsDisabled] = React.useState(false);
  const [sendButtonLoading, setSendButtonLoading] = React.useState(false);

  const handleAddStep = React.useCallback((fingerprint) => {
    setSessionList((sessionList) => {
      return [
        ...sessionList,
        {
          type: "Step",
          fingerprint: fingerprint,
          config: []
        }
      ];
    });
  }, [setSessionList]);

  const handleStepNew = React.useCallback((fingerprint, title) => {
    setSessionList((sessionList) => sessionList.map((item) =>
      item.fingerprint === fingerprint
        ? { ...item, config: [ ...item.config, { title: title, result: null } ] }
        : item
    ));
  }, [setSessionList]);

  const handleStepFin = React.useCallback((fingerprint, result) => {
    if (/\s*/.test(result)) {
      return;
    }
    setSessionList((sessionList) => sessionList.map((item) =>
      item.fingerprint === fingerprint
        ? {
          ...item,
          config: item.config.slice(0, -1).concat([{
            title: item.config.slice(-1)[0].title,
            result: result
          }])
        } : item
    ));
  }, [setSessionList]);

  const handleAddBubble = React.useCallback((fromUser, content, attached) => {
    setSessionList((sessionList) => [
      ...sessionList,
      {
        type: "Bubble",
        fromUser: fromUser,
        content: content,
        attached: attached
      }
    ])
  }, [setSessionList]);

  const handleAddBanner = React.useCallback((color, content) => {
    setSessionList((sessionList) => [
      ...sessionList,
      {
        type: "Banner",
        color: color,
        content: content
      }
    ])
  }, [setSessionList])

  const handleClickSend = React.useCallback(() => {
    setSendButtonLoading(true);
    setPromptsDisabled(true);

    setPrompts((prompts) => {
      setSavedPrompts({
        prompts: prompts,
        file: dropFile?.path
      });
      return "";
    })
  }, [dropFile])

  React.useEffect(() => {
    if (savedPrompts.prompts.length === 0) {
      return;
    }

    setDropFile(null);
    const filename = savedPrompts.file
      ? window.require
      ? window.require("path").basename(savedPrompts.file)
      : savedPrompts.file.split("/").slice(-1)[0]
      : null;
    handleAddBubble(true, savedPrompts.prompts, filename)
    sendPrompts(savedPrompts.prompts, savedPrompts.file, {
      handleAddBubble: handleAddBubble,
      handleAddStep: handleAddStep,
      handleStepNew: handleStepNew,
      handleStepFin: handleStepFin
    })
      .then((_) => {
        handleAddBanner("success", "Current task execution completed.");
      })
      .catch((err) => {
        console.error(err);
        err && handleAddBanner("danger", err.info ? err.info : err.toString());
      })
      .finally(() => {
        setPromptsDisabled(false);
        setSendButtonLoading(false);
        setSavedPrompts({ prompts: "", file: null });
      })
  // WARNING: savedPrompts ONLY changed in handleClickSend()
  // eslint-disable-next-line
  }, [savedPrompts]);

  const onDrop = React.useCallback((acceptedFiles) => {
    if (promptsDisabled) {
      return;
    }
    setDropFile(acceptedFiles[0]);
  }, [promptsDisabled])
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    noClick: true,
    noKeyboard: true,
    onDrop: onDrop
  })

  return (
    <Division>
      <div {...getRootProps()}>
        <input {...getInputProps()} />
        <WrapTextarea
          color="neutral"
          minRows={4}
          maxRows={4}
          sx={{
            backgroundColor: isDragActive
              ? "var(--joy-palette-neutral-300)"
              : "var(--joy-palette-neutral-100)"
          }}
          placeholder={promptsDisabled ? "" : "Send a message"}
          size="md"
          variant="soft"
          disabled={promptsDisabled}
          value={prompts}
          onChange={(event) => setPrompts(event.target.value)}
          startDecorator={dropFile &&
            <Chip
              color="primary"
              sx={{
                "--Chip-radius": "0px",
                minWidth: "100%",
                padding: 0.5,
                "& .MuiChip-label": {
                  display: "flex",
                  alignItems: "center"
                }
              }}
              endDecorator={
                <ChipDelete
                  sx={{ marginRight: 0.5 }}
                  onDelete={() => setDropFile(null)}
                />
              }
            >
              <UploadFileOutlinedIcon sx={{ marginRight: 0.5 }} />
              {dropFile.name}
            </Chip>
          }
          endDecorator={
            <Box
              sx={{
                display: 'flex',
                gap: 'var(--Textarea-paddingBlock)',
                pt: 'var(--Textarea-paddingBlock)',
                borderTop: '1px solid',
                borderColor: 'divider',
                flex: 'auto',
              }}
            >
              <IconButton
                disabled={sessionList.length === 0}
                variant="soft"
                sx={{
                  backgroundColor: sessionList.length === 0
                    ? "rgb(240, 244, 248) !important"
                    : undefined
                }}
              >
                <DeleteOutlineIcon
                  onClick={() => { setSessionList([]) }}
                />
              </IconButton>
              <Span />
              <Button
                disabled={prompts.length === 0}
                loading={sendButtonLoading}
                loadingPosition="end"
                endDecorator={<SendIcon />}
                variant="solid"
                children="SEND"
                onClick={handleClickSend}
              />
            </Box>
          }
        />
      </div>
    </Division>
  );
}

export default InputPanel;
