import React, { useState, useEffect } from "react";
import "./Card.scss";

export default function Card({ onClick, selected, className, children, style }) {
  return (
    <div
      className={`card ${className} ${
        selected ? 'selected' : ''
      }`}
      onClick={onClick}
      style={style}
    >
      {children}
    </div>
  );
}