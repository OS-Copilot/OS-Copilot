import React from "react";
import Chip from "@mui/joy/Chip";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeRaw from "rehype-raw";
import gfm from "remark-gfm";
import "katex/dist/katex.min.css";
import "../interface/markdown.css";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vs } from "react-syntax-highlighter/dist/esm/styles/prism";

const PackedMarkdown = (props) => {
  const { children } = props;

  return (
    <ReactMarkdown
      remarkPlugins={[gfm, remarkMath]}
      rehypePlugins={[rehypeKatex, rehypeRaw]}
      components={{
        img: ({ node, ...props }) => (
          <img
            style={{ maxWidth: "100%" }}
            alt={props.title}
            {...props}
          />
        ),
        a: ({ node, href, ...props }) => (
          <a
            target={href[0] === "#" ? "_self" : "_blank"}
            rel="noreferrer"
            href={href}
            children={props.children}
            {...props}
          />
        ),
        code: ({ node, inline, className, children, ...props }) => {
          const match = /language-(\w+)/.exec(className || "");
          return !inline && (function () {
            const badgeID = "chip-" + Array(8).fill().reduce(
              (current) =>
                current + Math.random().toString(36).slice(2, 6),
              ""
            );
            const codeID = "code-" + Array(8).fill().reduce(
              (current) =>
                current + Math.random().toString(36).slice(2, 6),
              ""
            );
            const badgeClick = (badgeID, codeID) => () => {
              const badge = document.querySelector("#" + badgeID);
              const code = document.querySelector("#" + codeID);
              badge.style.display = "none";
              code.style.display = "block";
            };
            return (
              <React.Fragment>
                <Chip
                  id={badgeID}
                  onClick={badgeClick(badgeID, codeID)}
                >
                  · · ·
                </Chip>
                {match ? (
                  <SyntaxHighlighter
                    id={codeID}
                    style={vs}
                    customStyle={{
                      padding: "0",
                      margin: "0",
                      border: "0",
                      fontSize: "0.9rem",
                      backgroundColor: "rgba(255, 255, 255, 0)",
                      display: "none"
                    }}
                    language={match[1]}
                    PreTag="div"
                    children={String(children).replace(/\n$/, "")}
                    {...props}
                  />
                ) : (
                  <code id={codeID} className={className} style={{ display: "none" }} {...props}>
                    {children}
                  </code>
                )}
              </React.Fragment>
            )
          })();
        }
      }}
      children={children}
    />
  );
};

export default PackedMarkdown;
