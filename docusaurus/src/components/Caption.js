import React from "react";
import styles from "./Caption.module.css";

/**
 * Adds a caption to be used underneath an image
 * @param children The text to show in the caption
 */
export const Caption = ({ children }) => (
  <div className={styles.caption}>{children}</div>
);

export default Caption;
