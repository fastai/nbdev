import React from "react";
import styles from "./CodeOutputBlock.module.css";

/**
 * Wrapper for code output blocks
 */
export const CodeOutputBlock = ({ children }) => (
  <div className={styles.wrapper}>{children} </div>
);

export default CodeOutputBlock;
