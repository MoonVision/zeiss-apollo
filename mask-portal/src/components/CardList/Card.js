import React, { useState, useEffect } from "react";
import "./Card.scss";

export default function Card({ onClick, selected, className, children }) {
  return (
    <div
      className={`card ${className} ${
        selected ? 'selected' : ''
      }`}
      onClick={onClick}
    >
      {children}
    </div>
  );
}