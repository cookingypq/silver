import React from "react";
import "./retro.css";

/**
 * 8bitInput - Pixel style input
 * @param {string} children - Input content
 * @param {string} className - Extra CSS classes
 * @param {string} font - 'normal' or 'retro'
 * @param {string} variant - style variant
 * @param {string} size - input size
 * @param {object} rest - other input props
 */
const BitInput = ({
  className = "",
  font = "retro",
  variant = "default",
  size = "default",
  ...rest
}) => {
  return (
    <div className={`bit-input-container ${className}`}>
      <input
        {...rest}
        className={`bit-input rounded-none transition-transform relative inline-flex items-center justify-center gap-1.5 ${font === "retro" ? "retro" : ""}`}
      />
      {/* Pixelated border */}
      <div className="absolute -top-1.5 w-1/2 left-1.5 h-1.5 bg-black" />
      <div className="absolute -top-1.5 w-1/2 right-1.5 h-1.5 bg-black" />
      <div className="absolute -bottom-1.5 w-1/2 left-1.5 h-1.5 bg-black" />
      <div className="absolute -bottom-1.5 w-1/2 right-1.5 h-1.5 bg-black" />
      <div className="absolute top-0 left-0 size-1.5 bg-black" />
      <div className="absolute top-0 right-0 size-1.5 bg-black" />
      <div className="absolute bottom-0 left-0 size-1.5 bg-black" />
      <div className="absolute bottom-0 right-0 size-1.5 bg-black" />
      <div className="absolute top-1.5 -left-1.5 h-2/3 w-1.5 bg-black" />
      <div className="absolute top-1.5 -right-1.5 h-2/3 w-1.5 bg-black" />
      {/* Top shadow */}
      <div className="absolute top-0 left-0 w-full h-1.5 bg-black/20" />
      <div className="absolute top-1.5 left-0 w-3 h-1.5 bg-black/20" />
      {/* Bottom shadow */}
      <div className="absolute bottom-0 left-0 w-full h-1.5 bg-black/20" />
      <div className="absolute bottom-1.5 right-0 w-3 h-1.5 bg-black/20" />
    </div>
  );
};

export default BitInput; 