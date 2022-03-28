import React from "react";
import styles from "./HTMLOutputBlock.module.css";
import Helmet from "react-helmet";

/**
 * Renders HTML within MDX
 *
 * Include the HTML code within a block so that the MDX parser ignores it and doesn't give errors.
 * This will work with a single <script> tag and will execute the code within. BE CAREFUL!
 *
 * Attributes:
 *
 * center: centers the output horizontally
 *
 * Usage:
 * <HTMLOutputBlock>
 *
 * ```
 * <strong>bad</strong>
 * ```
 *
 * </HTMLOutputBlock
 *
 */
export const HTMLOutputBlock = ({ children, center = false }) => {
  console.log("center: ", center);
  if (!children) {
    console.warn("<HTMLOutputBlock/> should include a code block");
    return null;
  }

  if (
    !children.props?.children ||
    children.props?.children?.props?.originalType !== "code"
  ) {
    console.warn("<HTMLOutputBlock/> should include a code block");
    return null;
  }

  const html = children.props.children.props.children;

  const script = html.match(/<script[^>]*>(.*)<\/script>/s);
  const hasScript = script && script.length > 1;

  return (
    <>
      {hasScript ? (
        <Helmet>
          <script>{script[1]}</script>
        </Helmet>
      ) : null}
      <div
        className={styles.wrapper + (center ? " " + styles.center : "")}
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </>
  );
};

export default HTMLOutputBlock;
