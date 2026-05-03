import React from "react";
import NavBar from "./NavBar";

const ProtectedLayout = ({ children }) => {
  return (
    <>
      <NavBar />
      {children}
    </>
  );
};

export default ProtectedLayout;
