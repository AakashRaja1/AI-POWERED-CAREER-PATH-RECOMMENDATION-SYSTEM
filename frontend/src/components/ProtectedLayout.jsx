/*
Protected page layout. It keeps authenticated pages inside the shared navigation and page shell.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

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
